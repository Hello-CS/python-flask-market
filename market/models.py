from market import db, login_manager
from market import bcrpyt
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(length=30), nullable=False, unique=True)
    email_address = db.Column(db.String(length=50), nullable=False, unique=True)
    #we want to store password not as plain text, so we don't store it in that name as well
    password_hash = db.Column(db.String(length=60), nullable=False) #Use 60 because the hash libraries used w Flask all give 60
    budget = db.Column(db.Integer(), nullable=False, default=5000)
    #Relationship between items, note it is not stored as a column
    #backref back references to the user model, to see the owner of specific items
    #lazy=True is set so that SQLAlchemy will grab all the items in 1 shot
    items = db.relationship('Item', backref='owned_user', lazy=True)

    @property #Just an additional attribute that is going to be accessible for each instance
    def password(self):
        return self.password

    #using setter and getter to edit password
    @password.setter   
    def password(self, plain_text_password):
            self.password_hash = bcrpyt.generate_password_hash(plain_text_password).decode('utf-8')
    
    def check_password_correction(self, attempted_password):
        return bcrpyt.check_password_hash(self.password_hash, attempted_password)
    
    @property
    def prettier_budget(self):
        if len(str(self.budget)) >= 4:
            return f"${str(self.budget)[:-3]},{str(self.budget)[-3:]}"
        else:
            return f"{self.budget}$"

    def can_purchase(self,item_obj):
        return self.budget >= item_obj.price

    def can_sell(self, item_obj):
        return item_obj in self.items

class Item(db.Model): #creating model for items via class
    id = db.Column(db.Integer(), primary_key=True) #setting id as the primary key
    name = db.Column(db.String(length=30), nullable=False, unique=True) #length is max length
    price = db.Column(db.Integer(), nullable=False,)
    barcode = db.Column(db.String(length=12), nullable=False, unique=True)
    description = db.Column(db.String(length=1000), nullable=False, unique=True)
    #relates to the primary key of users, to see who owns the item
    owner = db.Column(db.Integer(), db.ForeignKey('user.id'))

    #To represent your class objects in string or wtv way you want
    def __repr__(self):
        return f'Item {self.name}'

    def buy(self,user):
        self.owner = user.id
        user.budget -= self.price
        db.session.commit()
    
    def sell(self, user):
        self.owner = None
        user.budget += self.price
        db.session.commit()


    """
    To add r/s, in terminal Python
    Create item and user.
    Then, filter for item
    item1 = Item.query.filter_by(...).first() Use first() because it returns an object and you want the 1st item
    item1.owner = User.query.filter_by(username=...).first().id reason you use id is because you set foreign key as user.id
    db.session.add(item1)
    db.commit()

    After this, you can check the reference as such
    i = Item.query.filter_by(name=...same name).first()
    i.owned_user will show the reference of which user
    i.owner will show if there is an owner (will show 1) or none
    """