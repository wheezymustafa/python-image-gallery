import psycopg2
from .secrets_client import get_secret
import json

dbName = "users"
dbUser = "image_gallery"
host = "image-gallery-priv.ctvpfstspksz.us-east-2.rds.amazonaws.com"
port = "5432"
connection = None


def get_image_gallery_secret():
    return get_secret()


def get_password():
    print('Retrieving secret..')
    secret = get_image_gallery_secret()
    secret_dict = json.loads(secret)
    print('Retrieved secret..')
    return secret_dict['password']


def connect():
    print('Connecting to {host}..'.format(host=host))
    password = get_password()
    global connection
    connection = psycopg2.connect(database=dbName,
                                  user=dbUser,
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

    
def get_all_users():
    query = "select * from users;"
    return execute(query)
