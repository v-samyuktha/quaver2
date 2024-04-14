# below lib is flask_security_too
from flask_security import Security, SQLAlchemyUserDatastore, login_user, roles_accepted, current_user, logout_user, auth_token_required
from application.models import *
import bcrypt
# from flask import current_app as app

user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security=Security()