# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from database.config import DATABASE_URI
from database.models import Base, Amazon_Product, Category
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql.expression import null
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from pytz import timezone
from decimal import Decimal
from pickle import dumps

engine = create_engine(DATABASE_URI)
Session = sessionmaker(bind=engine)

from contextlib import contextmanager
@contextmanager
def session_scope():
    session = Session()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()

def value_if_not_na(value):
    if value == "N/A":
        return null()
    else:
        return value

class AmazonScraperPipeline(object):
    def __init__(self):
        pass
    def process_item(self, item, spider):
        # item.setdefault("", "N/A")
        # item.setdefault("", "N/A")

        with session_scope() as s:
            product = Amazon_Product(name=item["name"],
                                    price=value_if_not_na(item["price"]),
                                    seller_name=value_if_not_na(item["seller_name"]),
                                    seller_rating=value_if_not_na(item["seller_rating"]),
                                    num_seller_ratings=value_if_not_na(item["num_seller_ratings"]),
                                    stars=value_if_not_na(item["stars"]),
                                    num_reviews=value_if_not_na(item["num_reviews"]),
                                    amazon_choice=value_if_not_na(item["amazon_choice"]),
                                    answered_qs=value_if_not_na(item["answered_qs"]),
                                    availibility=value_if_not_na(item["availibility"]),
                                    time=value_if_not_na(item["time"]),
                                    more_product_links=dumps((item["more_product_links"])),
                                    lightning_deal=value_if_not_na(item["lightning_deal"]),
                                    deal_price=value_if_not_na(item["deal_price"]),
                                    ASIN=value_if_not_na(item["ASIN"]),
                                    brand=value_if_not_na(item["brand"]),
                                    return_policy=value_if_not_na(item["return_policy"]),
                                    warranty=value_if_not_na(item["warranty"]),
                                    pay_on_delivery=value_if_not_na(item["pay_on_delivery"]),
                                    amazon_delivered=value_if_not_na(item["amazon_delivered"]),
                                    cart_count=value_if_not_na(item["cart_count"]),
                                    features=value_if_not_na(item["features"]),
                                    num_offers=value_if_not_na(item["num_offers"]),
                                    lowest_price=value_if_not_na(item["lowest_price"]),
                                    weight=value_if_not_na(item["weight"]),
                                    model=value_if_not_na(item["model"]),
                                    url=value_if_not_na(item["url"]),)
            for category in item["categories"]:
                temp = s.query(Category).filter(Category.name==category).first()
                if temp is None:
                    temp = Category(name=category)
                    s.add(temp)
                product.categories.append(temp)
            s.add(product)
            s.commit()
        return item
