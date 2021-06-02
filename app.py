from flask import Flask, render_template, request, redirect, session, flash, make_response
from bson.json_util import loads, dumps
import database as db
import authentication
import ordermanagement as om
import logging

app = Flask(__name__)

# Set the secret key to some random bytes.
# Keep this really secret!
app.secret_key = b's@g@d@c0ff33!'

logging.basicConfig(level=logging.DEBUG)
app.logger.setLevel(logging.INFO)

@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html')

@app.route('/auth', methods = ['GET', 'POST'])
def auth():
    username = request.form.get('username')
    password = request.form.get('password')

    is_successful, user = authentication.login(username, password)
    app.logger.info('%s', is_successful)
    if(is_successful):
        session["user"] = user
        return redirect('/products')
    else:
        flash("Invalid username or password. Please try again.")
        return redirect('/')

@app.route('/logout')
def logout():
    session.pop("user",None)
    session.pop("cart",None)
    session.pop("order",None)
    return redirect('/')

@app.route('/')
def index():
    return render_template('index.html', page="Index")

@app.route('/products')
def products():
    product_list = db.get_products()
    return render_template('products.html', page="Products", product_list=product_list)

@app.route('/productdetails')
def productdetails():
    code = request.args.get('code', '')
    product = db.get_product(int(code))

    return render_template('productdetails.html', code=code, product=product)

@app.route('/branches')
def branches():
    branch_list = db.get_branches()
    return render_template('branches.html', page="Branches", branch_list=branch_list)

@app.route('/branchdetails')
def branchdetails():
    code = request.args.get('code', '')
    branch = db.get_branch(int(code))

    return render_template('branchdetails.html', page="Branches", branch=branch)

@app.route('/aboutus')
def aboutus():
    return render_template('aboutus.html', page="About Us")

@app.route('/addtocart')
def addtocart():
    code = request.args.get('code', '')
    product = db.get_product(int(code))
    item=dict()
    # A click to add a product translates to a 
    # quantity of 1 for now

    item["qty"] =  1
    item["name"] = product["name"]
    item["code"] = product["code"]
    item["subtotal"] = product["price"]*item["qty"]
    item["image"] = product["image"]
    item["price"] = product["price"]

    if(session.get("cart") is None):
        session["cart"]={}

    cart = session["cart"]
    cart[code]=item
    session["cart"]=cart
    return redirect('/cart')

@app.route('/updatecart', methods=['POST'])
def updatecart():
    code = request.form.getlist("code")
    qty = request.form.getlist("qty")

    cart = session["cart"]

    for item in range(len(code)):
        product = db.get_product(int(code[item]))
        cart[code[item]]["qty"] = int(qty[item])
        cart[code[item]]["subtotal"] = int(qty[item]) * int(product["price"])

    session["cart"] = cart
    
    return redirect('/cart')

@app.route('/deleteitem')
def deleteitem():
    code = request.args.get('code', '')
    cart = session["cart"]
    cart.pop(code, None)
    session["cart"]=cart

    return redirect('/cart')

@app.route('/deleteall')
def deleteall():
    session.pop('cart', None)
    return redirect('/cart')

@app.route('/cart')
def cart():
    return render_template('cart.html')

@app.route('/checkout')
def checkout():
    om.create_order_from_cart()
    session.pop("cart",None)
    return render_template('checkout.html')

@app.route('/order', methods=['GET', 'POST'])
def order():
    order=dict()

    firstName = request.form.get('firstName')
    lastName = request.form.get('lastName')
    address1 = request.form.get('address1')
    address2 = request.form.get('address2')
    city = request.form.get('city')
    state = request.form.get('state')
    zip = request.form.get('zip')
    phone = request.form.get('phone')
    email = request.form.get('email')
    socmed = request.form.get('socmed')
    notes = request.form.get('notes')

    order["firstName"] =  firstName
    order["lastName"] =  lastName
    order["address1"] =  address1
    order["address2"] =  address2
    order["city"] =  city
    order["state"] =  state
    order["zip"] =  zip
    order["phone"] =  phone
    order["email"] =  email
    order["socmed"] =  socmed
    order["notes"] =  notes
    
    if(session.get("order") is None):
        session["order"]={}

    session["order"] = order
    # clear cart in session memory upon checkout
    om.create_order_from_cart()
    # om.create_order()
    session.pop("cart",None)
    session.pop("order",None)
    return redirect('/ordercomplete')

@app.route('/ordercomplete')
def ordercomplete():
    return render_template('ordercomplete.html')


@app.route('/api/products',methods=['GET'])
def api_get_products():
    resp = make_response( dumps(db.get_products()) )
    resp.mimetype = 'application/json'
    return resp
    
@app.route('/api/products/<int:code>',methods=['GET'])
def api_get_product(code):
    resp = make_response(dumps(db.get_product(code)))
    resp.mimetype = 'application/json'
    return resp

@app.route('/password')
def changepassword():
    return render_template('changepassword.html')

@app.route('/password-auth', methods = ['POST'])
def passwordauth():
    old = request.form.get('old-password')
    new = request.form.get('new-password')
    confirm = request.form.get('confirm-password')

    is_successful, is_correct_old, is_same_new = authentication.change_password_verification(old, new, confirm)
    app.logger.info('%s', is_successful)
    if(is_successful):
        db.change_pass(session['user']['username'], new)
        return redirect('/login')
    else:
        if not is_correct_old:
            flash("Old password is not correct.")
        if not is_same_new:
            flash("Passwords do not match.")

        return redirect('/password')