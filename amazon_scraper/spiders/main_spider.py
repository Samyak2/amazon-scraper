import scrapy
from amazon_scraper.items import AmazonProduct
from datetime import datetime
from pytz import timezone
from decimal import Decimal

india = timezone("Asia/Kolkata")

def if_available_strip(resp):
    if resp!=[]:
        return resp[0].strip()
    else:
        return "N/A"

class AmazonSpider(scrapy.Spider):
    name = "amazon_spider" #spider name
    # handle_httpstatus_list = [503]
    start_urls = ["https://www.amazon.in/gp/product/B07HGJKDQB/", "https://www.amazon.in/dp/B07SBK2BK7", "https://www.amazon.in/dp/B07RP8WGZJ", "https://www.amazon.in/dp/B07L57BMBR", "https://www.amazon.in/dp/B07MSKN6CS", "https://www.amazon.in/dp/B07C4YKR3J", "https://www.amazon.in/dp/B06X92RN9D", "https://www.amazon.in/dp/B01BMJ0Y76", "https://www.amazon.in/dp/B07989JYRS"]
    
    def parse(self, response):
        product = AmazonProduct()
        product["url"] = response.url
        product["name"] = response.xpath('//*[@id="productTitle"]/text()').extract()[0].strip()
        price = response.xpath('//*[@id="priceblock_ourprice"]/text()').extract()#[0].strip()[2:]
        if price != []:
            price = price[0].strip()[2:]
            product["price"] = Decimal("".join(i for i in price if i.isdigit() or i=="."))
            product["seller_name"] = response.xpath('//*[@id="sellerProfileTriggerId"]/text()').extract()[0]
            product["seller_rating"] = float(response.xpath('//*[@id="merchant-info"]/text()').extract()[1].strip()[1:4])
            tmp = response.xpath('//*[@id="merchant-info"]/text()').extract()[2].strip()
            product["num_seller_ratings"] = int("".join(i for i in tmp if i.isdigit()))#tmp[:tmp.index(")")]
        else:
            product["price"] = "N/A"
            product["seller_name"] = "N/A"
            product["seller_rating"] = "N/A"
            product["num_seller_ratings"] = "N/A"
        product["stars"] = response.xpath('//div[@id="averageCustomerReviews"]//span[@class="a-icon-alt"]/text()').extract()#[0][:3])
        if product["stars"] == []:
            product["stars"] = "N/A"
        else:
            product["stars"] = float(product["stars"][0][:3])
        product["num_reviews"] = if_available_strip(response.xpath('//*[@id="acrCustomerReviewText"]/text()').extract())#[0]
        if product["num_reviews"] != "N/A":
            product["num_reviews"] = int("".join(i for i in product["num_reviews"] if i.isdigit()))
        product["amazon_choice"] = len(response.xpath('//*[@id="acBadge_feature_div"]/*').extract())
        product["answered_qs"] = if_available_strip(response.xpath('//*[@id="askATFLink"]/span/text()').extract())#[0].strip()
        if product["answered_qs"] != "N/A":
            product["answered_qs"] = int("".join(i for i in product["answered_qs"] if i.isdigit()))
        product["availibility"] = if_available_strip(response.xpath('//*[@id="availability"]/span/text()').extract())#[0].strip()
        categories = response.xpath('//*[@id="showing-breadcrumbs_div"]//span[@class="a-list-item"]/a/text()').extract()
        product["categories"] = [i.strip() for i in categories]
        more_product_links = response.xpath('//a[contains(@href, "dp/")]/@href').extract()
        product["more_product_links"] =["https://www.amazon.in" + i[:i.index("ref")] for i in more_product_links]
        product["time"] = datetime.now(india)
        print("Name:", product["name"])
        print("Price:", product["price"])
        print("Rating:", product["stars"])
        print(product["num_reviews"])
        print(product["answered_qs"])
        print("Amazon's choice:", product["amazon_choice"])
        print("Seller:", product["seller_name"])
        print("Seller Rating:", product["seller_rating"])
        print("Number of seller ratings:", product["num_seller_ratings"])
        print("Availibility:", product["availibility"])
        print("Time:", product["time"])
        print("Categories:", product["categories"])
        print(product["more_product_links"])

        yield product