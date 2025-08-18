from fastapi import UploadFile, File, Form, APIRouter, HTTPException,Depends
from typing import Optional
import logging
from app.container import container
from app.container import Container
from app.schemas.get_user_schemas import UserSchema
from app.utils.auth_dependcies import get_current_user

router = APIRouter()

@router.post("/upload", status_code=201)
async def upload_file(
    file: UploadFile = File(...),
    metadata: Optional[str] = Form(None),
    current_user: UserSchema = Depends(get_current_user)
):
    """
    Upload a file. Service handles both validation and storage.
    """
    try:
        # Step 1: Prepare document (validation, decoding, metadata)
        document = await container.upload_service.prepare_document(file, metadata)

        # Step 2: Upload to Mongo & Qdrant
        details = await container.upload_service.upload_document(document, user_id=str(current_user.id))

        return {
            "message": "File uploaded successfully",
            "details": details
        }

    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Upload failed: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")
    
@router.get("/fetch")
async def list_files(
    container: Container = Depends(Container),
    current_user: UserSchema = Depends(get_current_user)
):
    try:
        files = await container.mongo_repo.list_documents(user_id=str(current_user.id))
        return {
            "files": [
                {"id": f["id"], "name": f["name"]}
                for f in files
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
