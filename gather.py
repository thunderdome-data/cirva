#!/usr/bin/env python

'''
grab all the data in CIR's VA API
and load into static json files 
for examination and processing.
'''
import json
import requests
from helpfunc import gather_all, add_to_csv

#Ask the API for the file in JSON format
base_url="http://vetsapi.apps.cironline.org"
tail_url="/api/field-type/?format=json&limit=500"

#use the requests library to call the API
r = requests.get(base_url+tail_url)
all_data=[json.loads(r.content)]
objects = all_data[0]['objects']

#build a list of all the available field names and IDs
fields = []
for object in objects:
    field_type = object['id']
    field_slug = object['slug']
    fields.append([field_type, field_slug])

tail_url="/api/data/?format=json&limit=500"

for field in fields:
    myfield = field[0]
    #loop through many requests to get it all, return a list of records
    records = gather_all(myfield, base_url, tail_url)
    new_slug=field[1].encode()     
    outfile = open('{0}.txt'.format(new_slug), 'w')
    print >> outfile, json.dumps(records)
    print new_slug + " " + str(len(records))
    outfile.close()
    add_to_csv(new_slug)