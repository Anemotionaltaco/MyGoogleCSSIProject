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
    # ("/gospel", GospelHandler),
    # ("/login", GetLoginUrlHandler),
    # ("/logout", GetLogoutUrlHandler),
    # ("/user", GetUserHandler)
], debug=True)
