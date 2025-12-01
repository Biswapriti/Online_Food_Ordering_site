from flask import Flask, request, render_template, redirect, url_for, session, flash
from flask_cors import CORS
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
import os
import json
from dotenv import load_dotenv

app = Flask(__name__)
CORS(app)

# Load environment variables
load_dotenv()

# Use environment variables with fallback for development
# Production (Render) should set SECRET_KEY via environment variables
app.secret_key = os.getenv('SECRET_KEY', 'dev-fallback-key-change-in-production')

# Database connection (use environment variables)
def get_db_connection():
    db_config = {
        'host': os.getenv('DB_HOST'),
        'user': os.getenv('DB_USER'),
        'password': os.getenv('DB_PASSWORD'),
        'database': os.getenv('DB_NAME'),
        'port': int(os.getenv('DB_PORT', '3306'))
    }
    # Warn if required DB variables are missing
    for key, val in db_config.items():
        if key != 'port' and not val:
            print(f"WARNING: {key.upper()} environment variable not set")
    return mysql.connector.connect(**db_config)

# Attempt DB connection on startup; if it fails, app can still start
try:
    conn = get_db_connection()
except Exception as e:
    print(f"WARNING: Database connection failed on startup: {e}")
    print("App will start but database-dependent routes will fail until DB is available.")
    conn = None


def get_db_cursor(buffered=False):
    """Get a fresh database cursor, creating a new connection if needed."""
    global conn
    try:
        # Try to use existing connection
        if conn is not None:
            return conn.cursor(buffered=buffered)
        else:
            # Create a new connection if the global one is None
            conn = get_db_connection()
            return conn.cursor(buffered=buffered)
    except Exception as e:
        print(f"ERROR: Failed to get database cursor: {e}")
        raise

# Load Cloudinary mapping if present (created by the upload script)
_CLOUD_MAP_PATH = os.path.join(os.path.dirname(__file__), 'static', 'cloudinary_map.json')
def _load_cloud_map():
    try:
        with open(_CLOUD_MAP_PATH, 'r', encoding='utf-8') as fh:
            return json.load(fh)
    except Exception:
        return {}

_CLOUD_MAP = _load_cloud_map()


@app.context_processor
def inject_helpers():
    def cloud_image(filename):
        if not filename:
            return ''
        # If already an URL, return as-is
        if isinstance(filename, str) and (filename.startswith('http://') or filename.startswith('https://')):
            return filename
        # Lookup in cloud map, otherwise fall back to static
        return _CLOUD_MAP.get(filename, url_for('static', filename=filename))

    return dict(cloud_image=cloud_image)


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access this page', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    # redirect logged-in users to profile
    if 'user_id' in session:
        flash('You are already logged in', 'info')
        return redirect(url_for('profile'))

    if request.method == 'POST':
        try:
            username = request.form.get('username')
            password = request.form.get('password')

            cur = get_db_cursor()
            cur.execute("SELECT user_id, username, password FROM users WHERE username = %s", (username,))
            row = cur.fetchone()

            if row:
                user_id, uname, stored = row[0], row[1], row[2]
                # Try password hash verification first
                if check_password_hash(stored, password):
                    session['user_id'] = user_id
                    session['username'] = uname
                    flash('Logged in successfully', 'success')
                    return redirect(url_for('index'))
                else:
                    # Handle legacy plaintext password: if store equals provided password,
                    # upgrade to hashed password transparently and log user in.
                    if stored == password:
                        new_hash = generate_password_hash(password)
                        upd = get_db_cursor()
                        upd.execute("UPDATE users SET password = %s WHERE user_id = %s", (new_hash, user_id))
                        conn.commit()
                        session['user_id'] = user_id
                        session['username'] = uname
                        flash('Logged in and password upgraded to secure storage', 'success')
                        return redirect(url_for('index'))
                    flash('Invalid username or password', 'danger')
            else:
                flash('Invalid username or password', 'danger')
        except Exception as e:
            print(f"ERROR in login route: {e}")
            flash('Database error: unable to process login. Please try again later.', 'danger')

    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    # Prevent logged-in users from registering again
    if 'user_id' in session:
        flash('You are already registered and logged in', 'info')
        return redirect(url_for('profile'))

    if request.method == 'POST':
        try:
            username = request.form.get('username')
            password = request.form.get('password')
            email = request.form.get('email')

            if not username or not password:
                flash('Username and password are required', 'warning')
                return render_template('register.html')

            cur = get_db_cursor()
            cur.execute("SELECT user_id FROM users WHERE username = %s OR email = %s", (username, email))
            if cur.fetchone():
                flash('Username or email already exists', 'warning')
                return render_template('register.html')

            hashed = generate_password_hash(password)
            ins = get_db_cursor()
            ins.execute("INSERT INTO users (username, password, email) VALUES (%s, %s, %s)", (username, hashed, email))
            conn.commit()
            flash('Registration successful. Please log in.', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            print(f"ERROR in register route: {e}")
            flash('Database error: unable to process registration. Please try again later.', 'danger')
            return render_template('register.html')

    return render_template('register.html')

@app.route('/register_prompt')
def register_prompt():
    flash('Please register or log in to place an order', 'info')
    return redirect(url_for('register'))

@app.route('/veg_momo')
def veg_momo():
    return render_template('veg_momo.html')


@app.route('/menu')
def menu_page():
    # Render the full menu page (all momos)
    return render_template('all_momos.html')

@app.route('/cart', methods=['GET', 'POST'])
def cart():
    if 'cart_items' not in session:
        session['cart_items'] = []
    
    if request.method == 'POST':
        if request.is_json:
            try:
                cart_data = request.get_json()
                session['cart_items'] = cart_data
                session.modified = True
                
                # Calculate new totals
                subtotal = sum(item['price'] * item['quantity'] for item in cart_data)
                delivery_fee = 0 if subtotal >= 30 else 2
                total = subtotal + delivery_fee
                
                return {
                    'status': 'success',
                    'cart': session['cart_items'],
                    'totals': {
                        'subtotal': subtotal,
                        'delivery_fee': delivery_fee,
                        'total': total,
                        'free_delivery_remaining': max(0, 30 - subtotal)
                    }
                }
            except Exception as e:
                return {'status': 'error', 'message': str(e)}, 400
        else:
            # Handle form submission (traditional POST)
            try:
                item = {
                    "id": request.form['item_id'],
                    "name": request.form['item_name'],
                    "image": request.form['item_image'],
                    "price": float(request.form['item_price']),
                    "quantity": int(request.form['quantity']),
                    "category": request.form.get('category', ''),
                    "spicy": request.form.get('spicy', 'false').lower() == 'true'
                }
                
                # Check if item already in cart, update quantity if so
                found = False
                for cart_item in session['cart_items']:
                    if cart_item['id'] == item['id']:
                        cart_item['quantity'] += item['quantity']
                        found = True
                        break
                if not found:
                    session['cart_items'].append(item)
                
                session.modified = True
                return redirect(url_for('cart'))
            except Exception as e:
                return str(e), 400
    
    # GET request - show cart page
    cart_items = session.get('cart_items', [])
    subtotal = sum(item['price'] * item['quantity'] for item in cart_items)
    delivery_fee = 0 if subtotal >= 30 else 2
    total = subtotal + delivery_fee
    
    return render_template('cart.html', 
                         cart_items=cart_items,
                         subtotal=subtotal,
                         delivery_fee=delivery_fee,
                         total=total,
                         free_delivery_remaining=max(0, 30 - subtotal))

@app.route('/cart/update', methods=['POST'])
def update_cart_item():
    if request.is_json:
        try:
            data = request.get_json()
            item_id = data.get('id')
            quantity = int(data.get('quantity', 1))
            action = data.get('action', 'update')
            
            if action == 'remove':
                session['cart_items'] = [item for item in session['cart_items'] if item['id'] != item_id]
            else:
                for item in session['cart_items']:
                    if item['id'] == item_id:
                        if quantity > 0:
                            item['quantity'] = quantity
                        else:
                            session['cart_items'].remove(item)
                        break
            
            session.modified = True
            
            # Calculate new totals
            subtotal = sum(item['price'] * item['quantity'] for item in session['cart_items'])
            delivery_fee = 0 if subtotal >= 30 else 2
            total = subtotal + delivery_fee
            
            return {
                'status': 'success',
                'totals': {
                    'subtotal': subtotal,
                    'delivery_fee': delivery_fee,
                    'total': total,
                    'free_delivery_remaining': max(0, 30 - subtotal)
                }
            }
        except Exception as e:
            return {'status': 'error', 'message': str(e)}, 400
    return {'status': 'error', 'message': 'Invalid request'}, 400

@app.route('/cart/clear', methods=['POST'])
def clear_cart():
    if request.is_json:
        session.pop('cart_items', None)
        session.modified = True
        return {'status': 'success', 'cart': []}
    else:
        session.pop('cart_items', None)
        session.modified = True
        return redirect(url_for('cart'))


@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    # Check if user is registered/logged in before allowing checkout
    if 'user_id' not in session:
        flash('Please register or log in to place an order', 'warning')
        return redirect(url_for('register'))
    
    # Prepare cart and totals similar to cart view
    cart_items = session.get('cart_items', [])
    subtotal = sum(item['price'] * item['quantity'] for item in cart_items)
    delivery_fee = 0 if subtotal >= 30 else 2
    total = subtotal + delivery_fee

    if request.method == 'POST':
        # Persist the order to the database if possible, otherwise show success without persistence.
        name = request.form.get('name')
        email = request.form.get('email')
        address = request.form.get('address')
        payment = request.form.get('payment', 'cod')

        order_data = {
            'name': name,
            'email': email,
            'address': address,
            'items': cart_items,
            'total': total,
            'payment': payment,
            'order_id': None
        }

        try:
            # ensure orders table exists
            curc = get_db_cursor()
            curc.execute('''
                CREATE TABLE IF NOT EXISTS orders (
                    order_id INT PRIMARY KEY AUTO_INCREMENT,
                    user_id INT NULL,
                    name VARCHAR(255),
                    email VARCHAR(255),
                    total DECIMAL(10,2),
                    address TEXT,
                    items TEXT,
                    payment VARCHAR(32),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            conn.commit()

            ins = get_db_cursor()
            items_json = json.dumps(cart_items, default=str)
            uid = session.get('user_id')
            ins.execute("INSERT INTO orders (user_id, name, email, total, address, items, payment) VALUES (%s,%s,%s,%s,%s,%s,%s)",
                        (uid, name, email, float(total), address, items_json, payment))
            conn.commit()
            order_id = ins.lastrowid
            order_data['order_id'] = order_id

            # Attempt to save address to users table for logged-in users
            if uid:
                try:
                    upd = get_db_cursor()
                    upd.execute("ALTER TABLE users ADD COLUMN IF NOT EXISTS address TEXT")
                except Exception:
                    # Some MySQL versions don't support IF NOT EXISTS with ALTER ADD COLUMN; ignore
                    pass
                try:
                    upd2 = get_db_cursor()
                    upd2.execute("UPDATE users SET address = %s WHERE user_id = %s", (address, uid))
                    conn.commit()
                except Exception:
                    # ignore if column missing
                    pass

        except Exception as e:
            # If persistence fails, continue gracefully and show success page.
            print('Order persistence failed:', e)

        # clear cart
        session.pop('cart_items', None)
        session.modified = True
        return render_template('order_success.html', order=order_data)

    return render_template('checkout.html', cart_items=cart_items, subtotal=subtotal, delivery_fee=delivery_fee, total=total)


@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('username', None)
    flash('You have been logged out', 'info')
    return redirect(url_for('index'))


@app.route('/profile')
@login_required
def profile():
    cur = get_db_cursor()
    cur.execute("SELECT user_id, username, email, created_at FROM users WHERE user_id = %s", (session.get('user_id'),))
    row = cur.fetchone()
    user = None
    if row:
        user = {
            'user_id': row[0],
            'username': row[1],
            'email': row[2],
            'created_at': row[3]
        }
    # Attempt to load past orders from an `orders` table if present.
    orders = []
    try:
        cur2 = get_db_cursor(buffered=True)
        # expected orders table (order_id, user_id, total, address, items (JSON), created_at)
        cur2.execute("SELECT order_id, total, address, items, created_at FROM orders WHERE user_id = %s ORDER BY created_at DESC", (user['user_id'],))
        rows = cur2.fetchall()
        for r in rows:
            items = []
            try:
                items = json.loads(r[3]) if r[3] else []
            except Exception:
                # if items stored differently, keep raw
                items = r[3]
            orders.append({
                'order_id': r[0],
                'total': r[1],
                'address': r[2],
                'items': items,
                'created_at': r[4]
            })
    except Exception:
        # If the orders table doesn't exist or query fails, show empty list — avoid breaking the profile.
        orders = []

    # Load saved address from users table if present (non-breaking)
    saved_address = None
    try:
        cur3 = get_db_cursor()
        cur3.execute("SELECT address FROM users WHERE user_id = %s", (user['user_id'],))
        ar = cur3.fetchone()
        if ar:
            saved_address = ar[0]
    except Exception:
        saved_address = session.get('profile_address')

    return render_template('profile.html', user=user, orders=orders, saved_address=saved_address)


@app.route('/profile/address', methods=['POST'])
@login_required
def save_profile_address():
    # Collect common address fields and format into a single text block
    line1 = request.form.get('line1', '').strip()
    line2 = request.form.get('line2', '').strip()
    city = request.form.get('city', '').strip()
    state = request.form.get('state', '').strip()
    zipcode = request.form.get('zipcode', '').strip()
    phone = request.form.get('phone', '').strip()

    if not line1 or not city or not phone:
        flash('Please provide at least address line 1, city and phone number', 'warning')
        return redirect(url_for('profile'))

    address_text = f"{line1}" + (f"\n{line2}" if line2 else "") + f"\n{city}, {state} - {zipcode}\nPhone: {phone}"

    try:
        cur = get_db_cursor()
        cur.execute("UPDATE users SET address = %s WHERE user_id = %s", (address_text, session.get('user_id')))
        conn.commit()
        flash('Address saved to your profile', 'success')
    except Exception:
        # If the users table doesn't have an `address` column, fall back to session storage and notify the user
        session['profile_address'] = address_text
        session.modified = True
        flash('Address saved locally for this session. To persist permanently, add an `address` column to the `users` table.', 'warning')

    return redirect(url_for('profile'))


@app.route('/contact_submit', methods=['POST'])
def contact_submit():
    name = request.form.get('name', '').strip()
    email = request.form.get('email', '').strip()
    subject = request.form.get('subject', '').strip()
    message = request.form.get('message', '').strip()

    if not name or not email or not subject or not message:
        flash('All fields are required', 'warning')
        return redirect(url_for('index'))

    try:
        # Create contacts table if it doesn't exist
        curc = get_db_cursor()
        curc.execute('''
            CREATE TABLE IF NOT EXISTS contacts (
                contact_id INT PRIMARY KEY AUTO_INCREMENT,
                name VARCHAR(255),
                email VARCHAR(255),
                subject VARCHAR(255),
                message TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()

        # Insert the contact message
        ins = get_db_cursor()
        ins.execute("INSERT INTO contacts (name, email, subject, message) VALUES (%s,%s,%s,%s)",
                    (name, email, subject, message))
        conn.commit()
        flash('Thank you for your message! We will get back to you soon.', 'success')
    except Exception as e:
        print('Contact form submission failed:', e)
        flash('An error occurred. Please try again.', 'danger')

    return redirect(url_for('index') + '#contact')


if __name__ == '__main__':
    app.run(debug=True)