from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from models import Base, SoccerTeam  # Import the Base and the SoccerTeam model

# Load environment variables
load_dotenv()

DATABASE_URL = os.getenv("GABS_DATABASE_URL")
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)


def init_db():
    Base.metadata.create_all(engine)


def load_initial_data(session, data):
    for row in data:
        print("Row to be added: {0}".format(row))
        team = SoccerTeam(
            name=row['name'],
            country=row['country'],
            city=row['city'],
            foundation=row['foundation'],
            stadium=row['stadium']
        )
        session.add(team)
    session.commit()
