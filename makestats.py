#!/usr/bin/env python

'''
loops through and gathers stats on each file in a folder
and builds an html page with the updates and links
'''

from datetime import datetime
from helpfunc import get_stats, folder, commas

outfile = open("index.html", "w")
w = "<html>\n<head><title>Latest VA records</title></head>\n<body>\n"
outfile.write(w)

w2 ="<h1>Latest VA records</h1>\n<table border='1' padding='1'>\n<tr>\n<td>file_name</td>\n<td>record_count</td>\n<td>newest_record</td>\n<td>oldest_record</td>\n</tr>"
outfile.write(w2)

for file in folder:
    file_name=str(file[1])+".csv"
    new_name, count, max_date, min_date = get_stats(file_name)
    line = "<tr>\n<td><a href='{0}'".format(new_name)+">"+ str(new_name)+"</a></td>\n<td><center>"+commas(count)+"</center></td>\n<td>"+str(max_date)+"</td>\n<td>"+str(min_date)+"</td>\n</tr>\n"
    outfile.write(line)

w3 = "<tr>\n<td><a href='{0}'".format("cities.csv")+">"+ "cities.csv"+"</a></td>\n<td><center></center></td>\n<td></td>\n<td></td>\n</tr>\n"
outfile.write(w3)

w4 = "</table>\n<p></p><br />\n"
outfile.write(w4)

w2a = "<a href='https://github.com/cirlabs/va-data-dashboard#data-updates'>Note on data updates and record layout from CIR</a><br />\n<br />\n"
outfile.write(w2a)

now=datetime.now()
mydate=str(now.month) + "/" + str(now.day) + "/" + str(now.year) + " " + str(now.hour) + ":" + str(now.minute)
stamp = "\nLast updated: {0}\n".format(mydate)
outfile.write(stamp)

w5 = "\n</body>\n</html>"
outfile.write(w5)
outfile.close()