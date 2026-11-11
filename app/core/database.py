from collections.abc import AsyncGenerator

from config import settings
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlmodel.ext.asyncio.session import AsyncSession

# Create the async database engine
engine = create_async_engine(
    str(settings.DATABASE_URL),
    echo=False,
    future=True,
)

# Create the async session factory
async_session_maker = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session