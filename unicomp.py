import urllib
import webapp2
import jinja2
import os
import datetime
import time

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
    
class Persons(ndb.Model):
    # Models a person. Key is the email.
    next_fav = ndb.IntegerProperty()  

class Favourites(ndb.Model):
    fav_uni = ndb.StringProperty()
    
def addToFave(email, uni_name):
        curr_user = ndb.Key('Persons', email)
        person = curr_user.get()
        if person == None:
            person = Persons(id=email)
            person.next_fav = 1            

        if uni_name== "":
            return
        
        #chosen_key = db.Key.from_path('Persons', email,'Favourites', uni_name)
        #chosen_uni = db.get(chosen_key)

        fav = Favourites(parent=curr_user, id= uni_name)
        fav.fav_uni = uni_name
        person.next_fav +=1
        person.put()
        fav.put()

#count the number of favourites added by user
def countFav():
    curr_user = ndb.Key('Persons', users.get_current_user().email())
    query = ndb.gql("SELECT * "
                    "FROM Favourites "
                     "WHERE ANCESTOR IS :1 ",
                     curr_user)
    count = 0
    for i in query:
        count +=1
    return count

         
# This part for the front page
class MainPage(webapp2.RequestHandler):

    def get(self):
        template = jinja_environment.get_template('mainpage.html')
        self.response.out.write(template.render())

# Front page for those logged in
class MainPageUser(webapp2.RequestHandler):
    
    def show(self):
        user = users.get_current_user()
        if user:  # signed in already

            query = ndb.gql("SELECT * "
                            "FROM University ")
            template_values = {
                'username': users.get_current_user().nickname(),
                'logout': users.create_logout_url(self.request.host_url),
                'query' : query,
                'counter': countFav(),
            }
            template = jinja_environment.get_template('homepage.html') 
            self.response.out.write(template.render(template_values))
        else:
            self.redirect(users.create_login_url(self.request.uri))

    def get(self):
        uni_name = self.request.get('uni_name')
        email = users.get_current_user().email()
        addToFave(email, uni_name) 
        self.show()

class BudgetPage(webapp2.RequestHandler):
    
    def show(self):
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
                'counter': countFav(),
            }
            template = jinja_environment.get_template('budgetpage.html') 
            self.response.out.write(template.render(template_values))
        else:
            self.redirect(users.create_login_url(self.request.uri))
    def get(self):
        uni_name = self.request.get('uni_name')
        email = users.get_current_user().email()
        addToFave(email, uni_name) 
        self.show()
        
class RegionPage(webapp2.RequestHandler):
    
    def show(self):
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
                'counter': countFav(),
            }
            template = jinja_environment.get_template('regionpage.html') 
            self.response.out.write(template.render(template_values))
        else:
            self.redirect(users.create_login_url(self.request.uri))
    def get(self):
        uni_name = self.request.get('uni_name')
        email = users.get_current_user().email()
        addToFave(email, uni_name) 
        self.show()
        
class RankPage(webapp2.RequestHandler):
    
    def show(self):
        user = users.get_current_user()
        if user:  # signed in already

            query_rank = ndb.gql("SELECT * "
                                 "FROM University "
                                 "ORDER by rank_avg ASC")
            
            template_values = {
                'username': users.get_current_user().nickname(),
                'logout': users.create_logout_url(self.request.host_url),
                'query_rank':query_rank,
                'counter': countFav(),
            }
            
            template = jinja_environment.get_template('rankpage.html') 
            self.response.out.write(template.render(template_values))
        else:
            self.redirect(users.create_login_url(self.request.uri))

    def get(self):
        uni_name = self.request.get('uni_name')
        email = users.get_current_user().email()
        addToFave(email, uni_name) 
        self.show()
        
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
                'counter': countFav(),
            }
            template = jinja_environment.get_template('indivpage.html') 
            self.response.out.write(template.render(template_values))
        else:
            self.redirect(users.create_login_url(self.request.uri))
            
    def get(self):
        self.show()
        
    def post(self):

        favOrNot = self.request.get('favOrNot')
        if favOrNot == 'True':
            uni_name = self.request.get('uni_name')
            email = users.get_current_user().email()
            addToFave(email, uni_name)
            self.show()

        else:
            uni_name = self.request.get('uni_name')
            uni_key = ndb.Key('University', uni_name)
            comment = Comment(parent=uni_key)
            comment.author = users.get_current_user().nickname()
            comment.content = self.request.get('content')
            uni.put()
            comment.put()
            self.show()


class UserPage(webapp2.RequestHandler):
   
    def get(self):
        user = users.get_current_user()
        curr_user = ndb.Key('Persons', users.get_current_user().email())
        if user:  # signed in already

            query = ndb.gql("SELECT * "
                            "FROM Favourites "
                            "WHERE ANCESTOR IS :1 ",
                            curr_user)

            query2 = ndb.gql("SELECT * "
                             "FROM University "
                                 )
            a_list = []
            for i in query:
                for j in query2:
                    if i.fav_uni == j.name :
                        a_list.append(j)
                        
            template_values = {
                'username': users.get_current_user().nickname(),
                'logout': users.create_logout_url(self.request.host_url),
                'query': a_list,
            }
            
            template = jinja_environment.get_template('userpage.html') 
            self.response.out.write(template.render(template_values))
        else:
            self.redirect(users.create_login_url(self.request.uri))
            
class AbtUsPage(webapp2.RequestHandler):
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


class FilterPage(webapp2.RequestHandler):

    def show(self):
        user = users.get_current_user()
        if user:  # signed in already
            wanted_Budget = self.request.get('budget')
            wanted_Rank = self.request.get('ranking')
            wanted_Region = self.request.get('region')

           
            query1 = ndb.gql("SELECT * "
                            "FROM University "
                            + getbudget(wanted_Budget)  
                            )

            query2 = ndb.gql("SELECT * "
                            "FROM University "
                            + getrank(wanted_Rank)  
                            )             
            a_list = []
            for i in query1:
                for j in query2:
                    if i.name == j.name :
                        a_list.append(j)

            if wanted_Region != 'none':
                query3 = ndb.gql("SELECT * "
                                 "FROM University "
                                 "WHERE region =:1", getregion(wanted_Region)  
                                 )
                b_list = []
                for i in query3:
                    for j in a_list:
                        if i.name == j.name :
                            b_list.append(j)

                queryfinal=b_list
                
            else:
                queryfinal = a_list

            template_values = {
                'username': users.get_current_user().nickname(),
                'logout': users.create_logout_url(self.request.host_url),
                'query' : queryfinal,
                'counter': countFav(),
                'wanted_Budget' : wanted_Budget,
                'wanted_Rank' : wanted_Rank,
                'wanted_Region' : wanted_Region, #all this needed because of 'get' method to run query again to display same page
            }
            
            template = jinja_environment.get_template('filterpage.html') 
            self.response.out.write(template.render(template_values))
        else:
            self.redirect(users.create_login_url(self.request.uri))

    def get(self):
        uni_name = self.request.get('uni_name')
        email = users.get_current_user().email()
        addToFave(email, uni_name) 
        self.show()
        
def getbudget(value):
    if value=='0':
        return "WHERE budget_avg <500"
    elif value=='500':
        return "WHERE budget_avg >=500 AND budget_avg<1000"
    elif value=='1000':
        return "WHERE budget_avg >=1000 AND budget_avg<1500"
    elif value=='1500':
        return "WHERE budget_avg >=1500"
    else:
        return ""

def getrank(value):
    if value=='0':
        return "WHERE rank_avg <100"
    elif value=='100':
        return "WHERE rank_avg >=100 AND rank_avg<200"
    elif value=='200':
        return "WHERE rank_avg >=200 AND rank_avg<300"
    elif value=='300':
        return "WHERE budget_avg >=300"
    else:
        return ""
    
def getregion(value):

    if value=='Asia':
        return  'Asia'
    elif value=='Australia':
        return 'Australia'
    elif value=='Europe':
        return 'Europe'
    elif value=='America':
        return 'America'
    else:
        return ""
    
app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/homepage', MainPageUser),
    ('/budget', BudgetPage),
    ('/region', RegionPage),
    ('/ranking', RankPage),
    ('/search', Search),
    ('/userpage', UserPage),
    ('/aboutus', AbtUsPage),
    ('/results', FilterPage)
], debug=True)
