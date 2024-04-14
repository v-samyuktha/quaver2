from flask import jsonify, request, make_response
from application.models import *
from application.security_framework import user_datastore, bcrypt, current_user, login_user, logout_user, roles_accepted
from flask_restful import Resource
from datetime import date

class UserAPI(Resource):
    def get(self, user_id):
        user = User.query.filter_by(id=user_id).first()
        if user:
            return make_response(jsonify(user.search()))
        else:
            return make_response(jsonify({"message":"Invalid userId"}))

class UsersAPI(Resource):
    def get(self):
        if request.args.get("role"):
            role = request.args.get("role")
            all_users = User.query.all()
            users=[]
            for user in all_users:
                if role in user.roles:
                    users.append(user.search())
            return make_response(jsonify(users))
        else:
            users = User.query.all()
            return make_response(jsonify([user.search() for user in users]))