'''
Functions to gather and process data from the CIR VA API.
'''
import json
import os
import subprocess
import csv
import requests
import datetime, time

#third-party module
import requests

folder=[[1, u'completed-claims'], [2, u'average-processing-time'], [3, u'appealed-claims'], [4, u'claims-completed-per-fte'], [5, u'employees-on-duty'], [6, u'claims-pending-at-least-one-year'], [7, u'claims-received'], [8, u'claims-received-average-wait'], [9, u'pending-claim'], [14, u'claims-pending-125-days'], [15, u'average-days-pending']]

testfolder=[[5, u'employees-on-duty'], [15, u'average-days-pending']]

def commas(N): 
    """
    format positive integer-like N for display with commas 
    between digit groupings: xxx,yyy,zzz
    From 'Learning Python' book
    """
    digits = str(N)
    assert(digits.isdigit())
    result = ''
    while digits:
        digits, last3 = digits[:-3], digits[-3:]
        result = (last3 + ',' + result) if result else last3 
    return result

def cirdate(datestring):
    '''returns a datetime object from weirdo date string'''
    newdate=datetime.datetime.strptime(datestring, "%a %d %b %Y %H:%M:%S GMT-0800")
    return newdate

def cleandate(datestring):
    '''returns a datetime object from a cleaned up date string'''
    newstring=datestring.split("-")
    year = newstring[0]
    month = newstring[1]
    if len(month)==1:
        month = "0" + month
    day = newstring[2]
    if len(day) == 1:
        day = "0" + day
    datestring = year+"-"+month+"-"+day        
    newdate=datetime.datetime.strptime(datestring, "%Y-%m-%d")
    return newdate

def last_updated(file):
    '''when was this csv/txt last touched?'''    
    this_time = os.path.getmtime(file)
    mean_time = datetime.datetime.fromtimestamp(this_time)
    return mean_time

def file_len(file):
    '''how many records in this json or csv?'''
    if file.endswith(".txt") or file.endswith(".json"):
        hi = open("{0}".format(file), "r")
        me = hi.read()
        hi.close()
        you = json.loads(me)
        me_length = len(you)
    elif file.endswith(".csv"):
        hi = open("{0}".format(file), "rb")
        count = 0 
        for line in you:
            count += 1
        me_length = count-1
    else:
        pass
    return me_length

def time_and_len(file):
    '''how big and old is this text file?'''
    time = last_updated(file)
    length = file_len(file)
    update = file + ", " + str(length) + " records, Last updated: " + str(time)
    return update

def get_stats(file):
    '''gives oldest/newest entries in a csv file'''
    welcome = open(file,"rb")
    greetings = csv.reader(welcome)
    greetings.next()
    dates = []
    for line in greetings:
        myline=line[4]
        helpme=cleandate(myline)
        seconds=time.mktime(helpme.timetuple())
        dates.append(seconds)
    count = len(dates)
    welcome.close()
    full_max_date = datetime.datetime.fromtimestamp(max(dates)).date()
    max_date = str(full_max_date.month) + "/" + str(full_max_date.day) + "/" + str(full_max_date.year)
    full_min_date = datetime.datetime.fromtimestamp(min(dates)).date()
    min_date = str(full_min_date.month) + "/" + str(full_min_date.day) + "/" + str(full_min_date.year)
    return file, count, max_date, min_date 

def add_to_csv(file):
    '''make a csv out of a json txt from a file'''
    outfile = open("{0}.csv".format(file), "w")
    writer = csv.writer(outfile)
    writer.writerow(['city','created','region','value','date','field_type_slug','id'])
    hello = open("{0}.txt".format(file), "r")
    old_friend = hello.read()
    hello.close()
    new_file = json.loads(old_friend)
    old_friend=[]
    for line in new_file: 
        mycity = line['city'].split('/api/city/')
        city = mycity[1][:-1] 
        mycreated = line['created']
        created = mycreated[:mycreated.find("T")]
        myregion = line['region'].split('/api/region/')
        region = myregion[1][:-1]
        value = line['value']
        mydate = line['date']
        mynewdate = cirdate(mydate)
        date = str(mynewdate.year)+"-"+str(mynewdate.month)+"-"+str(mynewdate.day)
        field_type = line['field_type_slug']
        id = line['id']
        record = (city, created, region, value, date, field_type, id)
        writer.writerow(record)
    outfile.close()
    message = file + " printed to csv"
    print message


def gather_all(field, base_url, tail_url):
    '''gather all of the data out of the API, returned as a str'''
    back_url = tail_url + "&field_type={0}".format(field)
    r = requests.get(base_url+back_url, config={"max_retries":20})
    field_data = json.loads(r.content)
    next_url = field_data['meta']['next']
    count = field_data['meta']['total_count']
    if count==0:
        records = None
    else: 
        records = field_data['objects']
        while next_url:
            askme = base_url + next_url
            hi = requests.get(askme, config={"max_retries":30})
            response = json.loads(hi.content)
            wordemup = (response['objects'])
            for round in wordemup:
                records.append(round)
            if response['meta']['next']==None:
                next_url = None
            else:
                next_url=response['meta']['next'].encode()
    return records

def archive():
    '''move all the csvs to an archive for safe-keeping'''
    now=datetime.datetime.now()
    mydate=str(now.year) + "_" + str(now.month) + "_" + str(now.day)
    mycmd = "mkdir archive/{0}".format(mydate)
    make_dir=subprocess.Popen(mycmd.split())
    make_dir.wait()
    for file in folder: 
        move_cmd = "cp {0}.csv archive/{1}/".format(file[1], mydate)
        args = move_cmd.split()
        print args
        move_files=subprocess.Popen(args)
        move_files.wait()
    message = "Archived csvs"
    return message

if __name__ == '__main__':
    print "hello"