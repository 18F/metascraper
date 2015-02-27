# metascraper
scrapers to create iso metadata

This is a set of http://scrapy.org/ code to scrape existing NOAA websites, and create json data files that can be used to populate templates for making ISO metadata.  

There is also a template program that read the output json and creates metadata files using a template in this system:
http://jinja.pocoo.org/docs/dev/templates/

This is a work in progress.


install pieces:
pip install Jinja2
pip install Scrapy
