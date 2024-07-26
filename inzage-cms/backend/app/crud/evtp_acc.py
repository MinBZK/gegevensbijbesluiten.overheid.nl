import asyncio
import io
import logging
import os
import re
from datetime import datetime
from os import listdir
from os.path import isfile, join
from pathlib import Path
from typing import Literal
from zipfile import ZipFile

import aiofiles
import clamd
from fastapi import UploadFile
from fastapi.responses import FileResponse
from sqlalchemy import exc, select
from sqlalchemy.ext.asyncio import AsyncSession

import app.models as models
import app.schemas as schemas
from app.api import exceptions
from app.config.resource import PATH_MNT

CLAMAV_HOST = os.getenv("CLAMAV_HOST", "")

# Setup logger
logger = logging.getLogger(__name__)


async def create_acc(
    db: AsyncSession, body: schemas.evtp_acc.EvtpAccIn, gebruiker: str | None
) -> models.evtp_acc.EvtpAcc:
    """
    Create a new EvtpAcc record in the database.

    Args:
        body: The input data for creating the EvtpAcc record.
        gebruiker: The user name associated with the record.

    Returns: The created EvtpAcc record.
    """
    payload_file = {
        "volg_nr": 1,
        "omschrijving": "",
        "bestand_verwijzing": "",
        "ts_create": datetime.now(),
        "user_nm": gebruiker,
    }

    model = models.evtp_acc.BestandAcc
    accordering = model(**payload_file)
    async with db.begin():
        db.add(accordering)

    payload_org = {
        **body.model_dump(exclude_unset=True),
        "ts_acc": datetime.now(),
        "bestand_acc_cd": accordering.bestand_acc_cd,
        "user_nm": gebruiker,
    }

    model = models.evtp_acc.EvtpAcc
    accordering = model(**payload_org)
    async with db.begin():
        db.add(accordering)
    return accordering


async def file_scan(file: UploadFile) -> str:
    """
    Scan the file for malware
    Returns:: "OK" on success, or an error message
    """
    if CLAMAV_HOST is None or CLAMAV_HOST == "":
        logger.warning("clamav host is not configured")
        return "OK"

    try:
        cd = clamd.ClamdNetworkSocket(host=CLAMAV_HOST, port=3310, timeout=30)
        file.file.seek(0)  # just in case another function didnt move the pointer
        response = cd.instream(file.file)
        file.file.seek(0)
        if response is None:
            raise clamd.ResponseError("Error 204; empty response from service")

    except TimeoutError as err:
        logger.exception(err)
        return "Timeout, het scannen duurt te lang. Probeer het later opnieuw of verwijder onnodige data"

    except clamd.ConnectionError as err:
        logger.exception(err)
        return "Error, kan geen verbinding maken met de virusscanner"

    except clamd.ResponseError as err:
        logger.exception(err)
        return str(err)

    except Exception as err:
        logger.exception(err)
        return str(err)

    logger.info(response["stream"])
    if response["stream"][0] == "OK":
        return "OK"
    else:
        logger.warning(f'Malware gevonden {response["stream"][1]}')
        return "Dit bestand bevat mogelijk schadelijke data. Neem contact op met uw ICT afdeling"


async def upload_files(
    db: AsyncSession,
    documents: list[UploadFile],
    evtp_cd: int,
    oe_cd: int,
    volg_nr: str,
    bestand_acc_cd: int,
    gebruiker: str | None,
) -> Literal["OK"]:
    """
    Uploads files to the database.

    Args:
        documents: The list of files to upload.
        evtp_cd: The event code.
        oe_cd: The order code.
        volg_nr: The sequence number.
        bestand_acc_cd: The file access code.
        gebruiker: The user name.

    Raises:
        exceptions.MalwareDetected: If malware is detected in any of the files.
        exceptions.FileFormatDoesNotMatch: If the file format does not match the allowed formats.
    """
    unzipped_documents = []

    payload_file = {
        "bestand_acc_cd": bestand_acc_cd,
        "volg_nr": 1,
        "omschrijving": "",
        "bestand_verwijzing": "",
        "ts_create": datetime.now(),
        "user_nm": gebruiker,
    }

    file_output_path = f"{PATH_MNT}/{evtp_cd}_{oe_cd}_{volg_nr}"

    for doc in documents:
        res = await file_scan(doc)
        if res != "OK":
            raise exceptions.MalwareDetected(res)

        if doc.content_type in [
            "application/zip",
            "application/x-zip-compressed",
        ]:
            with ZipFile(io.BytesIO(doc.file.read()), "r") as zf:
                for item in zf.namelist():
                    f = zf.open(item)
                    unzipped_documents.append(UploadFile(filename=f.name, file=io.BytesIO(f.read())))
        elif doc.content_type in [
            "text/pdf",
            "application/pdf",
            "text/plain",
            "text/word",
            "application/word",
        ]:
            unzipped_documents.append(doc)
        else:
            raise exceptions.FileFormatDoesNotMatch

    for index, unzipped_document in enumerate(unzipped_documents, 1):
        file_output_path_volg_nr = f"{file_output_path}_{index}.pdf"
        payload_file["bestand_verwijzing"] = f"{evtp_cd}_{oe_cd}_{volg_nr}"
        bestand_acc_volg_nr = index

        while Path(file_output_path_volg_nr).exists():
            bestand_acc_volg_nr = int(re.findall(r"\d+\.pdf", file_output_path_volg_nr)[-1][:-4])
            file_output_path_volg_nr = f"{file_output_path}_{bestand_acc_volg_nr + 1}.pdf"
            bestand_acc_volg_nr += 1
            payload_file["volg_nr"] = bestand_acc_volg_nr

        async with aiofiles.open(file_output_path_volg_nr, "wb") as out_file:
            content = await unzipped_document.read()
            await out_file.write(content)
        payload_file["volg_nr"] = bestand_acc_volg_nr

    model = models.evtp_acc.BestandAcc
    accordering = model(**payload_file)
    async with db.begin():
        await db.merge(accordering)
        await db.commit()
        return "OK"


async def delete_accordering(db: AsyncSession, evtp_acc_cd: int) -> Literal["DELETED"]:
    """
    Delete the EvtpAcc and BestandAcc records associated with the given evtp_acc_cd.

    Args:
        evtp_acc_cd: The evtp_acc_cd of the records to be deleted.

    Returns: A string indicating that the records have been deleted.
    """

    async with db.begin():
        name_files = await get_filenames(db=db, evtp_acc_cd=evtp_acc_cd)

        # delete files in concurrent processes
        await asyncio.gather(*[delete_files(file_path=file_path) for file_path in name_files])

        try:
            # delete EvtpAcc record
            model = models.evtp_acc.EvtpAcc
            result = await db.execute(select(model).filter(model.evtp_acc_cd == evtp_acc_cd))
            relation = result.scalar_one()
            await db.delete(relation)

            # get BestandAcc record
            result = await db.execute(
                select(models.evtp_acc.BestandAcc.bestand_acc_cd)
                .join(models.evtp_acc.EvtpAcc)
                .filter(models.evtp_acc.EvtpAcc.evtp_acc_cd == evtp_acc_cd)
            )
            bestand_acc_cd = result.scalar_one()

            # delete BestandAcc record
            model = models.evtp_acc.BestandAcc
            result = await db.execute(select(model).filter(model.bestand_acc_cd == bestand_acc_cd))
            relation = result.scalar_one()
            await db.delete(relation)

        except exc.IntegrityError as e:
            logging.error(e)
            raise exceptions.ForeignKeyError()

    return "DELETED"


async def get_filenames(db: AsyncSession, evtp_acc_cd: int) -> list[str]:
    """
    Retrieve a list of filenames based on the provided evtp_acc_cd.

    Args:
        evtp_acc_cd: The evtp_acc_cd to filter the filenames.

    Returns: A list of filenames that match the provided evtp_acc_cd.
    """
    result = await db.execute(
        select(models.evtp_acc.BestandAcc.bestand_verwijzing)
        .join(models.evtp_acc.EvtpAcc)
        .filter(models.evtp_acc.EvtpAcc.evtp_acc_cd == evtp_acc_cd)
    )
    bestand_verwijzing = result.scalar_one()

    if not os.path.exists(PATH_MNT):
        os.makedirs(PATH_MNT)

    files_list = [
        file
        for file in listdir(PATH_MNT)
        if isfile(join(PATH_MNT, file)) and file.startswith(bestand_verwijzing) and bestand_verwijzing
    ]
    return files_list


async def get_files(file_path: str) -> FileResponse:
    return FileResponse(os.path.join(PATH_MNT, file_path))


async def delete_files(file_path: str) -> Literal["DELETED"]:
    os.remove(os.path.join(PATH_MNT, file_path))
    return "DELETED"
