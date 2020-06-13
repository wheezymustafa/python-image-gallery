import admin_service
from flask import Flask
from flask import render_template, redirect, request
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/admin')
def admin_page():
    users = admin_service.get_users()
    return render_template('admin.html', users=users)

@app.route('/admin/editUser/<username>', methods=['GET'])
def edit_user_form(username):
    return render_template('editUser.html', username=username)

@app.route('/admin/editUser', methods=['POST'])
def edit_user():
    print(request)
    username = request.form['username']
    password = request.form['password']
    fullname = request.form['fullname']
    admin_service.update_user(username, password, fullname)
    return redirect('/admin')


