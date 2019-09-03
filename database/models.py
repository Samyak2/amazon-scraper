from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date, DateTime, Numeric, PickleType, ForeignKey
from sqlalchemy.dialects.postgresql import MONEY
from sqlalchemy.orm import relationship
from sqlalchemy.schema import Table

Base = declarative_base()

association_table = Table('association', Base.metadata,
    Column('product_id', Integer, ForeignKey('amazon_products.id')),
    Column('category_id', Integer, ForeignKey('category.id'))
)

class Amazon_Product(Base):
    __tablename__ = "amazon_products"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    price = Column(Numeric)
    seller_name = Column(String)
    seller_rating = Column(Numeric)
    num_seller_ratings = Column(Integer)
    stars = Column(Numeric)
    num_reviews = Column(Integer)
    amazon_choice = Column(Integer)
    answered_qs = Column(String)
    availibility = Column(String)
    categories = relationship("Category", secondary=association_table, back_populates="products", cascade="all,delete",)
    more_product_links = Column(PickleType)
    time = Column(DateTime(timezone=True))

class Category(Base):
    __tablename__ = "category"
    id = Column(Integer, primary_key = True)
    name = Column(String, unique=True)
    products = relationship("Amazon_Product", secondary=association_table, back_populates="categories")

# class Link(Base):
#     __tablename__ = 'link'
#     product_id = Column(
#         Integer,
#         ForeignKey('amazon_products.id'),
#         primary_key = True)
#     category_id = Column(
#         Integer,
#         ForeignKey('category.id'),
#         primary_key = True)