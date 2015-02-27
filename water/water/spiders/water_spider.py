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
            item['title2'] = title
            item['url'] = ''.join(sel.xpath('@href').extract())
            url = urlparse.urljoin(response.url, item['url'])
            item['url'] = url
            item['title'] = ''.join(sel.xpath('text()').extract())
            item['desc'] = ''.join(sel.xpath('following::li[1]/span/text()').extract())
            # create a key so we can later match up the KML and shapefiles
            # Shapefile (Maximum Forecast 1-Day)
            print "AJS=[",title,"]"
            keypart = re.match('(.*) .*\((.*)\)',item['title'])
            if keypart:
               print keypart.group(1),"|",keypart.group(2)
               item['type']=keypart.group(1)
               item['key']=keypart.group(2)

            yield item


