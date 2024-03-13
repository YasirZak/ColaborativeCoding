from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Mock user database (replace this with a real user database)
users = {}

@app.route('/')
def index():
    if 'username' in session:
        return f'Logged in as {session["username"]}. <a href="/logout">Logout</a>'
    return 'You are not logged in. <a href="/login">Login</a> or <a href="/signup">Sign Up</a>'

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users:
            return 'Username already exists. <a href="/signup">Try again</a>'
        users[username] = password
        session['username'] = username
        return redirect(url_for('index'))
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username not in users or users[username] != password:
            return 'Invalid username/password. <a href="/login">Try again</a>'
        session['username'] = username
        return redirect(url_for('index'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
