# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class NcepmodelsItem(scrapy.Item):
    # define the fields for your item here like:
    modeldesclink = scrapy.Field()
    modeldesc = scrapy.Field()
    update = scrapy.Field()
    grib = scrapy.Field()
    http = scrapy.Field()
    opendap  = scrapy.Field()
    docurl = scrapy.Field()
    title = scrapy.Field()
    minlon = scrapy.Field()
    maxlon = scrapy.Field()
    minlat = scrapy.Field()
    maxlat = scrapy.Field()
    latresolution= scrapy.Field()
    lonresolution= scrapy.Field()
    maxalt = scrapy.Field()
    minalt = scrapy.Field()
    pass
