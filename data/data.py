import csv
import urllib
import webapp2
import jinja2
import os
import datetime

from google.appengine.ext import ndb
from google.appengine.api import users

#testing function that reads schools into a list
def read_csv(csvfilename):
    """
    Reads a csv file and returns a list of list
    containing rows in the csv file and its entries.
    """
    rows = []

    with open(csvfilename) as csvfile:
        file_reader = csv.reader(csvfile)
        for row in file_reader:
            rows.append(row)
    return rows

#print(read_csv("consolidated_unis.csv"))
#note that first row is header, should start from row 1 not row 0

class University(ndb.Model):
    name = ndb.StringProperty()
    region = ndb.StringProperty()
    country = ndb.StringProperty()
    city_state = ndb.StringProperty()
    semester = ndb.StringProperty()
    places = ndb.StringProperty()
    budget = ndb.StringProperty()
    budget_avg = ndb.IntegerProperty()
    rank_global = ndb.StringProperty()
    rank_avg = ndb.IntegerProperty()
    rank_computing = ndb.StringProperty()
    language = ndb.StringProperty()
    remarks = ndb.StringProperty()
    weblink = ndb.StringProperty()
    pic_sml = ndb.StringProperty()
    pic_large = ndb.StringProperty()

""" To read in the unis and save to database"""
with open("consolidated_unis.csv") as csvfile:
    file_reader = csv.reader(csvfile)
    for row in file_reader:
        uni = University()       
        name = row[0]#
        uni = University.get_or_insert(name)#
        if not uni.country:     #if uni does not alr exist
            uni.name = row[0]
            uni.region = row[1] 
            uni.country = row[2]
            uni.city_state = row[3]
            uni.semester = row[4]
            uni.places = row[5]
            uni.budget = row[6]
            uni.budget_avg = int(row[7])
            uni.rank_global = row[8]
            uni.rank_avg = int(row[9])
            uni.rank_computing = row[10]
            uni.language = row[11]
            uni.remarks = row[12]
            uni.weblink = row[13]
            uni.pic_sml = row[14]
            uni.pic_large = row[15]
            uni.put()
        else:
            uni.name = row[0]
            uni.region = row[1] 
            uni.country = row[2]
            uni.city_state = row[3]
            uni.semester = row[4]
            uni.places = row[5]
            uni.budget = row[6]
            uni.budget_avg = int(row[7])
            uni.rank_global = row[8]
            uni.rank_avg = int(row[9])
            uni.rank_computing = row[10]
            uni.language = row[11]
            uni.remarks = row[12]
            uni.weblink = row[13]
            uni.pic_sml = row[14]
            uni.pic_large = row[15]
            

"""class SubmitForm(webapp2.RequestHandler):
  def post(self):
    # We set the parent key on each 'Greeting' to ensure each guestbook's
    # greetings are in the same entity group.
    guestbook_name = self.request.get('guestbook_name')
    greeting = Greeting(parent=ndb.Key("Book", guestbook_name or "*notitle*"),
                        content = self.request.get('content'))
    greeting.put()
"""
    
