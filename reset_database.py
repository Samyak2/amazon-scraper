from sqlalchemy import create_engine
from database.config import DATABASE_URI
from database.models import Base, Amazon_Product, Category
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from pytz import timezone
from decimal import Decimal
from pickle import dumps
from sqlalchemy.sql.expression import null

india = timezone("Asia/Kolkata")

engine = create_engine(DATABASE_URI)
Session = sessionmaker(bind=engine)

def recreate_database():
    Base.metadata.drop_all(engine)
    # for table in reversed(Base.metadata.sorted_tables):
    #     table.drop(engine)
    # Category.drop(engine)
    # Amazon_Product(engine)
    Base.metadata.create_all(engine)

recreate_database()