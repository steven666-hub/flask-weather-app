import os
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user
import requests

app = Flask(__name__)
app.secret_key = os.urandom(24)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

users = {'stevenwu1999@gmail.com': {'password': '1234'}}

# class User(UserMixin):
#     pass

# @login_manager.user_loader
# def user_loader(email):
#     if email not in users:
#         return

#     user = User()
#     user.id = email
#     return user




class User(UserMixin):
    def __init__(self, email):
        self.id = email

@login_manager.user_loader
def user_loader(email):
    if email not in users:
        return None
    user = User(email)
    return user


@app.route('/')
def index():
    return '歡迎來到天氣應用！請<a href="/login">登錄</a>以繼續。'

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        if email in users and users[email]['password'] == password:
            user = User(email)
            user.id = email
            login_user(user)
            return redirect(url_for('weather'))

        flash('Invalid username or password')

    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/weather')
@login_required
def weather():
    api_key = "79235961126ed3f37b5469868f5e5619"
    city = "Taipei"
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"

    response = requests.get(url)
    weather_data = response.json()
    return render_template('weather.html', weather=weather_data)

if __name__ == '__main__':
    app.run(debug=True)

