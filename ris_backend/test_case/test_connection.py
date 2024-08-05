# This file sets up the database
import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from app.models import StaffRole

# Load environment variables from .env file
load_dotenv()
DB_URL = os.getenv("DB_URL")

# Setup database engine and session
engine = create_engine(DB_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def test_connection():
    session = SessionLocal()
    try:
        # Query to check the connection
        roles = session.query(StaffRole).all()
        for role in roles:
            print(f"Role ID: {role.role_id}, Role Name: {role.role_name}")
        print("Connection successful!")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        session.close()


if __name__ == "__main__":
    test_connection()
