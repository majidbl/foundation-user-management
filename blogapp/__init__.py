from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

from . import route
from . import model

#model.User.invoices = relationship("Invoice", order_by = Invoice.id, back_populates = "customer")
#if __name__ == "__main__":
  #app.run(debug=True)