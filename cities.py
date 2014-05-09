'''
Grab the list of cities included in 
CIR's VA API
'''
import requests
import json
import csv

base_url="http://vetsapi.apps.cironline.org"
tail_url="/api/city/?limit=100"

r = requests.get(base_url+tail_url)
cities=json.loads(r.content)

#create a dictionary of the objects returned by the json request
citydict = cities['objects']

outfile = open('cities.csv', 'wb')
writer = csv.writer(outfile)
writer.writerow(['id','name','lat','lon','region','url','info'])

for item in citydict:
    id=item['id']
    if item['geojson']:
        lat=item['geojson']['geometry']['coordinates'][0]
        lon=item['geojson']['geometry']['coordinates'][1]
        region = item['geojson']['properties']['region']['name']
    else:
        lat = None
        lon = None 
        region = None
    name = item['name'].encode()
    url=item['resource_uri'].encode()
    info=item['text_field']
    line = id, name, lat, lon, region, url, repr(info)
    writer.writerow(line)
outfile.close()