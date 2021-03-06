import psycopg2
from secrets_client import get_secret
import json

dbName = "users"
port = "5432"
connection = None
menu = """
Image Gallery User Administration v0.1
==============================
[L]ist Users
[A]dd User
[E]dit User
[D]elete User
[Q]uit
    
Enter a choice: """


def get_image_gallery_secret():
    secret = get_secret()
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


def add_user_menu():
    username = input("Enter username: ")
    password = input("Enter password: ")
    fullname = input("Enter full name: ")
    add_user(username, password, fullname)

def edit_user_menu():
    username = input("Enter username: ")
    password = input("Enter password: ")
    fullname = input("Enter full name: ")
    update_user(username, password, fullname)

def delete_user_menu():
    delete_user(input("Enter username: "))
    print('Deleted user')

def list_users_menu():
    result = get_all_users()
    print("\nusername, password, fullname")
    for row in result:
        print(row)



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


def main():
    connect()
    choice = input(menu)
    while choice not in ['q', 'Q']:
        if choice in ['l', 'L']:
            list_users_menu()
        elif choice in ['a', 'A']:
            add_user_menu()
        elif choice in ['e', 'E']:
            edit_user_menu()
        elif choice in ['d', 'D']:
            delete_user_menu()
        else:
            print('Invalid option.')
        choice = input(menu)
    print("Okay, Bye.")

if __name__ == '__main__':
    main()
