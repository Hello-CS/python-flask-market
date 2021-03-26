from market import app
from flask import render_template, redirect, url_for, flash, request
from market.forms import RegisterForm, LoginForm, PurchaseForm,SellForm
from market import db #reason why you can import from market package is because it's in the init file
from flask_login import login_user, logout_user, login_required, current_user
from market.models import User, Item

@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')

@app.route('/market', methods=['GET','POST'])
@login_required
def market_page():
    purchase_form = PurchaseForm()
    sell_form = SellForm()
    """
    Note that validate_on_submit() will create the confirm form submission everytime you refresh
    because it expects a form. Not useful for this unlike login and register
    However, we have a request module to use now which helps us differentiate GET and POST request unlike
    this validate function
    Lesson: Assuming we use validate_on_submit()
    if purchase_form.validate_on_submit():
        #print(purchase_form.__dict__) Note this __dict__ magic func will open up the object for you to see
        #printing it shows that there is a submit object purchase_form['submit'] that outputs a html line
        #<input id="submit" name="submit" type="submit" value="Purchase">
        #We implement this in the modal to be able to find variables easier
        #We use flask's request module to help us faciliate getting of item
    """
    if request.method == "POST":
        #Purchase item logic
        purchased_item = request.form.get('purchased_item') #outputs name of item
        p_item_object = Item.query.filter_by(name=purchased_item).first()
        if p_item_object:
            if current_user.can_purchase(p_item_object):
                p_item_object.buy(current_user)
                flash(f"Product {p_item_object.name} has been purchased!", category='success')
            else:
                flash(f"Insufficient funds to purchase {p_item_object.name}", category='danger')
        #Sell item logic
        sold_item = request.form.get('sold_item')
        s_item_object = Item.query.filter_by(name=sold_item).first()
        if s_item_object:
            if current_user.can_sell(s_item_object):
                s_item_object.sell(current_user)
                flash(f"Product {s_item_object.name} has been sold!", category='success')
            else:
                flash(f"Something went wrong! Unable to sell {s_item_object.name}", category='danger')   
                
        return redirect(url_for("market_page"))

    if request.method == "GET":   
        items = Item.query.filter_by(owner=None)
        owned_items = Item.query.filter_by(owner=current_user.id)
        return render_template('market.html', items=items, purchase_form=purchase_form, owned_items=owned_items, sell_form=sell_form)

@app.route('/register', methods=['GET','POST']) #Put methods so you can enable these methods in the route 
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        user_to_create = User(username=form.username.data,
                                email_address=form.email_address.data,
                                password=form.password1.data)
        db.session.add(user_to_create)
        db.session.commit()
        login_user(user_to_create)
        flash(f'Account successfully created! You are logged in as {user_to_create.username}!', category='success')
        return redirect(url_for('market_page'))
    if form.errors != {}: #errors if any are in a dictionary, check if got any errors
        for err in form.errors.values():
            #flash instead of print. Builtin function of flask to display your messages on html
            #get_flashed_messages is the api to use the messages you flash
            flash(f'There was an error with creating user: {err}', category='danger')  

    return render_template('register.html', form=form)

@app.route('/login', methods=['GET','POST'])
def login_page():
    form = LoginForm()
    #this method does 2 things - validate and acts on submit
    if form.validate_on_submit(): 
        attempted_user = User.query.filter_by(username=form.username.data).first()
        if attempted_user and attempted_user.check_password_correction(
            attempted_password=form.password.data
        ):
            login_user(attempted_user)
            flash(f'Login success! You are logged in as: {attempted_user.username}', category='success')
            return redirect(url_for('market_page'))
        else:
            flash('Username and password do not match! Please try again', category='danger')
            
    return render_template('login.html', form=form)

@app.route('/logout')
def logout_page():
    logout_user()
    flash('You have logged out', category='info')
    return redirect(url_for("home_page"))


"""
Dynamic Routes can be inserted as such (Using <> to get parameters)
@app.route('/<username>')
def new_route(username):
    return f"This page is for {username}"

Can use variables with the render_template() method using Jinja
return render_template('market.html', item_name="Phone")
Then in the html, use {{ item_name  }}
"""