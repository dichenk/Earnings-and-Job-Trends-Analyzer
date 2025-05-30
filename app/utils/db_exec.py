from sqlalchemy.exc import SQLAlchemyError
from app.core.database import AsyncSessionLocal
from sqlalchemy import text


async def exec_sql_and_print(sql: str):
    """
    Выполняет SQL-запрос и возвращает результат.
    """
    async with AsyncSessionLocal() as session:
        try:
            result = await session.execute(text(sql))
            rows = result.fetchall()
            columns = result.keys()
            if not rows:
                return
            return rows
        except SQLAlchemyError as e:
            return str(e)
