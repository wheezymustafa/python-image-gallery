import boto3
import psycopg2

dbName = "useradmin"
dbUser = "useradmin"
dbPassword = "Xb0x3601"
host = "192.168.1.69"
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

def connect():
    global connection
    connection = psycopg2.connect(database=dbName,
                                  user=dbUser,
                                  password=dbPassword,
                                  host=host,
                                  port=port)
    connection.set_session(autocommit=True)


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


def add_user(username, password, fullname):
    cur = get_cursor()
    query = "insert into users (username, password, fullname) values (%s, %s, %s);"
    # cur.execute(query, (username, password, fullname))
    execute(query, (username, password, fullname))


def edit_user_menu():
    username = input("Enter username: ")
    password = input("Enter password: ")
    fullname = input("Enter full name: ")
    update_user(username, password, fullname)


def update_user(username, password, fullname):
    query = "update users set password = %s, fullname = %s where username = %s;"
    execute(query, (password, fullname, username))


def delete_user_menu():
    delete_user(input("Enter username: "))
    print('Deleted user')


def delete_user(username):
    query = "delete from users where username = %s;"
    execute(query, (username,))


def get_all_users():
    query = "select * from users;"
    result = execute(query)
    print("username, password, fullname")
    for row in result:
        print(row)


if __name__ == '__main__':
    connect()
    choice = input(menu)
    while choice != 'Q' and choice != 'q':
        if choice in ['l', 'L']:
            get_all_users()
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
