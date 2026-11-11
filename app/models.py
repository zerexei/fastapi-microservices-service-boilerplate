from datetime import UTC, datetime

from sqlmodel import Field, SQLModel


class UserBase(SQLModel):
  email: str = Field(unique=True, index=True, max_length=255)
  full_name: str | None = Field(default=None, max_length=255)
  is_active: bool = Field(default=True)
  is_superuser: bool = Field(default=False)


class User(UserBase, table=True):
  __tablename__ = "users"

  id: int | None = Field(default=None, primary_key=True)
  hashed_password: str = Field(nullable=False)
  created_at: datetime = Field(
      default_factory=lambda: datetime.now(UTC), nullable=False
  )