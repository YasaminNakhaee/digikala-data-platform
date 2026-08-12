from src.db.database import engine
from src.db.models import Base

def create_database_tables():
    Base.metadata.create_all(bind=engine)
    print("successfully")

if __name__ == "__main__" :
    create_database_tables()