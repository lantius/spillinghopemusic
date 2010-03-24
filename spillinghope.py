import cgi
import wsgiref.handlers

import os
from google.appengine.ext.webapp import template

from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext import db
from google.appengine.api import mail
import datetime

class MainPage(webapp.RequestHandler):
  def get(self):
    
    template_values = {}
    
    path = os.path.join(os.path.dirname(__file__), 'index.html')
    self.response.out.write(template.render(path, template_values))

class ThanksPage(webapp.RequestHandler):
  def get(self):

    template_values = {}

    path = os.path.join(os.path.dirname(__file__), 'thanks.html')
    self.response.out.write(template.render(path, template_values))

    
class Music(webapp.RequestHandler):
  def post(self):
    
    email = self.request.get('email')
    
    email_address = EmailAddress.gql("WHERE email = :email", email=email).get()
    if email_address:
      email_address.date = datetime.datetime.now()
    else:
      email_address = EmailAddress()
      email_address.email = email
    
    email_address.put()
    
    mail.send_mail(sender="Spilling Hope <lantatlantius@gmail.com>",
                  to=email_address.email,
                  subject="Thank you for your interest in Spilling Hope!",
                  body="""
    Spilling Hope is excellent.
    
    Check out these sweet tunes!

    Spilling Hope
    """)
    
    self.redirect('/thanks')
       
class EmailAddress(db.Model):
  email = db.StringProperty(multiline=True)
  date = db.DateTimeProperty(auto_now_add=True)

def main():
  application = webapp.WSGIApplication(
                                   [('/', MainPage),
                                    ('/thanks', ThanksPage),
                                    ('/music', Music)],
                                    debug=True)
  wsgiref.handlers.CGIHandler().run(application)

if __name__ == "__main__":
  main()


