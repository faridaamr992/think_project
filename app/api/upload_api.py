from fastapi import UploadFile, File, Form, APIRouter, HTTPException, status
from typing import Optional
import json
import logging

from app.container import container
from app.models.upload_schemas import DocumentCreate

router = APIRouter()

@router.post("/", status_code=status.HTTP_201_CREATED)
async def upload_file(
    file: UploadFile = File(...),
    metadata: Optional[str] = Form(None),
):
    """
    Upload a file. Contents will be processed and stored.
    """
    try:
        # Check file size before reading
        if hasattr(file, "size") and file.size and file.size > 1_000_000:  # 1MB limit
            raise HTTPException(
                status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                detail="File too large. Please upload a file smaller than 1MB"
            )

        # Read file in chunks
        content_chunks = []
        chunk_size = 8192  # 8KB chunks
        while True:
            chunk = await file.read(chunk_size)
            if not chunk:
                break
            content_chunks.append(chunk)

        # Combine chunks and decode
        content = b"".join(content_chunks)
        try:
            content_str = content.decode("utf-8")
        except UnicodeDecodeError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="File must be UTF-8 encoded text"
            )

        # Validate content length
        if len(content_str) < 10:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="File content too short"
            )

        # Parse metadata
        metadata_dict = {}
        if metadata:
            try:
                metadata_dict = json.loads(metadata)
                if not isinstance(metadata_dict, dict):
                    raise ValueError("Metadata must be a JSON object")
            except json.JSONDecodeError:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Invalid metadata JSON format"
                )

        # Create document
        document = DocumentCreate(
            content=content_str,
            metadata={
                **metadata_dict,
                "filename": file.filename,
                "content_type": file.content_type
            }
        )

        # Upload document using container service
        result = await container.upload_service.upload_document(document)

        return {
            "message": "File uploaded successfully",
            "details": result
        }

    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Upload failed: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Upload failed: {str(e)}"
        )
    finally:
        await file.close()
