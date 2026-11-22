from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.models import User


class ServiceError(Exception):
    """Base exception for service-layer errors."""


class UserAlreadyExistsError(ServiceError):
    """Raised when attempting to create a user with an existing email."""

    def __init__(self, email: str):
        self.email = email
        super().__init__(f"User with email '{email}' already exists.")

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
        # Check if email is already taken
        existing_user = await UserService.get_by_email(db, email=email)
        if existing_user:
            raise UserAlreadyExistsError(email)

        db_user = User(
            email=email,
            hashed_password=hashed_password,
            full_name=full_name,
        )
        db.add(db_user)
        await db.commit()
        await db.refresh(db_user)
        return db_user
