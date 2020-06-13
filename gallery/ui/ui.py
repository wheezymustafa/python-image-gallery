from flask import Flask
from .admin_service import *
from flask import render_template
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/admin')
def admin_page():
    return render_template('admin.html')