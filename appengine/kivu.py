import os
import sys

import cgi
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from third_party.ezt import ezt

import database


# The path to the root of our resources.
_RESOURCE_ROOT = os.path.dirname(sys.modules[__name__].__file__)


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
    template = ezt.Template(os.path.join(_RESOURCE_ROOT, 'templates',
                                         'main.ezt'))
    template.generate(self.response.out, {})

class PostBalance(webapp.RequestHandler):
  @EnsureLoggedIn
  def post(self):
    database.Database().SetBalance(users.get_current_user(),
                                   cgi.escape(self.request.get('borrower')),
                                   cgi.escape(self.request.get('amount')))
    self.redirect('/balance')

class AddBalance(webapp.RequestHandler):
  @EnsureLoggedIn
  def get(self):
    self.response.headers['Content-Type'] = 'text/html'
    self.response.out.write("""
      <html>
        <body>
          <form action="/tmp_post_balance" method="post">
            borrower <div><input name="borrower" type="text"/></div>
            amount <div><input name="amount" type="text"/></div>
            <div><input type="submit" value="add balance"></div>
          </form>
        </body>
      </html>""")


class BalancePage(webapp.RequestHandler):
  @EnsureLoggedIn
  def get(self):  
    self.response.headers['Content-Type'] = 'text/plain'
    balance = database.Database().getBalance(users.get_current_user())
    if balance > 0:
      self.response.out.write('You\'re owed $%d' % balance)
    else:
      self.response.out.write('You owe $%d' % abs(balance))


application = webapp.WSGIApplication(
                                     [('/', MainPage),
                                      ('/balance', BalancePage),
                                      ('/add_balance', AddBalance),
                                      ('/tmp_post_balance', PostBalance),
                                     ],
                                     debug=True)

def main():
  run_wsgi_app(application)

if __name__ == "__main__":
  main()
