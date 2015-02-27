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
      # the 9'th table is the one we want, iterate through each row (tr)
      for sel in response.xpath('//table[9]/trbody/tr'):
        print "one"
        yield self.parse_one_row(response,sel,0)

      # there is a missing <tr> tag in one of the tables, pull in the element
      for sel in response.xpath('//table[9]/trbody/td/..'):
        print "two"
        yield self.parse_one_row(response,sel,0)
        print "three"
        yield self.parse_one_row(response,sel,5)

    def parse_one_row(self,response,sel,offset):
      # the description link is in the 1st td inside the a, sometimes there is a font tag around it, do an or
      tdnum = str(offset+1)
      modeldesclink = sel.xpath('td['+tdnum+']/a/@href|td['+tdnum+']/font/a/@href').extract()
      print modeldesclink 
      # if we have a link - then we have an item. create an element (we want to ignore titles)
      if len(modeldesclink) and isinstance(modeldesclink[0], basestring):
         item = NcepmodelsItem()
         item['modeldesclink'] = ''.join(modeldesclink)
         item['title']=''.join(sel.xpath('td['+tdnum+']/a/text()|td['+tdnum+']/font/a/text()').extract())
         tdnum = str(offset+2)
         updatearray = sel.xpath('td['+tdnum+']/text()').extract()
         if len(updatearray) and isinstance(updatearray[0], basestring):
           item['update'] = updatearray[0].strip()
         tdnum = str(offset+3)
         item['grib'] = ''.join(sel.xpath('td['+tdnum+']/a/@href').extract())
         tdnum = str(offset+4)
         item['http'] = ''.join(sel.xpath('td['+tdnum+']/a/@href').extract())
         tdnum = str(offset+5)
         item['opendap'] = ''.join(sel.xpath('td['+tdnum+']/a/@href').extract())
         print item['modeldesclink'], item['title'], item['grib'], item['http'], item['opendap']
         url = urlparse.urljoin(response.url, item['modeldesclink'])
         print url
         request = scrapy.Request(url,callback=self.parse_desc,meta={'item': item},dont_filter=True)
         return request


    def parse_desc(self,response):
       print "parse_page"
       item = response.meta['item']
       # this one leaves the first line that we don't want:
       item['modeldesc']  = ''.join(response.xpath("string(//table[7]/tbody/tr/td[1])").extract())
       # this one doesn't do anything good with the html
       #item['modeldesc']  = ''.join(response.xpath("//table[7]/tbody/tr/td[1]/p/text()").extract())
       #print item['modeldesc']
       request = item
       if item['opendap'] and isinstance(item['opendap'], basestring):
         opendapurl = urlparse.urljoin("http://nomads.ncep.noaa.gov/", item['opendap'])
         print "AJS",opendapurl
         request = scrapy.Request(opendapurl,callback=self.parse_opendap,meta={'item': item},dont_filter=True)
       yield request

    def parse_opendap(self,response):
       print "parse_opendap1"
       request = None
       item = response.meta['item']
       #nexturla = response.xpath("//a[6]/@href").extract()
       nexturla = response.xpath("//a[.='dir']/@href").extract()
       if len(nexturla) and isinstance(nexturla[0], basestring):
         nexturl= urlparse.urljoin(response.url, nexturla[0])
         print "AJS1",nexturl,"|",response.url
         request = scrapy.Request(nexturl,callback=self.parse_opendap2,meta={'item': item},dont_filter=True)
       yield request

    def parse_opendap2(self,response):
       print "parse_opendap2"
       request = None
       item = response.meta['item']
       #nexturla = response.xpath("//a[6]/@href").extract()
       nexturla = response.xpath("//a[.='info']/@href").extract()
       print "AJS2",nexturla
       if len(nexturla) and isinstance(nexturla[0], basestring):
         nexturl= urlparse.urljoin(response.url, nexturla[0])
         print "AJS2b",nexturl
         request = scrapy.Request(nexturl,callback=self.parse_opendap3,meta={'item': item},dont_filter=True)
       yield request

    def parse_opendap3(self,response):
       print "parse_opendap3"
       item = response.meta['item']
       altitudestring = response.xpath("normalize-space(//tr[td/b[contains(.,'Altitude:')]]/td[position()>1])").extract()
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
       altitude = re.match('(.*).. to (.*)..',altitudestring[0])
       if altitude is not None:
         item['maxalt']=altitude.group(1)
         item['minalt']=altitude.group(2)
       # resolution
       # [u'\xa0(707 points, avg. res. 0.046\xb0)'] [u'\xa0(1407 points, avg. res. 0.049\xb0)']
       latr = re.match('.*res. *(.*).\)',latresolution[0])
       lonr = re.match('.*res. *(.*).\)',lonresolution[0])
       item['latresolution']=latr.group(1)
       item['lonresolution']=lonr.group(1)
       return item

