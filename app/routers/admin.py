from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.security import OAuth2PasswordBearer
from app.database import get_db
from app.services.auth_service import AuthService
from app.repositoris.user_repository import UserRepository
from app.schem import UserResponse

router = APIRouter(prefix="/admin", tags=["Admin"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

async def get_current_admin(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)):
    auth_service = AuthService(db)
    user = await auth_service.get_current_user(token, db)
    if not user.is_admin:
        raise HTTPException(status_code=403, detail="Admin access required")
    return user

@router.get("/users", response_model=list[UserResponse])
async def get_all_users(admin: str = Depends(get_current_admin), db: AsyncSession = Depends(get_db)):
    user_repo = UserRepository(db)
    users = await user_repo.get_all_users()
    return [UserResponse(id=u.id, email=u.email, username=u.username, is_admin=u.is_admin) for u in users]