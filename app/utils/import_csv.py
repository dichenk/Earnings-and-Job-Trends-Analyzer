import pandas as pd
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.models.freelancer import Base, FreelancerEarnings
from app.core.config import settings


CSV_PATH = settings.csv_path
DATABASE_URL = settings.database_url

engine = create_async_engine(DATABASE_URL, echo=True, future=True)
SessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def main():
    """
    Импортирует данные из CSV-файла в базу данных.
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    df = pd.read_csv(CSV_PATH)
    async with SessionLocal() as session:
        for _, row in df.iterrows():
            freelancer = FreelancerEarnings(**row.to_dict())
            session.add(freelancer)
        await session.commit()
    print("Импорт завершён!")

if __name__ == "__main__":
    asyncio.run(main())
