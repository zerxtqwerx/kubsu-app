import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import AsyncSessionLocal, init_db as create_tables
from src.main import app
from src.models import User


@pytest_asyncio.fixture(scope="session")
async def init_db() -> None:
    await create_tables()


@pytest_asyncio.fixture(scope='function')
async def db_session() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session
        await session.rollback()


@pytest_asyncio.fixture(autouse=True)
async def test_client():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        yield client


@pytest_asyncio.fixture(autouse=True)
async def clear_table(init_db, db_session: AsyncSession) -> None:
    await db_session.execute(text("TRUNCATE users;"))
    await db_session.commit()


@pytest_asyncio.fixture
async def user(db_session: AsyncSession) -> User:
    user = User(name="John Doe")
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)
    return user
