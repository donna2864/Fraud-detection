# ----------------------- IMPORTING MODULES ------------------------------------ #
from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify, send_from_directory, get_flashed_messages
import requests
from datetime import datetime
import pandas as pd
import numpy as np
from xgboost import XGBClassifier
import joblib
import pickle
from sklearn.preprocessing import LabelEncoder
from scipy import stats
from email_validator import validate_email, EmailNotValidError
from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash
from bson.objectid import ObjectId

# ----------------------- ML MODEL DECLARATIONS ------------------------------------ #
rf = joblib.load("random_forest_model.pkl")
xgb = joblib.load("xgboost_model.pkl")
log = joblib.load("logistic_model.pkl")

with open('ensemble_modell.pkl', 'rb') as f:
    ensemble_data = pickle.load(f)
weights = ensemble_data['weights']

def ensemble_predict(X_input):
    base_preds = np.column_stack([
        log.predict_proba(X_input)[:, 1],
        xgb.predict_proba(X_input)[:, 1],
        rf.predict_proba(X_input)[:, 1]
    ])
    final_score = np.dot(base_preds, weights)
    return int(final_score > 0.5), float(final_score)

# ----------------------- RENDER APP ------------------------------------ #
app = Flask(__name__, template_folder="pages")

app.secret_key = '9f6b3decd6c44932b9e00f4e8c258af9'  # Needed for flashing messages

# ----------------------- MONGO DB CONNECTION AND COLLECTIONS ------------------------------------ #
client = MongoClient('mongodb://localhost:27017/')
db = client['fraud_detection']
products_collection = db['products']
users_collection = db['users']
cart_collection = db['cart']

# ----------------------- SERVING FILES ------------------------------------ #
@app.route('/images/<path:filename>')
def serve_images(filename):
    return send_from_directory('images', filename)

@app.route('/styles/<path:filename>')
def serve_styles(filename):
    return send_from_directory('styles', filename)

@app.route('/')
def home():
    return render_template('index.html')

# ----------------------- VPN DETECTION MODULE ------------------------------------ #
def get_real_ip():
    try:
        return requests.get("https://api64.ipify.org?format=json").json()["ip"]
    except Exception as e:
        # print(f"Error getting real IP: {e}")
        return request.remote_addr  # fallback
    
def get_ip_info(ip_address):
    api_key = "1d22d76e62d4446880560caada4f8427"
    url = f'https://vpnapi.io/api/{ip_address}?key={api_key}'
    try:
        res = requests.get(url)
        res.raise_for_status()
        return res.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching IP information: {e}")
        return None
    
# ----------------------- LOGIN ROUTING + VPN DETECTION ------------------------------------ #
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # # Get IP address of user
        # ip_address = get_real_ip() # IP without vpn
        ip_address = "45.62.123.4"  # IP With vpn

        ip_data = get_ip_info(ip_address)

        is_vpn = ip_data and ip_data.get('security', {}).get('vpn', False)

        email = request.form['email']
        password = request.form['password']

        user = users_collection.find_one({'email': email})
        if user and check_password_hash(user['password'], password):
            session['user_name'] = user['name']
            session['user_id'] = str(user['_id'])  
            
            # Flash VPN alert here
            if is_vpn:
                flash("VPN Detected! You are using a VPN connection. You are being monitored", "vpn")
            else:
                flash("No VPN detected. You are on a normal connection.", "vpn")
            
            #on successful login
            return redirect(url_for('healthAndBeauty'))

        else:
            flash("Invalid email or password.")
            return redirect(url_for('login'))

    return render_template('Login.html')

# ----------------------- EMAIL VALIDATION  ------------------------------------ #
def validate_user_email(email):
    try:
        v = validate_email(email)
        return f"✅ '{email}' is a valid email address."
    except EmailNotValidError as e:
        return f"❌ Email validation error: {str(e)}"
    
def check_breaches(email):
    url = f"https://api.xposedornot.com/v1/check-email/{email}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            if data.get("breaches"):
                breaches = [f"🔴 {b['breach_name']} (Leaked: {b['leak_date']})" for b in data["breaches"]]
                return "\n".join(breaches)
            else:
                return "✅ No known breaches found."
        elif response.status_code == 404:
            return "✅ No breach data found."
        else:
            return f"⚠️ Unexpected response: {response.status_code}"
    except Exception as e:
        return f"❌ Error checking breaches: {e}"
    
def check_email_activity(email):
    api_key = "2550ddf39b5d4eb48dc46c1d8a54e71b"
    try:
        url = f"https://emailvalidation.abstractapi.com/v1/?api_key={api_key}&email={email}"
        response = requests.get(url)
        data = response.json()
        return f"📬 Deliverability: {data.get('deliverability')}"
    except Exception as e:
        return f"❌ Error checking Abstract API: {e}"
    
def find_related_emails(email):
    api_key = "34b11512752ce32168664e4110d962c79f8f7a90"
    domain = email.split('@')[-1]
    try:
        url = f"https://api.hunter.io/v2/domain-search?domain={domain}&api_key={api_key}"
        response = requests.get(url)
        data = response.json()
        emails = data.get("data", {}).get("emails", [])
        return "\n".join([f"📧 {e.get('value')} (Type: {e.get('type')})" for e in emails[:5]]) if emails else "✅ No related emails found."
    except Exception as e:
        return f"❌ Error querying Hunter API: {e}"
    
# ----------------------- REGISTRATION ROUTING + EMAIL VALIDATION ------------------------------------ #
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        age = request.form['age']
        device = request.form['device']
        account_age_days = request.form['account_age_days']

        if password != confirm_password:
            flash("Passwords do not match.")
            return redirect(url_for('register'))

        if users_collection.find_one({'email': email}):
            flash("Email already registered.")
            return redirect(url_for('register'))

        # 1. Validate Email Format
        email_validation_result = validate_user_email(email)
        if "❌" in email_validation_result:
            flash(email_validation_result, "error")
            return redirect(url_for('register'))

        # 2. Check for breaches
        breach_result = check_breaches(email)
        if "🔴" in breach_result:  # Found breaches
            flash(f"❌ Cannot register. Breach detected:\n{breach_result}", "error")
            return redirect(url_for('register'))

        # 3. Check Email Activity
        email_activity_result = check_email_activity(email)
        if ("UNDELIVERABLE" in email_activity_result.upper()) or ("DELIVERABILITY: UNDELIVERABLE" in email_activity_result.upper()):
            flash(f"❌ Cannot register. Email not deliverable.\n{email_activity_result}", "error")
            return redirect(url_for('register'))
        
        #4. Check Related Emails
        related_emails_result = find_related_emails(email)
        if "📧" in related_emails_result:   # Related emails found
            flash(f"⚠️ Warning: Related emails found in public records:\n{related_emails_result}", "error")
            return redirect(url_for('register'))
        
        #added validated users to the database
        hashed_password = generate_password_hash(password)
        users_collection.insert_one({'name': name, 'email': email, 'password': hashed_password, 'Customer Age': age, 'Device Used':device, 'Account Age Days': account_age_days})
        flash("Registered successfully. Please log in.", "success")
        return redirect(url_for('login'))

    return render_template('SignUp.html')

# ----------------------- FORGOT PASSWORD ROUTING------------------------------------ #
@app.route('/forgot-password', methods=['GET', 'POST'])
def forgotPassword():
    if request.method == 'POST':
        email = request.form['email']
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')

        if new_password != confirm_password:
            flash("Passwords do not match.")
            return redirect(url_for('forgotPassword'))

        user = users_collection.find_one({'email': email})
        if user:
            hashed_password = generate_password_hash(new_password)
            users_collection.update_one({'email': email}, {'$set': {'password': hashed_password}})
            flash("Password updated successfully. Please log in.")
            return redirect(url_for('login'))
        else:
            flash("Email not found.")
            return redirect(url_for('forgotPassword'))
        
    #on successful reset of password
    return render_template('forgotPassword.html')

# ----------------------- MODEL PERFORMANCE PAGE ROUTING------------------------------------ #
@app.route('/performance')
def performance():
    return render_template('performance.html')

# ----------------------- PRODUCTS PAGE CATEGORY-WISE ROUTING------------------------------------ #
@app.route('/products/<category>')
def show_products(category):
    products = list(products_collection.find({"category": category}))
    user_name = session.get('user_name', 'Guest')  # Fallback if user not logged in
    return render_template('categoryPage.html', products=products, category=category, user_name=user_name)

@app.route('/healthAndBeauty')
def healthAndBeauty():
    return redirect(url_for('show_products', category='Health & Beauty'))

@app.route('/ToysAndGames')
def ToysAndGames():
    return redirect(url_for('show_products', category='Toys & Games'))

@app.route('/homeAndGarden')
def homeAndGarden():
    return redirect(url_for('show_products', category='Home & Garden'))

@app.route('/clothing')
def clothing():
    return redirect(url_for('show_products', category='Clothing'))

@app.route('/electronics')
def electronics():
    return redirect(url_for('show_products', category='Electronics'))

# ----------------------- PRODUCT-WISE ROUTING------------------------------------ #
@app.route('/product/<product_id>')
def product_detail(product_id):
    from bson.objectid import ObjectId
    product = products_collection.find_one({'_id': ObjectId(product_id)})
    if not product:
        flash("Product not found.")
        return redirect(url_for('home'))
    
    user_name = session.get('user_name', 'Guest')
    return render_template('productPage.html', product=product, user_name=user_name)

# ----------------------- ADD TO CART ROUTING + OPERATIONS ------------------------------------ #
@app.route('/add_to_cart/<product_id>', methods=['POST'])
def add_to_cart(product_id):
    quantity = int(request.form['quantity'])
    user_name = session.get('user_name', 'Guest')
    
    if not user_name:
        flash("You need to log in to add items to the cart.")
        return redirect(url_for('login'))

    product = products_collection.find_one({'_id': ObjectId(product_id)})
    if not product:
        flash("Product not found.")
        return redirect(url_for('home'))
    
    cart_item = {
        'product_id': product['_id'],
        'name': product['name'],
        'category': product['category'],
        'price': product['price'],
        'image': product['image'],
        'quantity': quantity,
        'user_name': user_name
    }

    cart_collection.update_one(
        {'user_name': user_name, 'product_id': product['_id']},
        {'$set': cart_item},
        upsert=True
    )
    
    flash(f"{product['name']} has been added to your cart.")
    return redirect(url_for('cart'))

@app.route('/cart')
def cart():
    user_name = session.get('user_name', 'Guest')
    if not user_name:
        flash("You need to log in to view your cart.")
        return redirect(url_for('login'))
    
    cart_items = list(cart_collection.find({'user_name': user_name}))
    total = sum(item['price'] * item['quantity'] for item in cart_items)
    
    return render_template('cart.html', cart_items=cart_items, total=total, user_name=user_name)

@app.route('/update_cart_item/<item_id>', methods=['POST'])
def update_cart_item(item_id):
    quantity = int(request.form['quantity'])
    cart_collection.update_one(
        {'_id': ObjectId(item_id)},
        {'$set': {'quantity': quantity}}
    )
    flash("Cart updated successfully.")
    return redirect(url_for('cart'))

@app.route('/remove_from_cart/<item_id>')
def remove_from_cart(item_id):
    cart_collection.delete_one({'_id': ObjectId(item_id)})
    flash("Item removed from cart.")
    return redirect(url_for('cart'))

# ----------------------- DATA PREPARATION FOR MODEL PREDICTION ------------------------------------ #

# Define mappings for categorical variables
age_cat_map = {'<25': 0, '25-34': 1, '35-44': 2, '45-54': 3, '55+': 4}
hour_bin_map = {'Night': 0, 'Morning': 1, 'Afternoon': 2, 'Evening': 3}
payment_method_map = {"debit card": 0, "credit card": 1, "PayPal": 2, "bank transfer": 3}
product_category_map = {"Home & Garden": 0, "Electronics": 1, "Toys & Games": 2, "Clothing": 3, "Health & Beauty": 4}
device_used_map = {"desktop": 0, "mobile": 1, "tablet": 2}

def categorize_age(age):
    if age < 25:
        return '<25'
    elif age < 35:
        return '25-34'
    elif age < 45:
        return '35-44'
    elif age < 55:
        return '45-54'
    else:
        return '55+'

def bin_hour(hour):
    if 0 <= hour < 6:
        return 'Night'
    elif 6 <= hour < 12:
        return 'Morning'
    elif 12 <= hour < 18:
        return 'Afternoon'
    else:
        return 'Evening'

def preprocess_input(data):
    df = pd.DataFrame([data])

    # Feature engineering
    df['Quantity_Log'] = np.log1p(df['Quantity'])
    df['Account_Age_Weeks'] = df['Account Age Days'] // 7
    df['Age_Category'] = df['Customer Age'].apply(categorize_age)
    df['Hour_Bin'] = df['Transaction Hour'].apply(bin_hour)
    df['Amount_zscore'] = (df['Transaction Amount'] - 229.36709867140559) / 282.04666899189573

    # Encode categorical features
    df['Payment Method'] = df['Payment Method'].map(payment_method_map)
    df['Product Category'] = df['Product Category'].map(product_category_map)
    df['Device Used'] = df['Device Used'].map(device_used_map)
    df['Age_Category'] = df['Age_Category'].map(age_cat_map)
    df['Hour_Bin'] = df['Hour_Bin'].map(hour_bin_map)

    # Define final columns in order
    features = ['Transaction Amount', 'Amount_zscore', 'Payment Method', 'Product Category',
                'Quantity', 'Quantity_Log', 'Customer Age', 'Age_Category',
                'Device Used', 'Account Age Days', 'Account_Age_Weeks',
                'Transaction Hour', 'Hour_Bin']

    if df[features].isnull().any().any():
        print("⚠️ NaNs detected in input:")
        print(df[features].isnull().sum())
        print(df[features])

    return df[features]


def get_cart_items_for_user(user_name):
    try:
        return list(db.cart.find({'user_name': user_name}))
    except Exception as e:
        print(f"Error fetching cart items: {e}")
        return []


def get_user_profile(user_id_str):  # now expects a string
    try:
        # Check if the user_id_str is a valid ObjectId string
        if not ObjectId.is_valid(user_id_str):
            raise ValueError("Invalid ObjectId format.")
        
        # Convert to ObjectId
        user_id = ObjectId(user_id_str)
        
        # Fetch the user from the database
        return db.users.find_one({'_id': user_id})
    
    except ValueError as e:
        print(f"Error: {e}")
        return {}  # return empty if invalid ObjectId format
    except Exception as e:
        print(f"Error fetching user profile: {e}")
        return {}

# ----------------------- MODEL PREDICTION ON CHECKOUT ROUTING------------------------------------ #

@app.route("/checkout", methods=["POST"])
def checkout():
    try:
        # 1. Check for user session
        user_id_str = session.get('user_id')
        if not user_id_str:
            flash("Please log in to continue.")
            return redirect(url_for('login'))

        try:
            user_id = ObjectId(user_id_str)
        except Exception:
            return "Invalid user ID format", 400

        user_name = session.get('user_name')
        if not user_name:
            flash("Please log in to continue.")
            return redirect(url_for('login'))
        
        # 2. Get form values
        payment_method = request.form.get("payment_method")

        # 3. Get cart and user info using helper functions
        cart_items = get_cart_items_for_user(user_name)
        user = get_user_profile(ObjectId(user_id))

        if not cart_items:
            return "Cart is empty", 400
        if not user:
            return "User not found", 404

        # 4. Get first item in cart
        first_item = cart_items[0]
        product_category = first_item['category']
        quantity = first_item['quantity']

        # 5. Calculate amount
        total = sum(item['price'] * item['quantity'] for item in cart_items) + 4  # Add shipping

        # 6. Get transaction hour
        transaction_hour = datetime.now().hour

        # 7. User details
        try:
            customer_age = int(user.get('age', 0))
        except ValueError:
            customer_age = 0

        try:
            account_age_days = int(user.get('account_age_days', 0))
        except ValueError:
            account_age_days = 0

        device_used = user.get('device', 'desktop') 

        # 8. Create transaction data
        transaction_data = {
            "Transaction Amount": total,
            "Payment Method": payment_method,
            "Product Category": product_category,
            "Quantity": quantity,
            "Customer Age": customer_age,
            "Device Used": device_used,
            "Account Age Days": account_age_days,
            "Transaction Hour": transaction_hour
        }

        # 9. Insert into transactions
        transaction_id = db.transactions.insert_one(transaction_data).inserted_id

        # 10. Preprocess and predict
        processed = preprocess_input(transaction_data)
        prediction, prob = ensemble_predict(processed)

        # 11. Update transaction with result
        db.transactions.update_one(
            {"_id": transaction_id},
            {"$set": {"is_fraud": prediction, "fraud_score": round(prob, 4)}}
        )

        # 12. Show result page
        return render_template("checkout_result.html", is_fraud=prediction, prob=round(prob * 100, 2))

    except Exception as e:
        return f"Error: {str(e)}", 500

# ----------------------- START POINT FOR THE APP ------------------------------------ #
if __name__ == '__main__':
    app.run(debug=True)