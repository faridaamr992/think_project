from fastapi import APIRouter, Depends
from app.container import Container


router = APIRouter()

@router.get("/files")
async def list_files(container: Container = Depends(Container)):
    files = await container.mongo_repo.list_documents()
    return {
    "files": [
        {"id": f["id"], "name": f["name"]}
        for f in files
    ]
}

