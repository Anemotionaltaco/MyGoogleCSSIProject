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

class Message(object):
    def __init__(self, text):
        self.text = text
        self.timestamp = datetime.datetime.now()
    def to_dict(self):
        result = {
            "text": self.text,
            "timestamp": self.timestamp.strftime("%Y-%m-%d %H-%M-%S")
        }
        # if len(self.email) > 10:
        #     result['email'] = self.email.split("@", 1)[0]
        # else:
        #     result['email'] = self.email
        return result


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

# class SetUserDataHandler(webapp2.RequestHandler):
#     def dispatch(self):



# class AddMessageHandler(webapp2.RequestHandler):
#     def dispatch(self):
#         result = {}
#         email = get_current_user_email()
#         if email:
#             msg_text = self.request.get("text")
#             if len(msg_text) > 500:
#                 result["error"] = "Message is too long."
#             elif not msg_text.strip():
#                 result["error"] = "Message is empty."
#             else:
#                 messages = memcache.get("messages")
#                 if not messages:
#                     messages = []
#                 msg = Message(email, msg_text)
#                 messages.append(msg)
#                 memcache.set("messages", messages)
#                 result["OK"] = True
#         else:
#             result["error"] = "User is not logged in."
#         send_json(self, result)
#
# class GetLoginUrlHandler(webapp2.RequestHandler):
#     def dispatch(self):
#         result = {
#             "url": users.create_login_url("/")
#         }
#         send_json(self, result)
#
# class GetLogoutUrlHandler(webapp2.RequestHandler):
#     def dispatch(self):
#         result = {
#             "url": users.create_logout_url("/")
#         }
#         send_json(self, result)
#
# class GetMessageHandler(webapp2.RequestHandler):
#     def dispatch(self):
#         email = get_current_user_email()
#         result = {}
#         if email:
#             result["messages"] = []
#             messages = memcache.get("messages")
#             if messages:
#                 for message in messages:
#                     result["messages"].append(message.to_dict())
#         else:
#             result["error"] = "User is not logged in"
#         send_json(self, result)
#
# class GetUserHandler(webapp2.RequestHandler):
#     def dispatch(self):
#         email = get_current_user_email()
#         result = {}
#         if email:
#             result["user"] = email
#         else:
#             result["error"] = "User is not logged in"
#         send_json(self, result)


class AddMessageHandler(webapp2.RequestHandler):
    def dispatch(self):
        result = {}
        # email = get_current_user_email()
        text = self.request.get("home")
        # Model.genre = self.request.get(genre)
        if len(text) > 500:
            result["error"] = "Message is too long."
        elif not text.strip():
            result["error"] = "Message is empty."
        else:
            messages = memcache.get("messages")
            if not messages:
                messages = []
            msg = Message(text)
            messages.append(msg)
            memcache.set("messages", messages)
            result["OK"] = True

        m = Model(text=text)
        m.put()

        # else:
        #     result["error"] = "User is not logged in."


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
    # ("/setUserData", SetUserDataHandler)
    # ("/gospel", GospelHandler),
    # ("/login", GetLoginUrlHandler),
    # ("/logout", GetLogoutUrlHandler),
    # ("/messages", GetMessageHandler),
    # ("/user", GetUserHandler)
], debug=True)
