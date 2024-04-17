from flask import jsonify, request, make_response
from application.models import *
from application.security_framework import user_datastore, bcrypt, current_user, login_user, logout_user, roles_accepted, auth_token_required
from flask_restful import Resource
from datetime import date

class ArtistsAPI(Resource):
    @roles_accepted('user', 'creator', 'admin')
    def get(self):
        if request.args.get("artistId"):
            artist = Artist.query.filter_by(artist_id=request.args.get("artistId")).first()
            return make_response(jsonify(artist.search()), 200)
        elif request.args.get("username"):
            artist = Artist.query.filter_by(username=request.args.get("username")).first()
            return make_response(jsonify(artist.search()), 200)

        artists = Artist.query.all()
        return make_response(jsonify([artist.search() for artist in artists]), 200)
    
    @roles_accepted('user')
    @auth_token_required
    def post(self):
        data = request.get_json()
        name = data["name"]
        username = data["username"]
        user_id = data["id"]
        artist = Artist(name=name, username=username)
        db.session.add(artist)
        db.session.commit()
        print("Added Artist")

        user = User.query.filter_by(id=user_id).first()
        role = Role.query.filter_by(name="creator").first()
        print(role)
        result=user_datastore.add_role_to_user(user, role)
        print(result)
        db.session.commit()

        return make_response(jsonify({"message": "Registered as Creator Successfully!"}), 200)