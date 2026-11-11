
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.models import User


class UserService:

  @staticmethod
  async def get_by_id(db: AsyncSession, user_id: int) -> User | None:
    result = await db.exec(select(User).where(User.id == user_id))
    return result.first()

  @staticmethod
  async def get_by_email(db: AsyncSession, email: str) -> User | None:
    result = await db.exec(select(User).where(User.email == email))
    return result.first()

  @staticmethod
  async def create_user(
      db: AsyncSession, *, email: str, hashed_password: str, full_name: str | None = None
  ) -> User:
    db_user = User(
        email=email,
        hashed_password=hashed_password,
        full_name=full_name,
    )
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user