from fastapi import HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositoris.user_repository import UserRepository
from app.auth import verify_password, get_password_hash, create_access_token, decode_access_token
from app.schem import UserRegister, UserLogin, UserResponse

class AuthService:
    def __init__(self, db: AsyncSession):
        self.user_repo = UserRepository(db)
    
    async def register(self, user_data: UserRegister):
        # Проверка существования пользователя
        existing_user = await self.user_repo.get_by_username(user_data.username)
        if existing_user:
            raise HTTPException(status_code=400, detail="Username already registered")
        
        existing_email = await self.user_repo.get_by_email(user_data.email)
        if existing_email:
            raise HTTPException(status_code=400, detail="Email already registered")
        
        # Создание пользователя (первый пользователь - админ)
        is_admin = await self.user_repo.get_all_users() == []  # первый пользователь - админ
        hashed_password = get_password_hash(user_data.password)
        
        user = await self.user_repo.create(
            username=user_data.username,
            email=user_data.email,
            hashed_password=hashed_password,
            is_admin=is_admin
        )
        
        return UserResponse(id=user.id, email=user.email, username=user.username, is_admin=user.is_admin)
    
    async def login(self, login_data: UserLogin):
        user = await self.user_repo.get_by_username(login_data.username)
        if not user or not verify_password(login_data.password, user.hashed_password):
            raise HTTPException(status_code=401, detail="Invalid credentials")
        
        token = create_access_token(data={"sub": user.username, "user_id": user.id, "is_admin": user.is_admin})
        return {"access_token": token, "token_type": "bearer"}
    
    async def get_current_user(self, token: str, db: AsyncSession):
        payload = decode_access_token(token)
        if not payload:
            raise HTTPException(status_code=401, detail="Invalid token")
        
        user_id = payload.get("user_id")
        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid token")
        
        user_repo = UserRepository(db)
        user = await user_repo.get_by_id(user_id)
        if not user:
            raise HTTPException(status_code=401, detail="User not found")
        
        return user