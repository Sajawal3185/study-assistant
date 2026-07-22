db_url = "postgresql://postgres:3185sajawal@localhost:5432/postgres"

from sqlalchemy import create_engine
engine = create_engine(db_url)

from sqlalchemy.orm import declarative_base
base = declarative_base()
