from fastapi import APIRouter, Depends, HTTPException
from app.container import Container
from app.utils.auth_dependcies import get_current_user
from app.schemas.get_user_schemas import UserSchema  # or your User model

router = APIRouter()

@router.get("/files")
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
