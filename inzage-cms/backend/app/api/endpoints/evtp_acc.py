import logging
from typing import Literal

from fastapi import APIRouter, Depends, File, UploadFile
from fastapi.responses import FileResponse
from sqlalchemy.ext.asyncio import AsyncSession

import app.crud as crud
import app.models as models
from app.api.endpoints._default import generate_router
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
        # current_gebruiker: schemas.gebruiker.Gebruiker = Depends(dependencies.get_current_gebruiker),
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
        """
        Takes a list of input files and applies all relevant rules.
        Findings are NOT stored in the connected database since its a dry run.

        Returns: Report containing findings and linked importance levels of rules.
        """
        return await crud.evtp_acc.get_filenames(db, evtp_acc_cd=evtp_acc_cd)

    @router.get("/get-files/{file_path}")
    async def get_files(
        file_path: str,
    ) -> FileResponse:
        """
        Takes a list of input files and applies all relevant rules.
        Findings are NOT stored in the connected database since its a dry run.

        Returns: Report containing findings and linked importance levels of rules.
        """
        return await crud.evtp_acc.get_files(
            file_path=file_path,
        )

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
