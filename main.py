from google.appengine.api import memcache
from google.appengine.ext import ndb
from google.appengine.api import users


import datetime
import jinja2
import json
import os
import webapp2

jinja_current_directory = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class Model(ndb.Model):
    genre = ndb.StringProperty()
    text = ndb.TextProperty()
    date = ndb.DateTimeProperty(auto_now_add=True)

# class Message(object):
#     def __init__(self, text):
#         self.text = text
#         self.timestamp = datetime.datetime.now()
#     def to_dict(self):
#         result = {
#             "text": self.text,
#             "timestamp": self.timestamp.strftime("%Y-%m-%d %H-%M-%S")
#         }
#         # if len(self.email) > 10:
#         #     result['email'] = self.email.split("@", 1)[0]
#         # else:
#         #     result['email'] = self.email
#         return result


#HANDLERS
class GetMainPageHandler(webapp2.RequestHandler):
    def get(self):
        main_page = jinja_current_directory.get_template("templates/buttonPage.html")
        params = {}
        params['genres'] = {
            'gospel': 'Gospel!',
            'hiphop': 'Hip Hop!',
            'indie': 'Indie!',
            'jazz': 'Jazz!',
            'pop': 'Pop!',
            'rnb': 'R&B!',
        }
        self.response.out.write(main_page.render(params))

class GetAboutPageHandler(webapp2.RequestHandler):
    def get(self):
        main_page = jinja_current_directory.get_template("templates/aboutus.html")
        self.response.out.write(main_page.render())

class GetGenreHandler(webapp2.RequestHandler):
    def get(self):
        genre = self.request.get("genre")
        # genre_key = ndb.Key('Model', 'rnb')
        # genre = genre_key.get()
        print(genre)
        if genre == "gospel":
            genre_page = jinja_current_directory.get_template("templates/gospelpage.html")
        if genre == "hiphop":
            genre_page = jinja_current_directory.get_template("templates/hiphoppage.html")
        if genre == "indie":
            genre_page = jinja_current_directory.get_template("templates/indiepage.html")
        if genre == "jazz":
            genre_page = jinja_current_directory.get_template("templates/jazzpage.html")
        if genre == "pop":
            genre_page = jinja_current_directory.get_template("templates/poppage.html")
        if genre == "rnb":
            genre_page = jinja_current_directory.get_template("templates/rnbpage.html")
        self.response.out.write(genre_page.render())

class AddMessageHandler(webapp2.RequestHandler):
    def dispatch(self):
        # result = {}
        # email = get_current_user_email()
        genre = self.request.get("genre")
        text = self.request.get("home")
        # Model.genre = self.request.get(genre)
        # if len(text) > 500:
        #     result["error"] = "Message is too long."
        # elif not text.strip():
        #     result["error"] = "Message is empty."
        # else:
        #     messages = memcache.get("messages")
        #     if not messages:
        #         messages = []
        #     msg = Message(text)
        #     messages.append(msg)
        #     memcache.set("messages", messages)
        #     result["OK"] = True

        m = Model(genre=genre, text=text)
        m.put()

        self.redirect("/genre?genre=" + genre)

        # else:
        #     result["error"] = "User is not logged in."

class GetMessageHandler(webapp2.RequestHandler):
    def dispatch(self):
        result = {}
        result["messages"] = []
        genre = self.request.get("genre")
        # messages = memcache.get("messages")
        # if messages:
        #     for message in messages:
        #         result["messages"].append(message.to_dict())
        #
        # 1) get all Model entries with Model.genre == genre sorted by date
        # if Model.genre == "rnb":

        query = Model.query()


        # print(result["messages"])
        if genre == "gospel":
            query_gospel = query.filter(Model.genre == "gospel")
            for text in query_gospel:
                result["messages"].append(text.text)
            genre_page = jinja_current_directory.get_template("templates/gospelpage.html")
        if genre == "hiphop":
            query_hiphop = query.filter(Model.genre == "hiphop")
            for text in query_hiphop:
                result["messages"].append(text.text)
            genre_page = jinja_current_directory.get_template("templates/hiphoppage.html")
        if genre == "indie":
            query_indie = query.filter(Model.genre == "indie")
            for text in query_indie:
                result["messages"].append(text.text)
            genre_page = jinja_current_directory.get_template("templates/indiepage.html")
        if genre == "jazz":
            query_jazz = query.filter(Model.genre == "jazz")
            for text in query_jazz:
                result["messages"].append(text.text)
            genre_page = jinja_current_directory.get_template("templates/jazzpage.html")
        if genre == "pop":
            query_pop = query.filter(Model.genre == "pop")
            for text in query_pop:
                result["messages"].append(text.text)
            genre_page = jinja_current_directory.get_template("templates/poppage.html")
        if genre == "rnb":
            query_rnb = query.filter(Model.genre == "rnb")
            for text in query_rnb:
                result["messages"].append(text.text)
            genre_page = jinja_current_directory.get_template("templates/rnbpage.html")
        # 3) pass the list to a template and render
        print(result["messages"])
        self.response.out.write(genre_page.render(messages=result["messages"]))

        # self.redirect("/genre?genre=" + genre)
        # else:
        #     result["error"] = "User is not logged in"

class User(ndb.Model):
  """CssiUser stores information about a logged-in user.

  The AppEngine users api stores just a couple of pieces of
  info about logged-in users: a unique id and their email address.

  If you want to store more info (e.g. their real name, high score,
  preferences, etc, you need to create a Datastore model like this
  example).
  """
  first_name = ndb.StringProperty()
  last_name = ndb.StringProperty()

class GetUserHandler(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        # If the user is logged in...
        if user:
          email_address = user.nickname()
          the_user = User.get_by_id(user.user_id())
          signout_link_html = '<a href="%s">sign out</a>' % (
              users.create_logout_url('/login'))
          # If the user has previously been to our site, we greet them!
          if the_user:
            self.response.write('''
                Welcome %s %s (%s)! <br> %s <br>''' % (
                  the_user.first_name,
                  the_user.last_name,
                  email_address,
                  signout_link_html))
          # If the user hasn't been to our site, we ask them to sign up
          else:
            self.response.write('''
                Welcome to our site, %s!  Please sign up! <br>
                <form method="post" action="/">
                <input type="text" name="first_name">
                <input type="text" name="last_name">
                <input type="submit">
                </form><br> %s <br>
                ''' % (email_address, signout_link_html))
        # Otherwise, the user isn't logged in!
        else:
          self.response.write('''
            Please log in to use our site! <br>
            <a href="%s">Sign in</a>''' % (
              users.create_login_url('/login')))

    def post(self):
        user = users.get_current_user()
        if not user:
          # You shouldn't be able to get here without being logged in
          self.error(500)
          return
        the_user = User(
            first_name=self.request.get('first_name'),
            last_name=self.request.get('last_name'),
            id=user.user_id())
        the_user.put()
        self.response.write('Thanks for signing up, %s!' %
            the_user.first_name)

#
# #DEFS
# def get_current_user_email():
#     current_user = users.get_current_user()
#     if current_user:
#         return current_user.email()
#     else:
#         return None



#MAPPING
app = webapp2.WSGIApplication([
    ("/", GetMainPageHandler),
    ("/add", AddMessageHandler),
    ("/genre", GetGenreHandler),
    ("/messages", GetMessageHandler),
    # ("/setUserData", SetUserDataHandler)
    ("/about", GetAboutPageHandler),
    ("/login", GetUserHandler),
    # ("/logout", GetLogoutUrlHandler),
    # ("/user", GetUserHandler)
], debug=True)
