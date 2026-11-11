from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.database import get_session
from app.schemas import UserCreate, UserResponse
from app.services import UserService

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(
    user_in: UserCreate, db: AsyncSession = Depends(get_session)
):
  # Check if email is already taken
  existing_user = await UserService.get_by_email(db, email=user_in.email)
  if existing_user:
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Email already registered",
    )

  # Note: In a production app, hash the password with bcrypt/argon2 here.
  hashed_password = f"{user_in.password}_hashed_placeholder"

  user = await UserService.create_user(
      db,
      email=user_in.email,
      hashed_password=hashed_password,
      full_name=user_in.full_name,
  )
  return user


@router.get("/{user_id}", response_model=UserResponse)
async def read_user(user_id: int, db: AsyncSession = Depends(get_session)):
  user = await UserService.get_by_id(db, user_id)
  if not user:
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
    )
  return user