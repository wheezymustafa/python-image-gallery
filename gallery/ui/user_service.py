from . import user_dao

user_dao.connect()

def is_valid_user(username, password):
    user = get_user_by_username(username)
    if not user or password != user['password']:
        return False
    else:
        return True

def is_admin(username):
    return True if username == 'dam0045' else False

def get_user_by_username(username):
    res = user_dao.get_user_by_username(username)
    user = res.fetchone()
    if not user:
        return None
    else:
        userObj = {'username': user[0], 'password': user[1], 'fullname': user[2]}
        return userObj


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
   
def get_images_by_user(username):
    imageids = []
    res = user_dao.get_images_by_user(username)
    for imageid in res:
        imageids.append(imageid[0])
    return imageids

def put_user_image(username, imageid):
    print('Inserting record: {}, {}'.format(username, imageid))
    user_dao.put_user_image(username, imageid)

def delete_image(username, imageid):
    user_dao.delete_image(username, imageid)
