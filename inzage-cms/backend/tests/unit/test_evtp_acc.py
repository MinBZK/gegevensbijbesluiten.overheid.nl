# from unittest.mock import AsyncMock, MagicMock, patch

# import pytest
# from fastapi import UploadFile
# from fastapi.responses import FileResponse
# from sqlalchemy.ext.asyncio import AsyncSession

# from app.config.resource import PATH_MNT
# from app.crud.evtp_acc import (
#     create_acc,
#     delete_accordering,
#     delete_files,
#     file_scan,
#     get_filenames,
#     get_files,
#     upload_files,
# )
# from app.models.evtp_acc import EvtpAcc
# from app.schemas.evtp_acc import EvtpAccIn


# @pytest.mark.asyncio
# async def test_create_acc():
#     db = AsyncMock(AsyncSession)
#     body = EvtpAccIn(evtp_cd=1, notitie="test")
#     gebruiker = "test_user"

#     result = await create_acc(db, body, gebruiker)

#     assert isinstance(result, EvtpAcc)
#     db.add.assert_called()
#     db.commit.assert_called()


# @pytest.mark.asyncio
# async def test_file_scan_ok():
#     file = MagicMock(UploadFile)
#     file.file.read.return_value = b"test content"
#     file.file.seek.return_value = None

#     with patch("app.crud.evtp_acc.clamd.ClamdNetworkSocket") as mock_clamd:
#         mock_clamd.return_value.instream.return_value = {"stream": ["OK"]}
#         result = await file_scan(file)
#         assert result == "OK"


# @pytest.mark.asyncio
# async def test_file_scan_malware():
#     file = MagicMock(UploadFile)
#     file.file.read.return_value = b"test content"
#     file.file.seek.return_value = None

#     with patch("app.crud.evtp_acc.clamd.ClamdNetworkSocket") as mock_clamd:
#         mock_clamd.return_value.instream.return_value = {"stream": ["FOUND", "Eicar-Test-Signature"]}
#         result = await file_scan(file)
#         assert "Dit bestand bevat mogelijk schadelijke data" in result


# @pytest.mark.asyncio
# async def test_upload_files():
#     db = AsyncMock(AsyncSession)
#     documents = [UploadFile(filename="test.txt", file=AsyncMock())]
#     evtp_cd = 1
#     oe_cd = 1
#     volg_nr = "1"
#     bestand_acc_cd = 1
#     gebruiker = "test_user"

#     with patch("app.crud.evtp_acc.file_scan", return_value="OK"):
#         with patch("aiofiles.open", new_callable=AsyncMock):
#             result = await upload_files(db, documents, evtp_cd, oe_cd, volg_nr, bestand_acc_cd, gebruiker)
#             assert result == "OK"


# @pytest.mark.asyncio
# async def test_delete_accordering():
#     db = AsyncMock(AsyncSession)
#     evtp_acc_cd = 1

#     with patch("app.crud.evtp_acc.get_filenames", return_value=["file1", "file2"]):
#         with patch("app.crud.evtp_acc.delete_files", return_value="DELETED"):
#             result = await delete_accordering(db, evtp_acc_cd)
#             assert result == "DELETED"


# @pytest.mark.asyncio
# async def test_get_filenames():
#     db = AsyncMock(AsyncSession)
#     evtp_acc_cd = 1

#     with patch("os.path.exists", return_value=True):
#         with patch("os.makedirs"):
#             with patch("os.listdir", return_value=["file1", "file2"]):
#                 result = await get_filenames(db, evtp_acc_cd)
#                 assert result == ["file1", "file2"]


# @pytest.mark.asyncio
# async def test_get_files():
#     file_path = "test_path"
#     result = await get_files(file_path)
#     assert isinstance(result, FileResponse)


# @pytest.mark.asyncio
# async def test_delete_files():
#     file_path = "test_path"
#     with patch("os.remove") as mock_remove:
#         result = await delete_files(file_path)
#         mock_remove.assert_called_with(f"{PATH_MNT}/{file_path}")
#         assert result == "DELETED"
