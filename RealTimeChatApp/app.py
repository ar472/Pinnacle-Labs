from flask import Flask, render_template, request, redirect, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO, emit
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

app.config['SECRET_KEY'] = 'secret123'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

db = SQLAlchemy(app)
socketio = SocketIO(app, async_mode='threading')

# User Table
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(200))

# Message Table
class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100))
    message = db.Column(db.Text)

# Home
@app.route('/')
def home():
    return redirect('/login')

# Register
@app.route('/register', methods=['GET', 'POST'])
def register():

    if request.method == 'POST':

        username = request.form['username']
        password = generate_password_hash(request.form['password'])

        existing_user = User.query.filter_by(username=username).first()

        if existing_user:
            flash("Username already exists")
            return redirect('/register')

        user = User(
            username=username,
            password=password
        )

        db.session.add(user)
        db.session.commit()

        flash("Registration Successful!")
        return redirect('/login')

    return render_template('register.html')

# Login
@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':

        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):

            session['username'] = username
            return redirect('/chat')

        flash("Invalid Credentials")

    return render_template('login.html')

# Chat
@app.route('/chat')
def chat():

    if 'username' not in session:
        return redirect('/login')

    messages = Message.query.all()

    return render_template(
        'chat.html',
        username=session['username'],
        messages=messages
    )

# Logout
@app.route('/logout')
def logout():

    session.clear()
    return redirect('/login')

# Socket Message Event
@socketio.on('send_message')
def handle_message(data):

    msg = Message(
        username=data['username'],
        message=data['message']
    )

    db.session.add(msg)
    db.session.commit()

    emit(
        'receive_message',
        data,
        broadcast=True
    )

# Run App
if __name__ == '__main__':

    with app.app_context():
        db.create_all()

    socketio.run(
        app,
        debug=True,
        allow_unsafe_werkzeug=True
    )