from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///visitors.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'your_secret_key_here'  # needed for session

db = SQLAlchemy(app)

# Visitor Table
class Visitor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    company_name = db.Column(db.String(100), nullable=False, default="OTS Mindspace")
    email = db.Column(db.String(100), nullable=False)
    contact_number = db.Column(db.String(20), nullable=False)
    purpose = db.Column(db.String(100), nullable=False)
    person_to_meet = db.Column(db.String(100), nullable=False)
    check_in_time = db.Column(db.String(50), nullable=False)
    check_out_time = db.Column(db.String(50), nullable=True)

# Create tables if they don't exist
with app.app_context():
    db.create_all()

# ----------------------
# Visitor Registration
# ----------------------
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        visitor = Visitor(
            name=request.form['name'],
            company_name="OTS Mindspace",
            email=request.form['email'],
            contact_number=request.form['contact_number'],
            purpose=request.form['purpose'],
            person_to_meet=request.form['person_to_meet'],
            check_in_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )
        db.session.add(visitor)
        db.session.commit()
        return "Registration Successful! ✅"

    return render_template('register.html')

# ----------------------
# Admin Login
# ----------------------
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Hardcoded credentials
        if username == 'OTS' and password == 'admin123':
            session['admin_logged_in'] = True
            return redirect(url_for('admin'))
        else:
            return "Invalid Credentials! ❌"
    
    return render_template('login.html')

# ----------------------
# Admin Dashboard
# ----------------------
@app.route('/admin')
def admin():
    if not session.get('admin_logged_in'):
        return redirect(url_for('login'))

    visitors = Visitor.query.order_by(Visitor.check_in_time.desc()).all()
    return render_template('admin.html', visitors=visitors)

# ----------------------
# Admin Logout
# ----------------------
@app.route('/logout')
def logout():
    session.pop('admin_logged_in', None)
    return redirect(url_for('login'))

import os

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))


