from sqlalchemy import create_engine
from config import DATABASE_URI
from models import Base, Amazon_Product, Category
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

# s = Session()

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

recreate_database()

# with session_scope() as s:
#     time = datetime.now(india)
#     product = Amazon_Product(name="OnePlus 7 Pro (Nebula Blue, 12GB RAM, 256GB Storage)", price=null(), seller_name="Darshita Electronics", seller_rating=4.7, num_seller_ratings=21300, stars=4.6, num_reviews=6702, amazon_choice=2, answered_qs=1000, availibility="In stock.", time=time, 
#         more_product_links=dumps(['https://www.amazon.in/dp/B07FNPS51G/',
#                         'https://www.amazon.in/dp/B07HG8SBDV/',
#                         'https://www.amazon.in/dp/B07HGJK535/',
#                         'https://www.amazon.in/dp/B07HG8SBDV/',
#                         'https://www.amazon.in/dp/B07HG8SBDW/',
#                         'https://www.amazon.in/Ringke-Transparent-Protection-Absorption-Technology/dp/B07S2D7Q24/',
#                         'https://www.amazon.in/GEAR-NEXT-Ultrasonic-Fingerprint-Transparent/dp/B07STJFVWX/',
#                         'https://www.amazon.in/Ringke-Transparent-Protection-Absorption-Technology/dp/B07S2D7Q24/',
#                         'https://www.amazon.in/GEAR-NEXT-Ultrasonic-Fingerprint-Transparent/dp/B07STJFVWX/',
#                         'https://www.amazon.in/Test-Exclusive-611/dp/B07HGMLBW1/',
#                         'https://www.amazon.in/Test-Exclusive-611/dp/B07HGMLBW1/',
#                         'https://www.amazon.in/Test-Exclusive-608/dp/B07HGBMJT6/',
#                         'https://www.amazon.in/Test-Exclusive-608/dp/B07HGBMJT6/',
#                         'https://www.amazon.in/Test-Exclusive-609/dp/B07HGJFVL2/',
#                         'https://www.amazon.in/Test-Exclusive-609/dp/B07HGJFVL2/',
#                         'https://www.amazon.in/Test-Exclusive-610/dp/B07HGH3G46/',
#                         'https://www.amazon.in/Test-Exclusive-610/dp/B07HGH3G46/',
#                         'https://www.amazon.in/Apple-iPhone-XR-128GB-Black/dp/B07JG7DS1T/',
#                         'https://www.amazon.in/Apple-iPhone-XR-128GB-Black/dp/B07JG7DS1T/',
#                         'https://www.amazon.in/Ringke-Transparent-Protection-Absorption-Technology/dp/B07S2D7Q24/',
#                         'https://www.amazon.in/Ringke-Transparent-Protection-Absorption-Technology/dp/B07S2D7Q24/',
#                         'https://www.amazon.in/dp/B07HGMLBW1/',
#                         'https://www.amazon.in/dp/B077Q44DKY/',
#                         'https://www.amazon.in/dp/B07JG7DS1T/',
#                         'https://www.amazon.in/dp/B07PP2JD3V/',
#                         'https://www.amazon.in/GEAR-NEXT-Ultrasonic-Fingerprint-Transparent/dp/B07STJFVWX/',
#                         'https://www.amazon.in/GEAR-NEXT-Ultrasonic-Fingerprint-Transparent/dp/B07STJFVWX/',
#                         'https://www.amazon.in/Ringke-Transparent-Protection-Absorption-Technology/dp/B07S2D7Q24/',
#                         'https://www.amazon.in/Ringke-Transparent-Protection-Absorption-Technology/dp/B07S2D7Q24/',
#                         'https://www.amazon.in/Compatible-OnePlus-Protection-Enhanced-Kickstand/dp/B07RY67KWY/',
#                         'https://www.amazon.in/Compatible-OnePlus-Protection-Enhanced-Kickstand/dp/B07RY67KWY/',
#                         'https://www.amazon.in/TARKAN-Heavy-Shockproof-Kickstand-OnePlus/dp/B07S9CJC6G/',
#                         'https://www.amazon.in/TARKAN-Heavy-Shockproof-Kickstand-OnePlus/dp/B07S9CJC6G/',
#                         'https://www.amazon.in/Pirum-Flip-Cover-OnePlus-Pro/dp/B07PDMST9H/',
#                         'https://www.amazon.in/Pirum-Flip-Cover-OnePlus-Pro/dp/B07PDMST9H/',
#                         'https://www.amazon.in/Ringke-Transparent-Protection-Absorption-Technology/dp/B07Q6GZXZK/',
#                         'https://www.amazon.in/Ringke-Transparent-Protection-Absorption-Technology/dp/B07Q6GZXZK/']),
#     )
#     categories = ['Electronics',
#                 'Mobiles & Accessories',
#                 'Smartphones & Basic Mobiles',
#                 'Smartphones']
#     # count = 0
#     for category in categories:
#         # temp = Category(name=category)
#         # product.categories.append(temp)
#         # s.add(temp)
#         temp = s.query(Category).filter(Category.name==category).first()
#         if temp is None:
#             temp = Category(name=category)
#             s.add(temp)
#         product.categories.append(temp)
#     s.add(product)
#     s.commit()