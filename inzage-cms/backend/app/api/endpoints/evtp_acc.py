import io
import logging
import os
import zipfile
from typing import Literal

from fastapi import APIRouter, Depends, File, UploadFile
from fastapi.responses import FileResponse, JSONResponse, StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession

import app.crud as crud
import app.models as models
from app.api.endpoints._default import generate_router
from app.config.resource import PATH_MNT
from app.database.database import get_async_session

# Setup logger
logger = logging.getLogger(__name__)

# Create router for login functionalities
router = APIRouter()


def crud_operations_files(router, *args):
    @router.post("/upload-files/{evtp_cd}/{oe_cd}/{volg_nr}/{bestand_acc_cd}")
    async def post_files(
        evtp_cd: int,
        oe_cd: int,
        volg_nr: str,
        bestand_acc_cd: int,
        documents: list[UploadFile] = File(...),
        db: AsyncSession = Depends(get_async_session),
    ) -> Literal["OK"]:
        """
        Takes a list of input files and applies all relevant rules.
        Findings are NOT stored in the connected database since its a dry run.

        Returns: Report containing findings and linked importance levels of rules.
        """
        return await crud.evtp_acc.upload_files(
            db,
            documents=documents,
            evtp_cd=evtp_cd,
            oe_cd=oe_cd,
            volg_nr=volg_nr,
            bestand_acc_cd=bestand_acc_cd,
            gebruiker="current_gebruiker.name",
        )

    @router.get("/get-filenames/{evtp_acc_cd}")
    async def get_filenames(
        evtp_acc_cd: int,
        db: AsyncSession = Depends(get_async_session),
    ) -> list[str]:
        return await crud.evtp_acc.get_filenames(db, evtp_acc_cd=evtp_acc_cd)

    @router.get("/get-files/{file_path}")
    async def get_files(
        file_path: str,
    ) -> FileResponse:
        return await crud.evtp_acc.get_files(
            file_path=file_path,
        )

    @router.get("/get-all-files/")
    async def get_all_files():
        file_paths = await crud.evtp_acc.get_all_files()
        zip_filename = "alle_accorderingen.zip"

        # Create a BytesIO object to store the zip file in memory
        zip_buffer = io.BytesIO()

        # Create the zip file in memory
        with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zipf:
            for file_response in file_paths:
                file_path = file_response.path
                with open(file_path, "rb") as file:
                    zipf.writestr(os.path.basename(file_path), file.read())

        # Seek to the beginning of the BytesIO buffer
        zip_buffer.seek(0)

        # Create a StreamingResponse to return the zip file
        return StreamingResponse(
            iter([zip_buffer.getvalue()]),
            media_type="application/zip",
            headers={"Content-Disposition": f"attachment; filename={zip_filename}"},
        )

    @router.post("/upload-and-extract/")
    async def upload_and_extract_zip(zip_file: UploadFile = File(...)):
        if not zip_file.filename or not zip_file.filename.endswith(".zip"):
            return JSONResponse(status_code=400, content={"message": "File must be a zip file"})

        # Ensure the extract directory exists
        os.makedirs(PATH_MNT, exist_ok=True)

        try:
            # Save the uploaded file temporarily
            temp_file = os.path.join(PATH_MNT, "temp.zip")
            with open(temp_file, "wb") as buffer:
                content = await zip_file.read()
                buffer.write(content)

            # Extract the zip file
            with zipfile.ZipFile(temp_file, "r") as zip_ref:
                zip_ref.extractall(PATH_MNT)

            # Remove the temporary zip file
            os.remove(temp_file)

            return JSONResponse(
                status_code=200,
                content={"message": "Zip file uploaded and extracted successfully", "PATH_MNT": PATH_MNT},
            )

        except zipfile.BadZipFile:
            return JSONResponse(status_code=400, content={"message": "Invalid zip file"})
        except Exception as e:
            return JSONResponse(status_code=500, content={"message": f"An error occurred: {str(e)}"})

    @router.get("/check-files/")
    async def check_files() -> bool:
        files = await crud.evtp_acc.get_all_files()
        if not files:
            return False
        return True

    @router.delete("/delete-files/{file_path}")
    async def delete_files(
        file_path: str,
    ) -> Literal["DELETED"]:
        """
        Takes a list of input files and applies all relevant rules.
        Findings are NOT stored in the connected database since its a dry run.

        Returns: Report containing findings and linked importance levels of rules.
        """
        return await crud.evtp_acc.delete_files(
            file_path=file_path,
        )


evtp_acc_router = generate_router(
    model_name="evtp_acc", base_model=models.evtp_acc.EvtpAcc, additional_routes=[crud_operations_files]
)
