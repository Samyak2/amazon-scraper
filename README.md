## Archived: This project is not being maintained anymore

[![No Maintenance Intended](http://unmaintained.tech/badge.svg)](http://unmaintained.tech/)

# Amazon India Scraper

## Description

A web scraper made specifically to extract data from product pages at [Amazon India](https://www.amazon.in/).
This is implemented using the Scrapy module in python.
The data collected using this scraper was used in [this project](https://github.com/Samyak2/amazon-analysis)

## Instructions to run


 - Clone this repository
 - Create a virtual environment (optional)
 - Install the python requirements using `pip install -r requirements.txt`
 - Set up a Postgres Database (or host it on Heroku and enable the Postgres add-on)
 - Add the links of products you want to scrape to `links.txt` (make sure there is a newline after the last link)
 - Add your email to the `USER_AGENT` in [settings.py](amazon_scraper/settings.py)
 - Add the URI to your Postgres Database as a `DATABASE_URL` environment variable, or create a file named `.env` and add it there in the following format
 
     `postgres://<USERNAME>:<PASSWORD>@<IP_ADDRESS>:<PORT>/<DATABASE_NAME>`
 - To run the scraper, use
 
    `cd amazon-scraper`
    
    `scrapy runspider amazon_spider`

## Technologies Used

 - Python 3
 - Scrapy
 - PostgreSQL
 - Heroku
 - XPath
 
