from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
import database

class PageWithLogin(webapp.RequestHandler):
  def login(self):
    self.user = users.get_current_user()
    if not self.user:
      self.redirect(users.create_login_url(self.request.uri))
    else:
      return True

class MainPage(PageWithLogin):
  def get(self):
    if not self.login():
      return
    self.response.headers['Content-Type'] = 'text/plain'
    self.response.out.write('Hello, webapp World!')

## temp!!
class AddBalance(PageWithLogin):
  def get(self):
    if not self.login():
      return
    self.response.headers['Content-Type'] = 'text/plain'

class BalancePage(PageWithLogin):
  def get(self):  
    if not self.login():
      return
    self.response.headers['Content-Type'] = 'text/plain'
    balance = database.Database().getBalance(self.user)
    self.response.out.write('Your balance is %d' % balance)

application = webapp.WSGIApplication(
                                     [('/', MainPage),
                                      ('/balance', BalancePage)],
                                     debug=True)

def main():
  run_wsgi_app(application)

if __name__ == "__main__":
  main()
