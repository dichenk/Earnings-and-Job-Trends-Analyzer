import pandas as pd
from sqlalchemy.ext.asyncio import create_async_engine
from app.models.freelancer import Base, FreelancerEarnings

DATABASE_URL = "sqlite+aiosqlite:///./test.db"
engine = create_async_engine(DATABASE_URL, echo=True, future=True)


async def init_db():
    """
    Инициализирует базу данных и загружает данные из CSV-файла.
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    df = pd.read_csv("./data/freelancer_earnings_bd.csv")
    async with engine.begin() as conn:
        for _, row in df.iterrows():
            f = FreelancerEarnings(**row.to_dict())
            await conn.merge(f)


import asyncio
if __name__ == "__main__":
    asyncio.run(init_db())
