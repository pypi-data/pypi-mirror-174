from loguru import logger
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from ..utils import sqlite

sqlite_engine = create_async_engine("sqlite+aiosqlite:///homesolar.db", echo=False)
sqlite_session = sessionmaker(bind=sqlite_engine, expire_on_commit=False, class_=AsyncSession)


async def reinitialize_tables():
    async with sqlite_engine.begin() as conn:
        await conn.run_sync(sqlite.Base.metadata.drop_all)
        await conn.run_sync(sqlite.Base.metadata.create_all)


async def write(data):
    try:
        async with sqlite_session() as session:
            async with session.begin():

                if type(data) is list:
                    for stmt in data:
                        await session.execute(stmt)
                else:
                    await session.execute(data)
            await session.commit()
            await session.close()

        logger.info("Data saved successfully!")
    except Exception as e:
        logger.exception(f"Data not saved! [{e}]")


async def execute(statement):
    result = None
    try:
        async with sqlite_session() as session:
            async with session.begin():
                result = await session.execute(statement)
            await session.commit()
            await session.close()
    except Exception as e:
        logger.exception(f"Something went wrong when executing an sql! [{e}]")
    finally:
        return result
