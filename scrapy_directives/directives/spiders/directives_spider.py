import scrapy
import urlparse
from directives.items import DirectiveItem

class  DirectivesSpider(scrapy.Spider):
   name = "directives"
   allowed_domains = ["products.weather.gov"]
   start_urls = []

   for n in range(0, 19):
    start_urls.append("http://products.weather.gov/viewlist.php?page="+str(n))

   def parse(self,response):
     #for sel in response.xpath('//table[3]/tr/td[1]/a/@href').extract()
     for sel in response.xpath('//table[3]/tr'):
       pagelink = sel.xpath('td[1]/a/@href').extract()
       print pagelink
       if len(pagelink) and isinstance(pagelink[0], basestring):
         item = DirectiveItem()
         item['pagelink'] = sel.xpath('td[1]/a/@href').extract()
         item['title']= sel.xpath('td[1]/a/text()').extract()
         item['desc']= sel.xpath('td[2]/text()').extract()
         item['pdflink'] = sel.xpath('td[3]/a/@href').extract()
         yield item
         print item['title'],item['pagelink'],item['desc'], item['pdflink']
      
         url = urlparse.urljoin(response.url, pagelink[0])
         print url
         yield scrapy.Request(url,callback=self.parse_page,meta={'item': item})

   def parse_page(self,response):
       pagelink = response.xpath('td[1]/a/@href').extract()
       item = response.meta['item']
       print "parse_page"
       return item
