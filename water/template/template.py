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
json_data=open('../water/items.json')
data = json.load(json_data)
json_data.close()


#
# reindex the products by type
#
records = {}
for (i, record) in enumerate(data):
  if 'key' in record:
    key = record['key']
    if not key in records:
       records[key] = {}

    records[key][record['type']] = record
  

#print records



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
for key in records:
   #
   # attach the correct extra entry with the scraped record
   # store it in extras.xxx (ie: extras.thumbnail )
   #
   # we are matching on title
   #
   for item in extras:
     print key,item['key']
     if item['key'] == key:
       print "match"
       records[key]['extras']=extras

   record = records[key]
   record['date']=date.today().isoformat()
   record['mainurl']="water.weather.gov"
   record['mainurltitle']="NOAA - National Weather Service - Water"

   #if not 'minlat' in record:
   #  print "AJS"
   #  record['minlat'] = "-90"
   #  record['maxlat'] = "90"
   #  record['minlon'] = "0"
   #  record['maxlon'] = "359.5"
   #  record['resolution'] = "maybe 1 degree"

   #print record['date']
   #print record 


   #
   # Load the isorecord.xml template from the templates directory
   #
   template = env.get_template('isorecord.xml')
   # render the template with record as the variables for the template

   print record

   if record['KMZ']['urlkey']:
      record['docid']='gov.weather.water:AHPS'+record['KMZ']['urlkey']
      record['doctitle']='AHPS'+record['KMZ']['urlkey']
      output = template.render(data=record)
      # write the output to a new ISO record in the waf directory
      outputfile = codecs.open('waf/AHPS'+record['KMZ']['urlkey']+'.xml',"w","UTF-8")
      #outputfile = codecs.open('waf/test.xml',"w","UTF-8")
      outputfile.write(output)
      outputfile.close()
   else:
      print "NO URL KEY"



