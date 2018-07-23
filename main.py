from google.appengine.api import memcache
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

#OBJECTS
# class Message(object):
#     def __init__(self, email, text):
#         self.email = email
#         self.text = text
#         self.timestamp = datetime.datetime.now()
#     def to_dict(self):
#         result = {
#             "text": self.text,
#             "timestamp": self.timestamp.strftime("%Y-%m-%d %H-%M-%S")
#         }
#         if len(self.email) > 10:
#             result['email'] = self.email.split("@", 1)[0]
#         else:
#             result['email'] = self.email
#         return result

#HANDLERS
class GetMainPageHandler(webapp2.RequestHandler):
    def get(self):
        main_page = jinja_current_directory.get_template("templates/buttonPage1.html")
        params = {}
        params['genres'] = {
            'hiphop': 'Hip Hop!',
            'rnb': 'R&B!',
            'indie': 'Indie!',
            'pop': 'Pop!',
            'jazz': 'Jazz!',
            'gospel': 'Gospel!'
        }
        self.response.out.write(main_page.render(params))

class GetGenreHandler(webapp2.RequestHandler):
    def get(self):
        genre = self.request.get("genre")
        if genre == "gospel":
            genre_page = jinja_current_directory.get_template("templates/gospelpage.html")

        self.response.out.write(genre_page.render())



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
#
# #DEFS
# def get_current_user_email():
#     current_user = users.get_current_user()
#     if current_user:
#         return current_user.email()
#     else:
#         return None
#
def send_json(request_handler, props):
    request_handler.response.content_type = "application/json"
    request_handler.response.out.write(json.dumps(props))


#MAPPING
app = webapp2.WSGIApplication([
    ("/", GetMainPageHandler),
    ("/genre", GetGenreHandler),
    # ("/gospel", GospelHandler),
    # ("/login", GetLoginUrlHandler),
    # ("/logout", GetLogoutUrlHandler),
    # ("/messages", GetMessageHandler),
    # ("/user", GetUserHandler)
], debug=True)
