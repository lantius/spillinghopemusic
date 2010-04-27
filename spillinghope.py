import cgi
import wsgiref.handlers

import os
from google.appengine.ext.webapp import template

from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext import db
from google.appengine.api import mail
import datetime

# alternate link: http://www.mediafire.com/file/gym3wguw2id/SpillingHopeVolumeOne.zip

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
    
    mail.send_mail(sender="Spilling Hope <woltbrian@gmail.com>",
                  to=email_address.email,
                  subject="Thank you for your interest in Spilling Hope!",
                  body="""
Thanks for choosing to download Spilling Hope - Volume One!  It is our desire that through the spreading of this music, people will become aware of their habits and the solvable issue of clean water - an unfortunate cause of thousands of deaths everyday.

Spilling Hope is an initiative committed to a new way of living in the world.  During the 50 days following Easter, people challenge one another to live simply and utilize resources differently by freeing up at least $1 a day.  (Cut out a cup of coffee or two, eat out less, cancel cable, walk more, etc.) At the end of the 50 days people give generously out of what they saved in order to provide clean drinking water to others.

Last year Spilling Hope was able to raise over $130,000 and provide 13 wells in Uganda.  Our goal this year is to drill at least 10 more wells in Uganda through Living Water International.  But it's not just about giving money; in fact you can't give until May 23, when the 50 days are over.  So in the meantime, take back control of your life, spend more time with family and less with the TV, serve in your community, reconsider eating choices, spending choices and how you spend your valuable resources of time and money.  I hope you consider simplifying with us and making a difference in your life and the lives of others!

Live simply. Give generously. Change lives.

Download the compilation here: http://dl.dropbox.com/u/1596576/SpillingHopeVolumeOne.zip                  
                  
- Spilling Hope V1 Team

p.s. The bands would love to hear your story... what did you do to Spill Hope?  Email your experience to: info@spillinghope.org
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


