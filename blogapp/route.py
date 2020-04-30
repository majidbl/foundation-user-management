from blogapp import app
from flask import render_template, redirect, request, url_for, flash, session, abort, Response
from blogapp import db
from blogapp.model import User, Moneyreceiving, Suppliesreceiving

from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user 

# flask-login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

login_manager.login_message_category = "info"

# silly user model
class Userlogin(UserMixin):

    def __init__(self, id):
        self.id = id
        self.name = "admin"
        self.password = "admin"


@app.route('/test/')
def test():
    return "Hello, World!"


@app.route('/')
def index():
    return render_template("home.html")
    

@app.route('/register', methods=["GET","POST"])
def register():
  if request.method == 'POST':
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']
    fathername = request.form["fathername"]
    identitynumber = request.form["identitynumber"]
      # TODO: write code...
    user = User(username=username, email=email, password=password, fathername=fathername, identitynumber=identitynumber)
    db.session.add(user)
    db.session.commit()
    #db.query.all()
    #for record in records:
      #print(record.username)
      # TODO: write code...
    flash(f'User Created','success')
    return redirect(url_for('index'))
  return render_template("register.html")
    
    
@app.route('/login' , methods=["GET","POST"])
def login():
  if request.method == 'POST':
    username = request.form['username']
    password = request.form['password']  
    Loginvalue = request.form['loginbtn']
    print("loginbtn value is : ", Loginvalue)
    if password == "admin" and username == "admin":
      user = Userlogin(1)
      login_user(user)
      return redirect(url_for('dashboard'))
    else:
      return abort(401)
  else:
    return render_template("login.html")
    
    
@app.route('/dashboard')
@login_required
def dashboard():
  users = db.session.query(User).all()
  return render_template("dashboard.html",   users = users)
    
    
# callback to reload the user object        
@login_manager.user_loader
def load_user(id=1):
    return Userlogin(id)
    
# handle login failed
@app.errorhandler(401)
def page_not_found(e):
    return Response('<p>Login failed</p>')

# somewhere to logout
@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You are Logout Successful","info")
    return redirect(url_for('index'))

    
@app.route('/dashboard/users/<int:id>', methods=["GET", "POST"])
@login_required
def profile(id):
  if request.method == "POST":
    btnvalue = request.form["btnvalue"]
    print(btnvalue)
    btnvalue = btnvalue.split()
    if btnvalue[0] == "AddMoney":
      user = db.session.query(User).filter_by(id=id).all()
      amount = request.form['donationmoney']
      temps = amount.replace(" ", "")
      if len(temps) == 0:
        flash('This field must not be empty', 'danger')
        redirect('/dashboard/users/id')
      else:
          moneyadded = Moneyreceiving(amount=amount)
          user[0].moneyreceivings.append(moneyadded)
          db.session.commit()
          redirect('/dashboard/users/id')
    if btnvalue[0] == "AddItem":
      user = db.session.query(User).filter_by(id=id).all()
      amount = request.form['donationitem']
      print(" amount is : ", amount)
      temps = amount.replace(" ", "")
      if len(temps) == 0:
        flash('This field must not be empty', 'danger')
        redirect('/dashboard/users/id')
      else:
          itemadded = Suppliesreceiving(amount=amount)
          user[0].suppliesreceivings.append(itemadded)
          db.session.commit()
          redirect('/dashboard/users/id')
    if btnvalue[0] == "deletemoney":
      print(btnvalue[0])
      print(btnvalue[1])
      moneydel = db.session.query(Moneyreceiving).filter_by(id=int(btnvalue[1])).all()
      db.session.delete(moneydel[0])
      db.session.commit()
    if btnvalue[0] == "deleteitem":
      print(btnvalue[0])
      print(btnvalue[1])
      itemdel = db.session.query(Suppliesreceiving).filter_by(id=int(btnvalue[1])).all()
      db.session.delete(itemdel[0])
      db.session.commit()
  money = Moneyreceiving.query.filter_by(userid=id).all()
  supply = Suppliesreceiving.query.filter_by(userid=id).all()
  user = User.query.filter_by(id=id).first()
  return render_template("profile.html", moneys=money, supplies=supply, user=user)