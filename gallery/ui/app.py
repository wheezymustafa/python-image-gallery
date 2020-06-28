from . import user_service
from . import secrets_client
import json
from flask import Flask
from flask import render_template, redirect, request, session
app = Flask(__name__)

flask_secret_name = "sec-ig-app-secret"

def get_app_secret():
    secret = secrets_client.get_secret(flask_secret_name)
    secret_dict = json.loads(secret)
    return secret_dict['secret']

app.secret_key = get_app_secret()

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_service.is_valid_user(username, password):
            session['username'] = username
        return render_template('index.html')
    else:
        return render_template('login.html')

@app.route('/index.html')
def index():
    return session['username']

@app.route('/admin')
def admin_page():
    users = user_service.get_users()
    return render_template('admin.html', users=users)

@app.route('/admin/editUser/<username>', methods=['GET'])
def edit_user_form(username):
    return render_template('editUser.html', username=username)

@app.route('/admin/editUser', methods=['POST'])
def edit_user():
    username = request.form['username']
    password = request.form['password']
    fullname = request.form['fullname']
    user_service.update_user(username, password, fullname)
    return redirect('/admin')

@app.route('/admin/addUser', methods=['GET','POST'])
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
def delete_user(username):
    if request.method == 'POST':
        user_service.delete_user(username)
        return redirect('/admin')
    else:
        return render_template('deleteUser.html', username=username)
