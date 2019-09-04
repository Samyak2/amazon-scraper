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

def price_extract(price):
    if price == []:
        return "N/A"
    price = price[0].strip()[2:].split()[0]
    return Decimal("".join(i for i in price if i.isdigit() or i=="."))

class AmazonSpider(scrapy.Spider):
    name = "amazon_spider" #spider name
    # handle_httpstatus_list = [503]
    # start_urls = ["https://www.amazon.in/dp/B07SBK2BK7"]#, "https://www.amazon.in/dp/B07SBK2BK7", "https://www.amazon.in/dp/B07RP8WGZJ", "https://www.amazon.in/dp/B07L57BMBR", "https://www.amazon.in/dp/B07MSKN6CS", "https://www.amazon.in/dp/B07C4YKR3J", "https://www.amazon.in/dp/B06X92RN9D", "https://www.amazon.in/dp/B01BMJ0Y76", "https://www.amazon.in/dp/B07989JYRS"]
    with open("links.txt") as f:
        lines = f.readlines()
        start_urls = list(set(line[:-1] for line in lines if line!="\n"))

    def parse(self, response):
        # try:
            product = AmazonProduct()
            product["url"] = response.url
            product["name"] = if_available_strip(response.xpath('//*[@id="productTitle"]/text()').extract())
            if product["name"] != "N/A":
                price = response.xpath('//*[@id="priceblock_ourprice"]/text()').extract()#[0].strip()[2:]
                if price != []:
                    # price = price[0].strip()[2:]
                    product["price"] = price_extract(price) #Decimal("".join(i for i in price if i.isdigit() or i=="."))
                    product["seller_name"] = if_available_strip(response.xpath('//*[@id="sellerProfileTriggerId"]/text()').extract())
                    product["seller_rating"] = response.xpath('//*[@id="merchant-info"]/text()').extract()#[1].strip()[1:4])
                    if product["seller_rating"] != []:
                        product["seller_rating"] = float(product["seller_rating"][1].strip()[1:4])
                    else:
                        product["seller_rating"] = "N/A"
                    tmp = response.xpath('//*[@id="merchant-info"]/text()').extract()#[2].strip()
                    if tmp != []:
                        tmp = tmp[2].strip()
                        product["num_seller_ratings"] = int("".join(i for i in tmp if i.isdigit()))#tmp[:tmp.index(")")]
                    else:
                        product["num_seller_ratings"] = "N/A"
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
                more_product_links =["https://www.amazon.in" + i[:i.find("ref")] for i in more_product_links]
                product["more_product_links"] = more_product_links
                product["time"] = datetime.now(india)
                product["lightning_deal"] = "Lightning Deal" in if_available_strip(response.xpath('//*[@id="LDBuybox"]//span[@class="a-size-base gb-accordion-active"]/text()').extract())
                product["deal_price"] = price_extract(response.xpath('//*[@id="priceblock_dealprice"]/text()').extract())
                product["ASIN"] = if_available_strip(response.xpath('//*[@id="prodDetails"]//td[text()="ASIN"]/following::td[@class="value"][1]/text()').extract())
                product["brand"] = if_available_strip(response.xpath('//*[@id="prodDetails"]//td[text()="Brand"]/following::td[@class="value"][1]/text()').extract())
                product["return_policy"] = if_available_strip(response.xpath('//div[@data-name="RETURNS_POLICY"]//span[@class="a-size-small"]/text()').extract())
                product["warranty"] = if_available_strip(response.xpath('//div[@data-name="WARRANTY"]//span[@class="a-size-small"]/text()').extract())
                product["pay_on_delivery"] = if_available_strip(response.xpath('//div[@data-name="PAY_ON_DELIVERY"]//span[@class="a-size-small"]/text()').extract())
                product["amazon_delivered"] = if_available_strip(response.xpath('//div[@data-name="AMAZON_DELIVERED"]//span[@class="a-size-small"]/text()').extract())
                product["cart_count"] = int(if_available_strip(response.xpath('//*[@id="nav-cart-count"]/text()').extract()))
                features = response.xpath('//*[@id="feature-bullets"]/ul/li//text()').extract()
                product["features"] = "||".join(feature.strip() for feature in features)
                product["num_offers"] = if_available_strip(response.xpath('//*[@id="olp-sl-new"]/span[@class="olp-padding-right"]/a/text()').extract())
                product["lowest_price"] = price_extract(response.xpath('//*[@id="olp-sl-new"]//span[@class="a-color-price"]/text()').extract())
                product["weight"] = if_available_strip(response.xpath('//*[@id="prodDetails"]//td[contains(translate(text(),"WEIGHT","weight"),"weight")]/following::td[@class="value"][1]/text()').extract())
                product["model"] = if_available_strip(response.xpath('//*[@id="prodDetails"]//td[contains(text(),"Model")]/following::td[@class="value"][1]/text()').extract())
                # print("Name:", product["name"])
                # print("Price:", product["price"])
                # print("Rating:", product["stars"])
                # print(product["num_reviews"])
                # print(product["answered_qs"])
                # print("Amazon's choice:", product["amazon_choice"])
                # print("Seller:", product["seller_name"])
                # print("Seller Rating:", product["seller_rating"])
                # print("Number of seller ratings:", product["num_seller_ratings"])
                # print("Availibility:", product["availibility"])
                # print("Time:", product["time"])
                # print("Categories:", product["categories"])
                # print(product["more_product_links"])
                yield product
            else:
                yield scrapy.Request(response.url, callback=self.parse)
                # product["url"] = response.url
                # product["name"] = "N/A"
                # product["price"] = "N/A"
                # product["seller_name"] = "N/A"
                # product["seller_rating"] = "N/A"
                # product["num_seller_ratings"] = "N/A"
                # product["stars"] = "N/A"
                # product["num_reviews"] = "N/A"
                # product["amazon_choice"] = "N/A"
                # product["answered_qs"] = "N/A"
                # product["availibility"] = "N/A"
                # product["categories"] = []
                # product["more_product_links"] = "N/A"
                # product["time"] = "N/A"
                # product["lightning_deal"] = "N/A"
                # product["deal_price"] = "N/A"
                # product["ASIN"] = "N/A"
                # product["brand"] = "N/A"
                # product["return_policy"] = "N/A"
                # product["warranty"] = "N/A"
                # product["pay_on_delivery"] = "N/A"
                # product["amazon_delivered"] = "N/A"
                # product["cart_count"] = "N/A"
                # product["features"] = "N/A"
                # product["num_offers"] = "N/A"
                # product["lowest_price"] = "N/A"
                # product["weight"] = "N/A"
                # product["model"] = "N/A"
                # yield product
            #     more_product_links = response.xpath('//a[contains(@href, "dp/")]/@href').extract()
            #     more_product_links =["https://www.amazon.in" + i[:i.find("?pf_rd_p")] for i in more_product_links]
            #     with open("links.txt", "a") as f:
            #         for url in more_product_links:
            #             f.write(url+"\n")
            # for url in more_product_links[0:]:
            #     yield scrapy.Request(url, callback=self.parse)
        # except:
        #     with open("errorlinks.txt", "at") as f:
        #         f.write(response.url + "\n")