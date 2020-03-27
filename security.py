from werkzeug.security import safe_str_cmp         # safer way to compare strings
from models.user import UserModel

# this change vs section4 allows us to store on sqlite database vs in memory database
# our program now allows us to retrieve users from that sqlite database

def authenticate(username, password):
    user = UserModel.find_by_username(username)
    if user and safe_str_cmp(user.password, password):
        return user

def identity(payload):  # payload is the content of the JWT token
    user_id = payload['identity']  # payload = {'exp': 1585089792, 'iat': 1585089492, 'nbf': 1585089492, 'identity': 1}
    return UserModel.find_by_id(user_id)
