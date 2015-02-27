from jinja2 import Template
import json
from datetime import date
import codecs


#
# Load the jinja templating system, and initialize the templates directory
#
from jinja2 import Environment, PackageLoader
env = Environment(loader=PackageLoader('module', 'templates'))

#
# read in the scraped json records
#
json_data=open('../ncepmodels/items.json')
data = json.load(json_data)
json_data.close()


#
# we might want to make some extras, like thumbnails, etc to include automatically
# load them here
#
extras_json=open('extras.json')
extras = json.load(extras_json)
extras_json.close()

#
# loop through each entry in the scraped json file
#
for (i, record) in enumerate(data):
   #
   # attach the correct extra entry with the scraped record
   # store it in extras.xxx (ie: extras.thumbnail )
   #
   # we are matching on title
   #
   for item in extras:
     print record['title'],item['title']
     if item['title'] == record['title']:
       print "match"
       record['extras']=item


   record['docid']='gov.noaa.ncep:NOMADS'+str(i)
   record['doctitle']='NOMADS'+str(i)
   record['date']=date.today().isoformat()
   record['nomadsurl']="http://nomads.ncep.noaa.gov/"
   record['nomadsurltitle']="NOAA Operational Model Archive and Distribution System - NOMADS at NCEP"

   if not 'minlat' in record:
     print "AJS"
     record['minlat'] = "-90"
     record['maxlat'] = "90"
     record['minlon'] = "0"
     record['maxlon'] = "359.5"
     record['resolution'] = "maybe 1 degree"

   print record['date']
   print record 
   #
   # Load the isorecord.xml template from the templates directory
   #
   template = env.get_template('isorecord.xml')
   # render the template with record as the variables for the template
   output = template.render(**record)

   # write the output to a new ISO record in the waf directory
   outputfile = codecs.open('waf/'+record['doctitle']+'.xml',"w","UTF-8")
   outputfile.write(output)
   outputfile.close()



