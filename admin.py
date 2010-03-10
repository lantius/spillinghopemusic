import cgi
import wsgiref.handlers

import os
from google.appengine.ext.webapp import template

from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext import db

from spillinghope import EmailAddress

class Admin(webapp.RequestHandler):
  def get(self):
    
    template_values = { 'emails' : EmailAddress.all() }
    
    path = os.path.join(os.path.dirname(__file__), 'admin.html')
    self.response.out.write(template.render(path, template_values))

def main():
  application = webapp.WSGIApplication(
                                   [('/admin', Admin),
                                   ],
                                    debug=True)
  wsgiref.handlers.CGIHandler().run(application)

if __name__ == "__main__":
  main()


