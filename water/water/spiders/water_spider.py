import scrapy
import urlparse
import re

from water.items import WaterItem

class WaterSpider(scrapy.Spider):
    name = "water"
    allowed_domains = ["water.weather.gov"]
    start_urls = ["http://water.weather.gov/ahps/download.php"]



    def parse(self,response):
      print "inside parse"
      #for sel in response.xpath("//h4[@class='download_subtitles']/following::ul/li[@class='download_list_item']"):
      for sel in response.xpath("//h4[@class='download_subtitles']/following::a"):
         # once we have the a - we want the href, and the text, and the description
        print "one"
        title = ''.join(sel.xpath('@title').extract())
        if title:
            item = WaterItem()
            item['title'] = title
            item['url'] = ''.join(sel.xpath('@href').extract())
            item['title2'] = ''.join(sel.xpath('text()').extract())
            item['desc'] = ''.join(sel.xpath('following::li[1]/span/text()').extract())
            yield item


