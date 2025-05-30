from sqlalchemy.exc import SQLAlchemyError
from app.core.database import AsyncSessionLocal
from sqlalchemy import text


DANGEROUS_WORDS = ["drop", "delete", "update", "insert", "alter"]


async def check_sql_valid(sql: str) -> bool:
    """
    Выполняет SQL-запрос и возвращает True, если он валиден
    и выполняется без ошибок.
    Никакие данные не изменяются (только SELECT).
    """
    sql = sql.strip().lower()
    if not sql.strip().lower().startswith("select"):
        return False
    if any(word in sql.lower() for word in DANGEROUS_WORDS):
        return False
    try:
        async with AsyncSessionLocal() as session:
            result = await session.execute(text(sql))
            _ = result.fetchone()
        return True
    except SQLAlchemyError as e:
        return False
