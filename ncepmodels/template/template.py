from jinja2 import Template
import json


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

   print record 
   #
   # Load the isorecord.xml template from the templates directory
   #
   template = env.get_template('isorecord.xml')
   # render the template with record as the variables for the template
   output = template.render(**record)

   # write the output to a new ISO record in the waf directory
   outputfile = open('waf/NCDC'+str(i)+'.xml',"w")
   outputfile.write(output)
   outputfile.close()



