from helpfunc import gather_all, cirdate
import json
from datetime import datetime

base_url="http://vetsapi.apps.cironline.org"
tail_url="/api/data/?format=json&limit=500&date__gte=2011-01-01"

#use this only if you want to get live data from the API
#records = gather_all(9, base_url, tail_url)
#tempfile = open('pending-claims-chart.txt', 'w')
#print >> tempfile, json.dumps(records)
#tempfile.close()

dictofdates = {}
dictofcities = {}

citiesdict={'/api/city/45/':'Buffalo, NY','/api/city/46/':'Cleveland, OH','/api/city/47/':'Detroit, MI','/api/city/49/':'Indianapolis, IN','/api/city/50/':'Manchester, NH','/api/city/51/':'New York, NY','/api/city/52/':'Newark, NJ','/api/city/53/':'Philadelphia, PA','/api/city/55/':'Providence, RI','/api/city/56/':'Togus, ME','/api/city/57/':'White River Junction, VT','/api/city/58/':'Wilmington, DE','/api/city/16/':'Columbia, SC','/api/city/17/':'Huntington, WV','/api/city/19/':'Louisville, KY','/api/city/20/':'Montgomery, AL', '/api/city/21/':'Nashville, TN','/api/city/23/':'San Juan, Puerto Rico','/api/city/25/':'Washington, DC','/api/city/26/':'Winston-Salem, NC','/api/city/29/':'Boise, ID','/api/city/18/':'Jackson, MS','/api/city/3/':'Fargo, ND','/api/city/8/':'Muskogee, OK','/api/city/9/':'New Orleans, LA', '/api/city/10/':'Sioux Falls, SD', '/api/city/11/':'St. Louis, MO', '/api/city/13/':'Waco, TX', '/api/city/15/':'Atlanta, GA','/api/city/32/':'Fort Harrison, MT', '/api/city/35/':'Manila, Philippines','/api/city/43/':'Baltimore, MD', '/api/city/44/':'Boston, MA','/api/city/37/':'Phoenix, AZ','/api/city/1/':'Chicago, IL','/api/city/39/':'Reno, NV','/api/city/5/':'Lincoln, NE','/api/city/6/':'Little Rock, AR','/api/city/40/':'Salt Lake City, UT','/api/city/14/':'Wichita, KS','/api/city/27/':'Albuquerque, NM','/api/city/28/':'Anchorage, AK','/api/city/31/':'Cheyenne, WY','/api/city/33/':'Honolulu, HI','/api/city/34/':'Los Angeles, CA', '/api/city/42/':'Seattle, WA','/api/city/7/':'Milwaukee, WI', '/api/city/4/':'Houston, TX','/api/city/12/':'St. Paul, MN','/api/city/30/':'Denver, CO', '/api/city/41/':'San Diego, CA', '/api/city/54/':'Pittsburgh, PA', '/api/city/61/':'National total', '/api/city/36/':'Oakland, CA','/api/city/24/':'St. Petersburg, FL','/api/city/2/':'Des Moines, IA', '/api/city/22/':'Roanoke, VA','/api/city/38/':'Portland, OR', '/api/city/48/':'Hartford, CT'}

monthdict={1:'Jan.', 2:'Feb.', 3:'March', 4:'April', 5:'May', 6:'June', 7:'July', 8:'Aug.', 9:'Sept.', 10:'Oct.', 11:'Nov.', 12:'Dec.'}

#use this version if you've already gathered the latest records
tempfile = open('pending-claim.txt', 'r')
reading = tempfile.read()
records = json.loads(reading)
count = 0

for item in records:
    if cirdate(item['date']) > datetime(year=2010, month=12, day=31):
        if item['date'] not in dictofdates.keys() and item['city'] != '/api/city/61/':
            dictofdates[item['date']] = [{'city': item['city'], 'value':item['value']}]
        elif item['date'] in dictofdates.keys() and item['city'] != '/api/city/61/':
            valuecity = {'city': item['city'], 'value':item['value']}
            dictofdates[item['date']].append(valuecity)
        else:
            pass
        city = citiesdict[item['city']]
        date = cirdate(item['date'])
        value = item['value']        
        if city not in dictofcities.keys() and city != 'National total':
            dictofcities[city] = [{'date': date, 'value': value}]
            count +=1
        elif city in dictofcities.keys() and city != 'National total':
            datecity = {'date': date, 'value': value}
            dictofcities[city].append(datecity)
            count +=1
        else:
            pass    
    else:
        continue

dictofcities['National average'] = []
       
for key, values in dictofdates.iteritems():
    avglist = []
    date = key
    date = cirdate(date)
    for listitem in values:
        item = listitem['value']
        avglist.append(item)        
    mysum = sum(avglist)
    average = mysum/float(len(avglist))
    mynewdict = {'date': date, 'value': average}
    dictofcities['National average'].append(mynewdict)
    count +=1

finallist=[]
for key, values in dictofcities.iteritems():
    newlist = sorted(values, key=lambda values: values['date'])
    for item in values:
        item['date'] = monthdict[item['date'].month] + " " + str(item['date'].day) + ", " + str(item['date'].year)
    newdict={}
    newdict[key]=newlist
    finallist.append(newdict)
    
newslug = "pending-claims-chart.json"
outfile = open(newslug, 'w')
myjson = json.dumps(finallist)
outfile.write(myjson)
outfile.close()
print count