from flask import Flask, url_for, redirect, request,  render_template
from flask_socketio import SocketIO
from db import Chatdbs
from flask_login import LoginManager, login_user
from flask_login import LoginManager, login_user, logout_user, login_required, current_user, UserMixin
from sqlalchemy.exc import IntegrityError
import json

app = Flask(__name__)
app.secret_key = "my secret key"
#socketio = SocketIO(app)
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)



session = 'session'
count = 1
num_session = {}

try:
    with open('pl.json', 'r') as file:
        num_session = json.load(file)
except Exception:
    num_session = {}


@login_manager.user_loader
def load_user(username):
    return Chatdbs.get_user(username)

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    '''login route'''
    global count
    global session
    global num_session


    # if current_user.is_authenticated:
    #     return redirect(url_for('main'))
    message = ''
    
    if request.method == 'POST':
        username = request.form.get('username')
        password_input = request.form.get('password')


        user = Chatdbs.get_user(username)
        if user and user.check_password(password_input):
            # login_user(user)
            sh = f'session{count}'
            try:
                num_session[sh]
                if len(num_session[sh]) >= 2:
                    count += 1
            except Exception:
                pass
            
            session_id = session + str(count)
            
            num_session.setdefault(session_id, []).append(session_id)

            with open('pl.json', 'w') as file:
                json.dump(num_session, file, indent=4)
                    
            # print(session_id)
            # print(num_session)
            return render_template('main.html', username=username, session_id=session_id)
        else:
            message = "failed to login"
    return render_template('login.html', message=message)

@app.route('/main')
def main():
    return render_template('main.html')

@app.route('/signup')
def signup():
    '''signup route'''
    if current_user.is_authenticated:
        return redirect(url_for('main'))

    message = ''
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password_input = request.form.get('password')
        try:
            Chatdbs.new(username, email, password_input)
            return redirect(url_for('login'))
        except IntegrityError:
            message = 'user already exists'

    return render_template('signup.html', message=message)

if __name__ == '__main__':
    app.run(port=5001, debug=1)