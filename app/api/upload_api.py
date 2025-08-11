from fastapi import UploadFile, File, Form, APIRouter, HTTPException,Depends
from typing import Optional
import logging
from app.container import container
from app.models.get_user_schemas import UserSchema
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
