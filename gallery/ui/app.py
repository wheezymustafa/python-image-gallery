from . import user_service
from . import image_service
from . import secrets_client
import json
from functools import wraps
from flask import Flask
from flask import render_template, redirect, request, session, flash
app = Flask(__name__)

flask_secret_name = "sec-ig-app-secret"

def get_app_secret():
    secret = secrets_client.get_secret(flask_secret_name)
    secret_dict = json.loads(secret)
    return secret_dict['secret']

app.secret_key = get_app_secret()

def requires_admin(func):
    @wraps(func)
    def decorated(**kwargs):
        print(session)
        if session['username'] and user_service.is_admin(session['username']):
            return func(**kwargs)
        else:
            return redirect('/login')
    return decorated

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_service.is_valid_user(username, password):
            session['username'] = username
            session['is_admin'] = True if user_service.is_admin(username) else False
            return redirect('/')
        else:
            error = 'Login failed'
            return render_template('login.html', error=error)
    else:
        return render_template('login.html', error=error)

@app.route('/')
def index():
    if not session['username']:
        return redirect('/login')
    return render_template('index.html', session=session)

@app.route('/admin')
@requires_admin
def admin_page():
    users = user_service.get_users()
    return render_template('admin.html', users=users)

@app.route('/admin/editUser/<username>', methods=['GET'])
@requires_admin
def edit_user_form(username):
    return render_template('editUser.html', username=username)

@app.route('/admin/editUser', methods=['POST'])
@requires_admin
def edit_user():
    username = request.form['username']
    password = request.form['password']
    fullname = request.form['fullname']
    user_service.update_user(username, password, fullname)
    return redirect('/admin')

@app.route('/admin/addUser', methods=['GET','POST'])
@requires_admin
def add_user():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        fullname = request.form['fullname']
        user_service.add_user(username, password, fullname)
        return redirect('/admin')
    else:
        return render_template('addUser.html')
    
@app.route('/admin/deleteUser/<username>', methods=['GET','POST'])
@requires_admin
def delete_user(username):
    if request.method == 'POST':
        user_service.delete_user(username)
        return redirect('/admin')
    else:
        return render_template('deleteUser.html', username=username)

@app.route('/testobject')
def testobject():
    image = image_service.get_image('asg config.png')
    return render_template('test.html', image=image);
