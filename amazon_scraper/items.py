# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class AmazonProduct(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name = scrapy.Field()
    price = scrapy.Field()
    seller_name = scrapy.Field()
    seller_rating = scrapy.Field()
    num_seller_ratings = scrapy.Field()
    stars = scrapy.Field()
    num_reviews = scrapy.Field()
    amazon_choice = scrapy.Field()
    answered_qs = scrapy.Field()
    availibility = scrapy.Field()
    categories = scrapy.Field()
    more_product_links = scrapy.Field()
    time = scrapy.Field()
    url = scrapy.Field()
    lightning_deal = scrapy.Field()
    deal_price = scrapy.Field()
    ASIN = scrapy.Field()
    brand = scrapy.Field()
    return_policy = scrapy.Field()
    warranty = scrapy.Field()
    pay_on_delivery = scrapy.Field()
    amazon_delivered = scrapy.Field()
    cart_count = scrapy.Field()
    features = scrapy.Field()
    num_offers = scrapy.Field()
    lowest_price = scrapy.Field()
    weight = scrapy.Field()
    model = scrapy.Field()