from . import user_dao

user_dao.connect()

def get_users():
    users = []
    res = user_dao.get_all_users()
    for user in res:
        users.append({'username': user[0], 'fullname': user[2]})
    return users

def add_user(username, password, fullname):
    user_dao.add_user(username, password, fullname)

def update_user(username, password, fullname):
    user_dao.update_user(username, password, fullname)

def delete_user(username):
    user_dao.delete_user(username)
   
