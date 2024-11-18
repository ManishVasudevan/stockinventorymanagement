from flask import Flask, render_template, redirect, url_for, session, request
from functools import wraps

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

# Authentication decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('logged_in'):
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# Login Route
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['admin']
        password = request.form['password123']
        # Add your authentication logic here
        if username == 'admin' and password == 'password':
            session['logged_in'] = True
            return redirect(url_for('home'))
    return render_template('login.html')

# Home Route
@app.route('/home')
@login_required
def home():
    return render_template('home.html')

# Route Handlers
@app.route('/transactions')
@login_required
def transactions():
    return render_template('transactions.html')

@app.route('/stock-entry')
@login_required
def stock_entry():
    return render_template('stockentry.html')

@app.route('/stock-check')
@login_required
def stock_check():
    return render_template('stockcheck.html')

@app.route('/history')
@login_required
def history():
    return render_template('Report.html')

# Logout Route
@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)