from blogapp import db
import datetime

class User(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(80), unique=False, nullable=False)
  fathername = db.Column(db.String(80), nullable=False)
  identitynumber = db.Column(db.String(120), unique=True, nullable=False)
  email = db.Column(db.String(120), unique=True, nullable=False)
  password = db.Column(db.String(120), nullable=False)
  
  #moneyreceiving = db.relationship("Moneyreceiving" , backref="User")
  #suppliesreceiving = db.relationship("Suppliesreceiving", backref="User")
  
  def __repr__(self):
        return '<User %r>' % self.username
  
class Moneyreceiving(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.String(80), unique=False, nullable=False)
    editdate = db.Column(db.DateTime, default = datetime.datetime.now, nullable=False)
    userid = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User',
        backref=db.backref('moneyreceivings', lazy=True))


class Suppliesreceiving(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.String(80), unique=False, nullable=False)
    userid = db.Column(db.Integer, db.ForeignKey('user.id'))
    editdate = db.Column(db.DateTime, default = datetime.datetime.now, nullable=False)
    category = db.relationship('User',
        backref=db.backref('suppliesreceivings', lazy=True))
#user = model.User(username="majidzare", fathername="Ali", identitynumber="5080075066", email="majidzarephysics@gmail.com", password=4311229569)
#money = model.Moneyreceiving(amount="500,000 rial")
#user.moneyreceivings.append(money)
#reguser[0].suppliesreceivings.append(sup)