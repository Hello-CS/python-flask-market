#This is used to package the files and allow them to be used
#Can delete market.py file since it is empty now 
#needs __init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import  LoginManager #manages your login functionalities

app = Flask(__name__)
#config is a dict that you can adjust and let flask recognize the database
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///market.db"
#key here is for login/register secret key
"""
Can be done easily by using python terminal
import os
os.urandom(12).hex()
"""
app.config['SECRET_KEY'] = '8dbc55e232becb491b6ab99d'
"""
Open up python in CLI with python 
from market import db
db.createall() to create db called market.db file
import Item
create items and add as such:
item1= Item(....)
db.session.add(item1)
db.session.commit()
Item.query.all() to see all items 
No need for id when creating because it is passed as primary key, and db will create itself

Can search with Item.query.filter_by(e.g. price=500) then you iterate over the object

We can go Google to search for DB Browser for Sqlite to be able to visually see what's in your db
Just need to select the db file when in the browser to open, and it will work

"""
db = SQLAlchemy(app)
bcrpyt = Bcrypt(app)
login_manager = LoginManager(app)
#Lets login manager know the login page so that login_required can work
login_manager.login_view = "login_page" 
login_manager.login_message_category = "info"
from market import routes