from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class FreelancerEarnings(Base):
    """
    Модель данных для таблицы freelancer_earnings_bd.
    """
    __tablename__ = "freelancer_earnings_bd"

    Freelancer_ID = Column(Integer, primary_key=True, index=True)
    Job_Category = Column(String)
    Platform = Column(String)
    Experience_Level = Column(String)
    Client_Region = Column(String)
    Payment_Method = Column(String)
    Job_Completed = Column(Integer)
    Earnings_USD = Column(Float)
    Hourly_Rate = Column(Float)
    Job_Success_Rate = Column(Float)
    Client_Rating = Column(Float)
    Job_Duration_Days = Column(Integer)
    Project_Type = Column(String)
    Rehire_Rate = Column(Float)
    Marketing_Spend = Column(Float)
