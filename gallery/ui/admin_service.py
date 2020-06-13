from ..tools import user_admin

def get_secret():
  sec = user_admin.get_secret()
  print(sec)