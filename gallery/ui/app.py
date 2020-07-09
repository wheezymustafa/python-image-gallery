from . import user_service
from . import image_service
from . import secrets_client
import os
import json
import pathlib
import uuid
from functools import wraps
from flask import Flask
from flask import render_template, redirect, request, session, flash

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp'}
app = Flask(__name__)

os.environ['IG_ROOT_PATH'] = app.root_path

flask_secret_name = "sec-ig-app-secret"
default_image_path = 'static/images'

def get_app_secret():
    if os.environ.get('IG_FLASK_SECRET_FILE') and os.path.exists(os.environ.get('IG_FLASK_SECRET_FILE')):
        f = open(os.environ.get('IG_FLASK_SECRET_FILE'), 'r')
        return f.readline().strip()
    elif os.environ.get('IG_FLASK_SECRET'):
        return os.environ.get('IG_FLASK_SECRET')
    else:
        secret = secrets_client.get_secret(flask_secret_name)
        secret_dict = json.loads(secret)
        return secret_dict['secret']

app.secret_key = get_app_secret()

def requires_admin(func):
    @wraps(func)
    def decorated(**kwargs):
        if session['username'] and user_service.is_admin(session['username']):
            return func(**kwargs)
        else:
            return redirect('/login')
    return decorated

def requires_logged_in(func):
    @wraps(func)
    def decorated(**kwargs):
        if not session or not session['username']:
            return redirect('/login')
        else:
            return func(**kwargs)
    return decorated

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def generate_uuid():
    return str(uuid.uuid1())

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

# Image Gallery User Routes

@app.route('/')
def index():
    if not session or not session['username']:
        return redirect('/login')
    return render_template('index.html', session=session)

@app.route('/view')
@requires_logged_in
def view():
    images = user_service.get_images_by_user(session['username'])
    for imageid in images:
        image_service.get_image(imageid)
    return render_template('view.html', image_path=default_image_path, images=images, username=session['username']);

@app.route('/view/<imageid>')
@requires_logged_in
def view_image(imageid):
    return render_template('view-image.html', image_path='../{}'.format(default_image_path), imageid=imageid);

@app.route('/delete/<imageid>')
@requires_logged_in
def delete_image(imageid):
    image_service.delete_image(imageid)
    user_service.delete_image(session['username'], imageid)
    return redirect('/view')

@app.route('/upload', methods=['GET', 'POST'])
@requires_logged_in
def upload():
    error = None
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file found')
        file = request.files['file']
        if file and allowed_file(file.filename):
            uuid = generate_uuid()
            image_service.upload_image(uuid, file)
            user_service.put_user_image(session['username'], uuid)
        return redirect('/view')
    else:
        return render_template('upload.html', error=error)


# Admin Routes

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
    images = user_service.get_images_by_user('dam0045')
    print(images)
    return render_template('test.html', image_path=default_image_path, images=images);
