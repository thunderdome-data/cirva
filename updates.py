#!/usr/bin/env python

'''
grab all the data in CIR's VA API
and load into static json files 
for examination and processing.
'''
import json
import requests
from datetime import datetime
from helpfunc import gather_all, get_stats, folder, archive, add_to_csv

#Ask the API for the file in JSON format
base_url="http://vetsapi.apps.cironline.org"

#archive all the current CSVs
archive()

#loop through the list of fields, get the latest date in the csv
#then query the API for any records since that date
for file in folder:
    file_name = file[1]
    file_id = file[0]
    file, count, max_date, min_date = get_stats("{0}.csv".format(file_name))
    query_date = max_date.split("/")
    year = query_date[2]
    month = query_date[0]
    if len(month)<2:
        month = "0" + month
    else:
        month = month
    date = query_date[1]
    if len(date) < 2:
        date = "0" + date
    else:
        date = date
    query_date = year + "-" + month + "-" + date
    tail_url = "/api/data/?format=json&limit=250&date__gt={0}".format(query_date)
    records = gather_all(file_id, base_url, tail_url)

    #if there's any new records since the query date, open the JSON txt file, read it
    #append the new records and write back to itself    
    if records:    
        infile = open('{0}.txt'.format(file_name), 'r')
        reading = infile.read()
        infile.close()
        outfile = open('{0}.txt'.format(file_name), 'w')
        old_json = json.loads(reading)
        for record in records:
            old_json.append(record) 
        print >> outfile, json.dumps(old_json)
        print file_name + " " + str(len(old_json))
        outfile.close()

        #create the CSV from the updated json text file
        add_to_csv(file_name)

    else: 
        print file_name + " has no updates today"