from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession, AsyncEngine, create_async_engine
from settings import pg_settings


engine: AsyncEngine = create_async_engine(pg_settings.get_url('psycopg'))
session_maker: async_sessionmaker[AsyncSession] = async_sessionmaker(engine)


def get_engine():
    return engine


def get_session_maker():
    return session_maker


def make_session():
    return get_session_maker()()
