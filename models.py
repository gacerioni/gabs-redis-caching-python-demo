from dotenv import load_dotenv
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

Base = declarative_base()

# Load environment variables
load_dotenv()


class SoccerTeam(Base):
    __tablename__ = 'soccer_teams'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    country = Column(String, nullable=False)
    city = Column(String, nullable=False)
    foundation = Column(String, nullable=False)  # Stored as string for simplicity
    stadium = Column(String, nullable=False)


DATABASE_URL = os.getenv("DATABASE_URL")
print("DATABASE URL MODELS: {0}".format(DATABASE_URL))
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)


def init_db():
    Base.metadata.create_all(engine)
