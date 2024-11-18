from flask import Flask, request, render_template, redirect, session
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

# Simulated user database
users = {
    'admin': {
        'username': 'admin',
        'password': generate_password_hash('password123')
    }
}

@app.route('/', methods=['GET'])
def login_page():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    if username in users:
        if check_password_hash(users[username]['password'], password):
            session['logged_in'] = True
            return redirect('/home')  # Redirect to home page
    
    # Login failed
    return render_template('login.html', error='Invalid credentials')

@app.route('/home')
def home():
    if not session.get('logged_in'):
        return redirect('/')
    return render_template('homepage.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)