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
    username = request.form['username']
    password = request.form['password']
    fullname = request.form['fullname']
    admin_service.update_user(username, password, fullname)
    return redirect('/admin')

@app.route('/admin/addUser', methods=['GET','POST'])
def add_user():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        fullname = request.form['fullname']
        admin_service.add_user(username, password, fullname)
        return redirect('/admin')
    else:
        return render_template('addUser.html')
    
@app.route('/admin/deleteUser/<username>', methods=['GET','POST'])
def delete_user(username):
    if request.method == 'POST':
        admin_service.delete_user(username)
        return redirect('/admin')
    else:
        return render_template('deleteUser.html', username=username)
