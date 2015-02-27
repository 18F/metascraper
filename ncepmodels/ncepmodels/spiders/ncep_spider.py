import scrapy
import urlparse
import re

from ncepmodels.items import NcepmodelsItem

class NCEPSpider(scrapy.Spider):
    name = "ncep"
    allowed_domains = ["nomads.ncep.noaa.gov"]
    start_urls = ["http://nomads.ncep.noaa.gov/"]

    def parse(self,response):
      print "inside parse"
      for sel in response.xpath('//table[9]/trbody/tr'):
       modeldesclink = sel.xpath('td[1]/a/@href').extract()
       print modeldesclink 
       if len(modeldesclink) and isinstance(modeldesclink[0], basestring):
         item = NcepmodelsItem()
         item['modeldesclink'] = ''.join(sel.xpath('td[1]/a/@href').extract())
         item['title']=''.join(sel.xpath('td[1]/a/text()').extract())
         updatearray = sel.xpath('td[2]/text()').extract()
         if len(updatearray) and isinstance(updatearray[0], basestring):
           item['update'] = updatearray[0].strip()
         item['grib'] = ''.join(sel.xpath('td[3]/a/@href').extract())
         item['http'] = ''.join(sel.xpath('td[4]/a/@href').extract())
         item['opendap'] = ''.join(sel.xpath('td[5]/a/@href').extract())
         print item['modeldesclink'], item['title'], item['grib'], item['http'], item['opendap']
         url = urlparse.urljoin(response.url, item['modeldesclink'])
         print url
         request = scrapy.Request(url,callback=self.parse_desc,meta={'item': item})
         yield request

    def parse_desc(self,response):
       print "parse_page"
       item = response.meta['item']
       item['modeldesc']  = ''.join(response.xpath("string(//table[7]/tbody/tr/td[1])").extract())
       print item['modeldesc']
       request = None
       if item['opendap'] and isinstance(item['opendap'], basestring):
         opendapurl = urlparse.urljoin("http://nomads.ncep.noaa.gov/", item['opendap'])
         print opendapurl
         request = scrapy.Request(opendapurl,callback=self.parse_opendap,meta={'item': item})
       yield request

    def parse_opendap(self,response):
       print "parse_opendap"
       request = None
       item = response.meta['item']
       nexturla = response.xpath("//a[6]/@href").extract()
       if len(nexturla) and isinstance(nexturla[0], basestring):
         nexturl= urlparse.urljoin(response.url, nexturla[0])
         print nexturl
         request = scrapy.Request(nexturl,callback=self.parse_opendap2,meta={'item': item})
       yield request

    def parse_opendap2(self,response):
       print "parse_opendap2"
       request = None
       item = response.meta['item']
       #nexturla = response.xpath("//a[6]/@href").extract()
       nexturla = response.xpath("//a[contains(., 'info')]/@href").extract()
       if len(nexturla) and isinstance(nexturla[0], basestring):
         nexturl= urlparse.urljoin(response.url, nexturla[0])
         print nexturl
         request = scrapy.Request(nexturl,callback=self.parse_opendap3,meta={'item': item})
       yield request

    def parse_opendap3(self,response):
       print "parse_opendap3"
       item = response.meta['item']
       lonstring = response.xpath("normalize-space(//tr[td/b[contains(.,'Longitude:')]]/td[position()>1])").extract()
       latstring = response.xpath("normalize-space(//tr[td/b[contains(.,'Latitude:')]]/td[position()>1])").extract()
       latresolution = response.xpath("normalize-space(//tr[td/b[contains(.,'Latitude:')]]/td[position()>2])").extract()
       lonresolution = response.xpath("normalize-space(//tr[td/b[contains(.,'Longitude:')]]/td[position()>2])").extract()
       # [u'-152.85510700000\xb0E to -49.68011411610\xb0E'] [u'12.28939100000\xb0N to 61.05139100000\xb0N']
       lonarray = re.match('(.*).. to (.*)..',lonstring[0])
       latarray = re.match('(.*).. to (.*)..',latstring[0])
       print latresolution,lonresolution
       print lonstring,latstring
       print lonarray.group(1),"|",lonarray.group(2),"|",latarray.group(1),latarray.group(2)
       item['minlat']=latarray.group(1)
       item['maxlat']=latarray.group(2)
       item['minlon']=lonarray.group(1)
       item['maxlon']=lonarray.group(2)
       # resolution
       # [u'\xa0(707 points, avg. res. 0.046\xb0)'] [u'\xa0(1407 points, avg. res. 0.049\xb0)']
       latr = re.match('.*res. *(.*).\)',latresolution[0])
       lonr = re.match('.*res. *(.*).\)',lonresolution[0])
       item['latresolution']=latr.group(1)
       item['lonresolution']=lonr.group(1)
       return item

