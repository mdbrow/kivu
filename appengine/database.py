from google.appengine.ext import db
from google.appengine.api import users

class Balance(db.Model):
  lender = db.UserProperty()
  borrower = db.UserProperty()
  balance = db.IntegerProperty()

class Database():
  def __init__(self):
    pass

  def getBalance(self, user):
    accounts_receivable = db.GqlQuery(("SELECT * FROM Balance WHERE "
                                       "lender = :1 ORDER BY borrower"), user)
    accounts_payable = db.GqlQuery(("SELECT * FROM Balance WHERE "
                                    "borrower = :1 ORDER BY lender"), user)
    total_balance = 0
    for b in accounts_receivable:
      total_balance += b.balance
    for b in accounts_payable:
      total_balance -= b.balance
    return total_balance

  def SetBalance(self, user, borrower, amount): 
    b = Balance()
    b.lender = user
    b.borrower = users.User(borrower)
    b.balance = int(amount)
    b.put()

