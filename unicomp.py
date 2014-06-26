import urllib
import webapp2
import jinja2
import os
import datetime

from google.appengine.ext import ndb
from google.appengine.ext import db
from google.appengine.api import users
from data.data import *

#db.delete(db.Query(keys_only=True))

jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__) + "/templates"))

class Comment(ndb.Model):
    # Models a comment.
    content = ndb.StringProperty(indexed=False)
    author = ndb.StringProperty()
    date = ndb.DateTimeProperty(auto_now_add=True)
    

# This part for the front page
class MainPage(webapp2.RequestHandler):

    def get(self):
        template = jinja_environment.get_template('mainpage.html')
        self.response.out.write(template.render())

# Front page for those logged in
class MainPageUser(webapp2.RequestHandler):
    
    def get(self):
        user = users.get_current_user()
        if user:  # signed in already

            query = ndb.gql("SELECT * "
                            "FROM University ")
            template_values = {
                'username': users.get_current_user().nickname(),
                'logout': users.create_logout_url(self.request.host_url),
                'query' : query,
            }
            template = jinja_environment.get_template('homepage.html') 
            self.response.out.write(template.render(template_values))
        else:
            self.redirect(users.create_login_url(self.request.uri))

class BudgetPage(webapp2.RequestHandler):
    
    def get(self):
        user = users.get_current_user()
        if user:  # signed in already

            query_0 = ndb.gql("SELECT * "
                                 "FROM University "
                                 "WHERE budget_avg < 500 ")            
            query_500 = ndb.gql("SELECT * "
                                 "FROM University "
                                 "WHERE budget_avg >=500 AND budget_avg<1000")
            query_1000 = ndb.gql("SELECT * "
                                 "FROM University "
                                 "WHERE budget_avg >=1000 AND budget_avg<1500")
            query_1500 = ndb.gql("SELECT * "
                                 "FROM University "
                                 "WHERE budget_avg >=1500")
            template_values = {
                'username': users.get_current_user().nickname(),
                'logout': users.create_logout_url(self.request.host_url),
                'query_0': query_0,
                'query_500': query_500,
                'query_1000': query_1000,
                'query_1500': query_1500,
            }
            template = jinja_environment.get_template('budgetpage.html') 
            self.response.out.write(template.render(template_values))
        else:
            self.redirect(users.create_login_url(self.request.uri))

class RegionPage(webapp2.RequestHandler):
    
    def get(self):
        user = users.get_current_user()
        if user:  # signed in already
            query_asia = ndb.gql("SELECT * "
                                 "FROM University "
                                 "WHERE region =:1", 'Asia')
            query_aust = ndb.gql("SELECT * "
                                 "FROM University "
                                 "WHERE region =:1", 'Australia')
            query_europe = ndb.gql("SELECT * "
                                 "FROM University "
                                 "WHERE region =:1", 'Europe')
            query_america = ndb.gql("SELECT * "
                                 "FROM University "
                                 "WHERE region =:1", 'America')

            
            template_values = {
                'username': users.get_current_user().nickname(),
                'logout': users.create_logout_url(self.request.host_url),
                'query_asia': query_asia,
                'query_aust': query_aust,
                'query_europe': query_europe,
                'query_america': query_america,
            }
            template = jinja_environment.get_template('regionpage.html') 
            self.response.out.write(template.render(template_values))
        else:
            self.redirect(users.create_login_url(self.request.uri))

class RankPage(webapp2.RequestHandler):
    
    def get(self):
        user = users.get_current_user()
        if user:  # signed in already

            query_rank = ndb.gql("SELECT * "
                                 "FROM University "
                                 "ORDER by rank_avg ASC")
            
            template_values = {
                'username': users.get_current_user().nickname(),
                'logout': users.create_logout_url(self.request.host_url),
                'query_rank':query_rank,
            }
            
            template = jinja_environment.get_template('rankpage.html') 
            self.response.out.write(template.render(template_values))
        else:
            self.redirect(users.create_login_url(self.request.uri))

class Search(webapp2.RequestHandler):
    #individual page for each uni
    def show(self):
        user = users.get_current_user()
        if user:  # signed in already

            uni=University()
            uni_name = self.request.get('uni_name')
            uni = University.get_or_insert(uni_name)

            uni_key = ndb.Key('University', uni_name) 
            comments_query = Comment.query(ancestor=uni_key).order(-Comment.date)
            comments = comments_query.fetch(10)
            
            template_values = {
                'username': users.get_current_user().nickname(),
                'logout': users.create_logout_url(self.request.host_url),
                'uni' : uni,
                'comments' : comments,
            }
            template = jinja_environment.get_template('indivpage.html') 
            self.response.out.write(template.render(template_values))
        else:
            self.redirect(users.create_login_url(self.request.uri))
            
    def get(self):
        self.show()
        
    def post(self):
        uni_name = self.request.get('uni_name')
        uni_key = ndb.Key('University', uni_name)
        comment = Comment(parent=uni_key)
        comment.author = users.get_current_user().nickname()
        comment.content = self.request.get('content')
        uni.put()
        comment.put()
        self.show()

class UserPage(webapp2.RequestHandler):
    #test page currently for database
    def get(self):
        user = users.get_current_user()
        if user:  # signed in already

            query = ndb.gql("SELECT * "
                            "FROM University ")

            
            template_values = {
                'username': users.get_current_user().nickname(),
                'logout': users.create_logout_url(self.request.host_url),
                'query': query,
            }
            
            template = jinja_environment.get_template('userpage.html') 
            self.response.out.write(template.render(template_values))
        else:
            self.redirect(users.create_login_url(self.request.uri))
            
class AbtUsPage(webapp2.RequestHandler):
    #test page currently for database
    def get(self):
        user = users.get_current_user()
        if user:  # signed in already

            query = ndb.gql("SELECT * "
                            "FROM University ")

            
            template_values = {
                'username': users.get_current_user().nickname(),
                'logout': users.create_logout_url(self.request.host_url),
                'query': query,
            }
            
            template = jinja_environment.get_template('abtuspage.html') 
            self.response.out.write(template.render(template_values))
        else:
            self.redirect(users.create_login_url(self.request.uri))


app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/homepage', MainPageUser),
    ('/budget', BudgetPage),
    ('/region', RegionPage),
    ('/ranking', RankPage),
    ('/search', Search),
    ('/userpage', UserPage),
    ('/aboutus', AbtUsPage)
], debug=True)
