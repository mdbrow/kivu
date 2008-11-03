from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
import database


def EnsureLoggedIn(fn):
  """This is a docstring bitches."""
  def Decorated(self, *args, **kwargs):
    if not users.get_current_user():
      self.redirect(users.create_login_url(self.request.uri))
    else:
      return fn(self, *args, **kwargs)
  return Decorated


class MainPage(webapp.RequestHandler):
  @EnsureLoggedIn
  def get(self):
    self.response.headers['Content-Type'] = 'text/plain'
    self.response.out.write('Hello, webapp World!')


## temp!!
class AddBalance(webapp.RequestHandler):
  @EnsureLoggedIn
  def get(self):
    self.response.headers['Content-Type'] = 'text/plain'


class BalancePage(webapp.RequestHandler):
  @EnsureLoggedIn
  def get(self):  
    self.response.headers['Content-Type'] = 'text/plain'
    balance = database.Database().getBalance(users.get_current_user())
    self.response.out.write('Your balance is %d' % balance)


application = webapp.WSGIApplication(
                                     [('/', MainPage),
                                      ('/balance', BalancePage)],
                                     debug=True)

def main():
  run_wsgi_app(application)

if __name__ == "__main__":
  main()
