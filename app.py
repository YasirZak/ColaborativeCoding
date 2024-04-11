from flask import Flask, render_template, request, redirect, url_for, session, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError
from flask_bcrypt import Bcrypt
from flask_socketio import SocketIO, emit
from subprocess import Popen, PIPE
#use "pip install -r requirements.txt" to install all modules

document = {'text': ''}

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'this'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
socketio = SocketIO(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String(20),nullable = False, unique = True)
    password = db.Column(db.String(20),nullable = False)

class SignupForm(FlaskForm):
    username = StringField(validators=[
        InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})

    password = PasswordField(validators=[
        InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": "Password"})

    submit = SubmitField('signup')

    def validate_username(self, username):
        existing_user_username = User.query.filter_by(
            username=username.data).first()
        if existing_user_username:
            raise ValidationError(
                'That username already exists. Please choose a different one.')    
        
class LoginForm(FlaskForm):
    username = StringField(validators=[
        InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})

    password = PasswordField(validators=[
        InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": "Password"})

    submit = SubmitField('Login')


# Create the application context
with app.app_context():
    # Create all database tables
    db.create_all()




@app.route('/')
def index():
    
    return render_template("home.html")

@app.route('/index')
def Index():
    return render_template('index.html')
    
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        new_user = User(username=form.username.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))

    return render_template('signup.html', form = form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username = form.username.data).first()
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect(url_for('dashboard'))
    return render_template('login.html', form = form)

@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    return render_template('dashboard.html')

@app.route('/logout', methods=['GET', 'POST'] )
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@socketio.on('connect')
def handle_connect():
    print('Client connected')
    emit('document_update', document) 

@socketio.on('text_change')
def handle_text_change(data):
    global document
    document['text'] = data['text']
    emit('document_update', document, broadcast=True)

@app.route('/compile', methods=['POST'])
def compile():
    code = request.form['code']
    try:
        process = Popen(['python', '-c', code], stdout=PIPE, stderr=PIPE)
        output, error = process.communicate(timeout=10)  # Timeout to prevent long-running processes
        if error:
            return error.decode('utf-8')
        else:
            return output.decode('utf-8')
    except Exception as e:
        return str(e)    
    return "Code compiled successfully!"


if __name__ == '__main__':
    app.run(host = '0.0.0.0',debug=True)
    socketio.run(app)
