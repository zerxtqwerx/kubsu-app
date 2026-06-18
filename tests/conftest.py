import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from src.main import app
from src.models import User
from src.database import Base

DATABASE_URL = "postgresql+asyncpg://kubsu:kubsu@127.0.0.1:5432/kubsu"

engine = create_async_engine(DATABASE_URL, echo=True)
AsyncSessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)


@pytest.fixture(scope="session")
def event_loop():
    import asyncio
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="session")
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@pytest_asyncio.fixture(scope='function')
async def db_session(init_db):
    async with AsyncSessionLocal() as session:
        yield session
        await session.rollback()


@pytest_asyncio.fixture(autouse=True)
async def test_client():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        yield client


@pytest_asyncio.fixture(autouse=True)
async def clear_table(db_session: AsyncSession):
    await db_session.execute(text("TRUNCATE users RESTART IDENTITY CASCADE;"))
    await db_session.commit()


@pytest_asyncio.fixture
async def user(db_session: AsyncSession) -> User:
    user = User(name="John Doe")
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)
    return user
