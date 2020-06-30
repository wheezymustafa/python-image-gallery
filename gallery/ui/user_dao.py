import psycopg2
from .secrets_client import get_secret
import json

dbName = "users"
port = "5432"
connection = None
image_gallery_secret_name = "sec-imagegallery-pw"

def get_image_gallery_secret():
    secret = get_secret(image_gallery_secret_name)
    secret_dict = json.loads(secret)
    return secret_dict

def get_password():
    print('Retrieving password..')
    secret_dict = get_image_gallery_secret()
    print('Retrieved password..')
    return secret_dict['password']

def get_host():
    print('Retrieving host..')
    secret_dict = get_image_gallery_secret()
    print('Retrieved host..')
    return secret_dict['host']

def get_user():
    print('Retrieving user..')
    secret_dict = get_image_gallery_secret()
    print('Retrieved user..')
    return secret_dict['username']

def connect():
    host = get_host()
    print('Connecting to {host}..'.format(host=host))
    user = get_user()
    password = get_password()
    global connection
    connection = psycopg2.connect(database=dbName,
                                  user=user,
                                  password=password,
                                  host=host,
                                  port=port)
    connection.set_session(autocommit=True)
    print('Connected to {host}'.format(host=host))


def get_cursor():
    if not connection:
        connect()
    return connection.cursor()


def execute(query, args=None):
    cur = get_cursor()
    if not args:
        cur.execute(query)
    else:
        cur.execute(query, args)
    return cur


def add_user(username, password, fullname):
    cur = get_cursor()
    query = "insert into users (username, password, fullname) values (%s, %s, %s);"
    execute(query, (username, password, fullname))

    
def update_user(username, password, fullname):
    query = "update users set password = %s, fullname = %s where username = %s;"
    execute(query, (password, fullname, username))

    
def delete_user(username):
    query = "delete from users where username = %s;"
    execute(query, (username,))


def get_user_by_username(username):
    query = "select * from users where username = %s;"
    return execute(query, (username,))
    
def get_all_users():
    query = "select * from users;"
    return execute(query)

def upload_image(username, imageid):
    query = "insert into userimages(username, imageid) values (%s, %s);"
    execute(query, (username, imageid))

def get_images_by_user(username):
    query = "select imageid from userimages where username = %s;"
    execute(query, (username,))
