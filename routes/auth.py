from flask import jsonify, request, make_response
from application.models import *
from application.security_framework import user_datastore, bcrypt, current_user, login_user, logout_user, roles_accepted
from flask_restful import Resource
import datetime

class RegisterAPI(Resource):
    def post(self):
        data = request.get_json()
        username = data["username"]
        password = data["password"]
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        try:
            new_user = user_datastore.create_user(username=username, password=hashed_password, joined_on=datetime.date.today())
            user_datastore.add_role_to_user(new_user, 'user')
            db.session.commit()
            print("Added new user")
            user_id = User.query.filter_by(username=username).first().id
            activity = UserActivity(user_id = user_id, activity_type="registered")
            db.session.add(activity)
            print("Updated activity 'registered'")
            db.session.commit()
            return make_response(jsonify({"message":"Registration successful!"}), 200)
        except:
            #if username already exists
            return make_response(jsonify({"message":'Username has already been taken.'}), 400)
        
class LoginAPI(Resource):
    def post(self):
        data = request.get_json()
        username = data["username"]
        password = data["password"]
        print(data)
        user = user_datastore.find_user(username=username)
        if user:
            if bcrypt.checkpw(password.encode('utf-8'), user.password):
                login_user(user) #session based login
                activity = UserActivity(user_id = user.id, activity_type="login")
                db.session.add(activity)
                user.last_login_at=datetime.datetime.now()
                db.session.commit()
                print("Updated activity 'login'")
                auth_token = user.get_auth_token() #token based login
                return make_response(jsonify({
                    "message": "Login Successful!", 
                    "auth_token" :auth_token, 
                    "id": current_user.id, 
                    "username": current_user.username, 
                    'roles': [role.name for role in current_user.roles]}), 200)
            else:
                return make_response(jsonify({"message": "Invalid username or password."}), 400)
        else:
            return make_response(jsonify({"message": "Invalid username or password."}), 400)

class LogoutAPI(Resource):
    def post(self):
        print("Logout requested")
        logout_user()
        return make_response(jsonify({"message": "Logged out."}), 200)