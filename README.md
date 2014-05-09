cirva
=====

What is this?
-------------

Scripts to grab and parse data from Center for Investigative Reporting's Veterans Affairs backlog API into CSVs.

https://github.com/cirlabs/va-data-dashboard#data-updates

You can see the latest data at:
http://tdbeta.digitalfirstmedia.com/cirva/

Credits
---------

Data from CIR's VA backlog API. Scripts by Tom Meagher.


Assumptions
-----------

Requirements for these scripts are simple: You need Python 2.7 and the [Requests library](http://docs.python-requests.org/en/latest/). To install Requests, while inside your [virtualenv](http://virtualenvwrapper.readthedocs.org/en/latest/) type `pip install requests`.

After you run it the first time, it's easy to get updates or even automate the process.
First, run `python updates.py`, which looks at the CSVs you've already grabbed and gets newer data from the API.
Then, run `python makestats.py`, which will create the index.html report page that offers a birds-eye view of the range of the data.

License
----------

This code is available under the MIT license. For more information, please see the LICENSE file in this repo.
