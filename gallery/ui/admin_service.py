from . import user_admin

user_admin.connect()

def get_users():
    users = []
    res = user_admin.get_all_users()
    for user in res:
        users.append({'username': user[0], 'fullname': user[2]})
    return users

def add_user(username, password, fullname):
    user_admin.add_user(username, password, fullname)

def update_user(username, password, fullname):
    user_admin.update_user(username, password, fullname)

def delete_user(username):
    user_admin.delete_user(username)
   
