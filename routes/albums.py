from flask import jsonify, request, make_response
from application.models import *
from application.security_framework import user_datastore, bcrypt, current_user, login_user, logout_user, roles_accepted
from flask_restful import Resource
from datetime import date
import requests

class AlbumsAPI(Resource):
    def get(self):
        if request.args.get("by"):
            albums=[]
            artist_id = request.args.get("by")
            print(artist_id)
            albums = Album.query.filter_by(artist_id = artist_id).all()
            return make_response(jsonify([album.search() for album in albums]), 200)
        elif request.args.get("key"):
            albums=[]
            key=request.args.get("key")
            results = Album.query.all()
            for album in results:
                if key.lower() in album.title.lower() and album.flag=="false":
                    albums.append(album)
            return make_response(jsonify([album.search() for album in albums]), 200)
        elif request.args.get("flag"):
            albums=[]
            results = Album.query.all()
            for album in results:
                if album.flag=="true":
                    albums.append(album)
            return make_response(jsonify([album.search() for album in albums]), 200)
        else:
            albums=[]
            results = Album.query.order_by(Album.rating.desc()).all()
            for album in results:
                if album.flag=="false":
                    albums.append(album)
            return make_response(jsonify([album.search() for album in albums]), 200)
    
    def post(self):
        print(request.get_json()['params'])
        data = request.get_json()['params']
        title = data["title"]
        if "description" in data.keys():
            description = data["description"]
        else:
            description=None
        created_at = date.today()
        genre = data["genre"]

        song_ids = data["song_ids"]
        artist_id = data["artistId"]

        album = Album(title=title, description=description, created_at=created_at, genre=genre, artist_id=artist_id)
        db.session.add(album)
        db.session.commit()
        print("Added Album")

        for id in song_ids:
            album_song = AlbumSong(album_id=album.album_id, song_id=id)
            db.session.add(album_song)
        db.session.commit()
        print("Updated AlbumSongs")
        return make_response(jsonify({"message": "Album has been added successfully!"}), 200)

class AlbumAPI(Resource):
    def get(self, album_id):
        album = Album.query.filter_by(album_id=album_id).first()
        if not album:
            return make_response(jsonify({"message":"Album not found."}), 400)
        return make_response(jsonify(album.search()), 200)
    
    def put(self, album_id):
        data = request.get_json()['params']
        if "rating" in data.keys():
            album = Album.query.filter_by(album_id=album_id).first()
            if album.rating is None:
                album.rating = data["rating"]
                album.no_users_rated = 1
            else:
                album.rating= (album.no_users_rated*album.rating + int(data["rating"]))*1.0/(album.no_users_rated+1)
                album.rating = round(album.rating, 2)
                album.no_users_rated += 1
            print("Updated rating")
        elif "flag" in data.keys():
            album = Album.query.filter_by(album_id=album_id).first()
            if data["flag"]=="true":
                album.flag="true"
            elif data["flag"]=="false":
                album.flag="false"
            else:
                return make_response(jsonify({"message":"Invalid request params"}))
            db.session.commit()
            print(f"Updated flag for album {album_id}")
        else:
            data = request.get_json()
            album = Album.query.filter_by(album_id=album_id).first()
            if not album:
                return make_response(jsonify({"message":"Album not found."}), 400)
            new_title = data.get("title")
            new_genre = data.get("genre")
            if new_title is not None:
                album.title=new_title
            if new_genre is not None:
                album.genre=new_genre
        db.session.commit()
        print(f'Updated album {album_id}')
        return make_response(jsonify({"message":"Album updated successfully!"}), 200)
    
    def delete(self, album_id):
        album = Album.query.filter_by(album_id=album_id).first()
        if not album:
            return make_response(jsonify({"message":"Album not found."}), 400)
        
        db.session.delete(album)
        db.session.commit()
        print("Deleted album", album_id)

        return make_response(jsonify({"message":"Album deleted successfully."}), 200)
