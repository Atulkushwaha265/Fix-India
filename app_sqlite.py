from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
import sqlite3
import math
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = 'nearfix_secret_key_2024'

# SQLite Database Configuration
DATABASE = 'nearfix.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_database():
    if not os.path.exists(DATABASE):
        conn = get_db_connection()
        
        # Create tables
        conn.execute('''
            CREATE TABLE users (
                user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                full_name TEXT NOT NULL,
                phone TEXT,
                address TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.execute('''
            CREATE TABLE services (
                service_id INTEGER PRIMARY KEY AUTOINCREMENT,
                service_name TEXT NOT NULL,
                description TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.execute('''
            CREATE TABLE helpers (
                helper_id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                full_name TEXT NOT NULL,
                phone TEXT,
                service_type_id INTEGER,
                latitude REAL,
                longitude REAL,
                is_available BOOLEAN DEFAULT 1,
                is_approved BOOLEAN DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (service_type_id) REFERENCES services(service_id)
            )
        ''')
        
        conn.execute('''
            CREATE TABLE service_requests (
                request_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                helper_id INTEGER,
                service_type_id INTEGER NOT NULL,
                title TEXT NOT NULL,
                description TEXT NOT NULL,
                user_latitude REAL,
                user_longitude REAL,
                user_address TEXT,
                status TEXT DEFAULT 'pending',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(user_id),
                FOREIGN KEY (helper_id) REFERENCES helpers(helper_id),
                FOREIGN KEY (service_type_id) REFERENCES services(service_id)
            )
        ''')
        
        conn.execute('''
            CREATE TABLE admins (
                admin_id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                full_name TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Insert default services
        services = [
            ('Plumber', 'Fixing pipes, leaks, drainage issues'),
            ('Electrician', 'Electrical repairs, wiring, appliance installation'),
            ('Car Mechanic', 'Car repair and maintenance services'),
            ('Bike Mechanic', 'Bike repair and maintenance services'),
            ('AC Repair', 'Air conditioner repair and maintenance'),
            ('Carpenter', 'Woodwork, furniture repair'),
            ('Painter', 'Painting services for walls and furniture'),
            ('Cleaning', 'Home and office cleaning services')
        ]
        
        conn.executemany('INSERT INTO services (service_name, description) VALUES (?, ?)', services)
        
        # Insert default admin
        conn.execute('INSERT INTO admins (username, email, password, full_name) VALUES (?, ?, ?, ?)',
                    ('admin', 'admin@nearfix.com', 'admin123', 'System Administrator'))
        
        conn.commit()
        conn.close()
        print("Database initialized successfully!")

# Initialize database
init_database()

# Helper Functions
def login_required(f):
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session and 'helper_id' not in session and 'admin_id' not in session:
            return redirect(url_for('home'))
        return f(*args, **kwargs)
    decorated_function.__name__ = f.__name__
    return decorated_function

def admin_required(f):
    def decorated_function(*args, **kwargs):
        if 'admin_id' not in session:
            flash('Admin access required!', 'error')
            return redirect(url_for('admin_login'))
        return f(*args, **kwargs)
    decorated_function.__name__ = f.__name__
    return decorated_function

def calculate_distance(lat1, lon1, lat2, lon2):
    """Calculate distance between two points in kilometers"""
    R = 6371  # Earth's radius in kilometers
    
    lat1_rad = math.radians(float(lat1))
    lat2_rad = math.radians(float(lat2))
    delta_lat = math.radians(float(lat2) - float(lat1))
    delta_lon = math.radians(float(lon2) - float(lon1))
    
    a = math.sin(delta_lat/2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(delta_lon/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    distance = R * c
    
    return distance

# Routes
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/user/register', methods=['GET', 'POST'])
def user_register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        full_name = request.form['full_name']
        phone = request.form['phone']
        address = request.form['address']
        
        hashed_password = generate_password_hash(password)
        
        conn = get_db_connection()
        try:
            conn.execute('INSERT INTO users (username, email, password, full_name, phone, address) VALUES (?, ?, ?, ?, ?, ?)',
                       (username, email, hashed_password, full_name, phone, address))
            conn.commit()
            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('user_login'))
        except sqlite3.IntegrityError:
            flash('Username or email already exists!', 'error')
            return redirect(url_for('user_register'))
        finally:
            conn.close()
    
    return render_template('user_register.html')

@app.route('/user/login', methods=['GET', 'POST'])
def user_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
        conn.close()
        
        if user and check_password_hash(user['password'], password):
            session['user_id'] = user['user_id']
            session['user_name'] = user['full_name']
            flash('Login successful!', 'success')
            return redirect(url_for('user_dashboard'))
        else:
            flash('Invalid username or password!', 'error')
    
    return render_template('user_login.html')

@app.route('/user/dashboard')
@login_required
def user_dashboard():
    if 'user_id' not in session:
        return redirect(url_for('user_login'))
    
    conn = get_db_connection()
    
    # Get services
    services = conn.execute('SELECT * FROM services').fetchall()
    
    # Get user's requests
    requests = conn.execute('''
        SELECT sr.*, s.service_name, h.full_name as helper_name
        FROM service_requests sr
        LEFT JOIN services s ON sr.service_type_id = s.service_id
        LEFT JOIN helpers h ON sr.helper_id = h.helper_id
        WHERE sr.user_id = ?
        ORDER BY sr.created_at DESC
    ''', (session['user_id'],)).fetchall()
    
    conn.close()
    
    return render_template('user_dashboard.html', services=services, requests=requests)

@app.route('/user/request_service', methods=['POST'])
@login_required
def request_service():
    service_type_id = request.form['service_type_id']
    title = request.form['title']
    description = request.form['description']
    latitude = request.form.get('latitude')
    longitude = request.form.get('longitude')
    address = request.form.get('address')
    
    conn = get_db_connection()
    
    # Find nearest available helper
    helpers = conn.execute('''
        SELECT h.*, s.service_name
        FROM helpers h
        JOIN services s ON h.service_type_id = s.service_id
        WHERE h.service_type_id = ? AND h.is_available = 1 AND h.is_approved = 1
    ''', (service_type_id,)).fetchall()
    
    nearest_helper = None
    min_distance = float('inf')
    
    for helper in helpers:
        if helper['latitude'] and helper['longitude'] and latitude and longitude:
            distance = calculate_distance(latitude, longitude, helper['latitude'], helper['longitude'])
            if distance < min_distance:
                min_distance = distance
                nearest_helper = helper
    
    # Create service request
    status = 'accepted' if nearest_helper else 'pending'
    helper_id = nearest_helper['helper_id'] if nearest_helper else None
    
    conn.execute('''
        INSERT INTO service_requests 
        (user_id, service_type_id, title, description, user_latitude, user_longitude, user_address, helper_id, status)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (session['user_id'], service_type_id, title, description, latitude, longitude, address, helper_id, status))
    
    conn.commit()
    conn.close()
    
    if nearest_helper:
        flash(f'Service request sent to nearest {nearest_helper["service_name"]}!', 'success')
    else:
        flash('Service request submitted. No available helper found nearby.', 'warning')
    
    return redirect(url_for('user_dashboard'))

@app.route('/user/logout')
def user_logout():
    session.pop('user_id', None)
    session.pop('user_name', None)
    flash('Logged out successfully!', 'success')
    return redirect(url_for('home'))

# Helper Routes
@app.route('/helper/register', methods=['GET', 'POST'])
def helper_register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        full_name = request.form['full_name']
        phone = request.form['phone']
        service_type_id = request.form['service_type_id']
        latitude = request.form.get('latitude')
        longitude = request.form.get('longitude')
        
        hashed_password = generate_password_hash(password)
        
        conn = get_db_connection()
        try:
            conn.execute('''
                INSERT INTO helpers 
                (username, email, password, full_name, phone, service_type_id, latitude, longitude)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (username, email, hashed_password, full_name, phone, service_type_id, latitude, longitude))
            conn.commit()
            flash('Registration successful! Please wait for admin approval.', 'success')
            return redirect(url_for('helper_login'))
        except sqlite3.IntegrityError:
            flash('Username or email already exists!', 'error')
            return redirect(url_for('helper_register'))
        finally:
            conn.close()
    
    conn = get_db_connection()
    services = conn.execute('SELECT * FROM services').fetchall()
    conn.close()
    
    return render_template('helper_register.html', services=services)

@app.route('/helper/login', methods=['GET', 'POST'])
def helper_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        conn = get_db_connection()
        helper = conn.execute('SELECT * FROM helpers WHERE username = ?', (username,)).fetchone()
        conn.close()
        
        if helper and check_password_hash(helper['password'], password):
            if not helper['is_approved']:
                flash('Your account is not approved yet!', 'error')
                return redirect(url_for('helper_login'))
            
            session['helper_id'] = helper['helper_id']
            session['helper_name'] = helper['full_name']
            flash('Login successful!', 'success')
            return redirect(url_for('helper_dashboard'))
        else:
            flash('Invalid username or password!', 'error')
    
    return render_template('helper_login.html')

@app.route('/helper/dashboard')
@login_required
def helper_dashboard():
    if 'helper_id' not in session:
        return redirect(url_for('helper_login'))
    
    conn = get_db_connection()
    
    # Get helper info
    helper = conn.execute('SELECT * FROM helpers WHERE helper_id = ?', (session['helper_id'],)).fetchone()
    
    # Get assigned requests
    requests = conn.execute('''
        SELECT sr.*, u.full_name as user_name, u.phone as user_phone, s.service_name
        FROM service_requests sr
        JOIN users u ON sr.user_id = u.user_id
        JOIN services s ON sr.service_type_id = s.service_id
        WHERE sr.helper_id = ?
        ORDER BY sr.created_at DESC
    ''', (session['helper_id'],)).fetchall()
    
    conn.close()
    
    return render_template('helper_dashboard.html', helper=helper, requests=requests)

@app.route('/helper/update_status', methods=['POST'])
@login_required
def update_request_status():
    request_id = request.form['request_id']
    status = request.form['status']
    
    conn = get_db_connection()
    conn.execute('UPDATE service_requests SET status = ? WHERE request_id = ?', (status, request_id))
    conn.commit()
    conn.close()
    
    flash('Request status updated!', 'success')
    return redirect(url_for('helper_dashboard'))

@app.route('/helper/toggle_availability', methods=['POST'])
@login_required
def toggle_availability():
    is_available = request.form['is_available'] == 'True'
    
    conn = get_db_connection()
    conn.execute('UPDATE helpers SET is_available = ? WHERE helper_id = ?', 
                (not is_available, session['helper_id']))
    conn.commit()
    conn.close()
    
    flash('Availability updated!', 'success')
    return redirect(url_for('helper_dashboard'))

@app.route('/helper/logout')
def helper_logout():
    session.pop('helper_id', None)
    session.pop('helper_name', None)
    flash('Logged out successfully!', 'success')
    return redirect(url_for('home'))

# Admin Routes
@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        conn = get_db_connection()
        admin = conn.execute('SELECT * FROM admins WHERE username = ?', (username,)).fetchone()
        conn.close()
        
        if admin and admin['password'] == password:  # In production, use password hashing
            session['admin_id'] = admin['admin_id']
            session['admin_name'] = admin['full_name']
            flash('Login successful!', 'success')
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Invalid username or password!', 'error')
    
    return render_template('admin_login.html')

@app.route('/admin/dashboard')
@admin_required
def admin_dashboard():
    conn = get_db_connection()
    
    # Get statistics
    total_users = conn.execute('SELECT COUNT(*) as count FROM users').fetchone()['count']
    total_helpers = conn.execute('SELECT COUNT(*) as count FROM helpers').fetchone()['count']
    pending_helpers = conn.execute('SELECT COUNT(*) as count FROM helpers WHERE is_approved = 0').fetchone()['count']
    total_requests = conn.execute('SELECT COUNT(*) as count FROM service_requests').fetchone()['count']
    
    # Get pending helpers
    pending_helpers_list = conn.execute('''
        SELECT h.*, s.service_name
        FROM helpers h
        LEFT JOIN services s ON h.service_type_id = s.service_id
        WHERE h.is_approved = 0
    ''').fetchall()
    
    # Get recent requests
    recent_requests = conn.execute('''
        SELECT sr.*, u.full_name as user_name, h.full_name as helper_name, s.service_name
        FROM service_requests sr
        LEFT JOIN users u ON sr.user_id = u.user_id
        LEFT JOIN helpers h ON sr.helper_id = h.helper_id
        LEFT JOIN services s ON sr.service_type_id = s.service_id
        ORDER BY sr.created_at DESC
        LIMIT 10
    ''').fetchall()
    
    conn.close()
    
    return render_template('admin_dashboard.html', 
                         total_users=total_users,
                         total_helpers=total_helpers,
                         pending_helpers=pending_helpers,
                         total_requests=total_requests,
                         pending_helpers_list=pending_helpers_list,
                         recent_requests=recent_requests)

@app.route('/admin/approve_helper/<int:helper_id>')
@admin_required
def approve_helper(helper_id):
    conn = get_db_connection()
    conn.execute('UPDATE helpers SET is_approved = 1 WHERE helper_id = ?', (helper_id,))
    conn.commit()
    conn.close()
    
    flash('Helper approved successfully!', 'success')
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/users')
@admin_required
def admin_users():
    conn = get_db_connection()
    users = conn.execute('SELECT * FROM users ORDER BY created_at DESC').fetchall()
    conn.close()
    
    return render_template('admin_users.html', users=users)

@app.route('/admin/helpers')
@admin_required
def admin_helpers():
    conn = get_db_connection()
    helpers = conn.execute('''
        SELECT h.*, s.service_name
        FROM helpers h
        LEFT JOIN services s ON h.service_type_id = s.service_id
        ORDER BY h.created_at DESC
    ''').fetchall()
    conn.close()
    
    return render_template('admin_helpers.html', helpers=helpers)

@app.route('/admin/services')
@admin_required
def admin_services():
    conn = get_db_connection()
    services = conn.execute('SELECT * FROM services ORDER BY service_name').fetchall()
    conn.close()
    
    return render_template('admin_services.html', services=services)

@app.route('/admin/add_service', methods=['POST'])
@admin_required
def add_service():
    service_name = request.form['service_name']
    description = request.form['description']
    
    conn = get_db_connection()
    conn.execute('INSERT INTO services (service_name, description) VALUES (?, ?)', 
                (service_name, description))
    conn.commit()
    conn.close()
    
    flash('Service added successfully!', 'success')
    return redirect(url_for('admin_services'))

@app.route('/admin/logout')
def admin_logout():
    session.pop('admin_id', None)
    session.pop('admin_name', None)
    flash('Logged out successfully!', 'success')
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
