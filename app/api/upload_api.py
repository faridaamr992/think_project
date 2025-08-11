from fastapi import UploadFile, File, Form, APIRouter, HTTPException
from typing import Optional
import logging
from app.container import container

router = APIRouter()

@router.post("/", status_code=201)
async def upload_file(
    file: UploadFile = File(...),
    metadata: Optional[str] = Form(None),
):
    """
    Upload a file. Service handles both validation and storage.
    """
    try:
        # Step 1: Prepare document (validation, decoding, metadata)
        document = await container.upload_service.prepare_document(file, metadata)

        # Step 2: Upload to Mongo & Qdrant
        details = await container.upload_service.upload_document(document)

        return {
            "message": "File uploaded successfully",
            "details": details
        }

    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Upload failed: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")
