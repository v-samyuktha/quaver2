from flask import jsonify, request, make_response
from application.models import *
from application.security_framework import user_datastore, bcrypt, current_user, login_user, logout_user, roles_accepted
from flask_restful import Resource
from datetime import date

class PlaylistsAPI(Resource):
    def get(self):
        if request.args.get("key"):
            if request.args.get("userId"):
                userId = request.args.get("userId")
                playlists=[]
                key=request.args.get("key")
                results = Playlist.query.filter_by(created_by=userId)
                for playlist in results:
                    if key.lower() in playlist.title.lower():
                        playlists.append(playlist)
                return make_response(jsonify([playlist.search() for playlist in playlists]), 200)
        elif "userId" in request.args:
            userId = request.args.get("userId")
            print(f"Playlists requested for {userId}")
            playlists = Playlist.query.filter_by(created_by=userId).all()
        else:
            playlists = Playlist.query.all()
        print(playlists)
        playlists.reverse()
        return make_response(jsonify([playlist.search() for playlist in playlists]), 200)
    
    def post(self):
        data = request.get_json()
        print(data)
        created_by=data["userId"]
        title=data["title"]
        created_at=date.today()
        description=data["desc"]
        new_playlist = Playlist(created_at=created_at, created_by=created_by, title=title, description=description)
        db.session.add(new_playlist)
        db.session.commit()
        print("Made a playlist")

        print("Adding Songs...")
        song_ids=data["song_ids"]
        for id in song_ids:
            new_playlist_song = PlaylistSong(playlist_id=new_playlist.playlist_id, song_id=id)
            db.session.add(new_playlist_song)
            db.session.commit()
        return make_response(jsonify({"message":"Successfully created playlist"}), 200)
    
class PlaylistAPI(Resource):
    def get(self, playlist_id):
        playlist = Playlist.query.filter_by(playlist_id=playlist_id).first()
        if not playlist:
            return make_response(jsonify({"message":"Playlist not found."}), 400)
        return make_response(jsonify(playlist.search()), 200)
    
    def delete(self, playlist_id):
        playlist = Playlist.query.filter_by(playlist_id=playlist_id).first()
        if not playlist:
            return make_response(jsonify({"message":"Playlist not found."}), 400)

        db.session.delete(playlist)
        db.session.commit()
        print(f"Deleted playlist {playlist_id}")

        return make_response(jsonify({"message":"Playlist deleted successfully."}), 200)
    
    def put(self,playlist_id):
        playlist = Playlist.query.filter_by(playlist_id=playlist_id).first()
        if not playlist:
            return make_response(jsonify({"message":"Playlist not found."}), 400)
        
        if request.args.get("add_song"):
            song_id = request.args.get("add_song")
            new_playlist_song = PlaylistSong(playlist_id=playlist_id, song_id=song_id)
            db.session.add(new_playlist_song)
            db.session.commit()
            print(f"Added song {song_id} to playlist {playlist_id}")
            return make_response(jsonify({"message":f"Added song {song_id} to playlist {playlist_id}"}), 200)

        elif request.args.get("remove_song"):
            song_id = request.args.get("remove_song")
            playlist_song = PlaylistSong.query.filter_by(playlist_id=playlist_id, song_id=song_id).first()
            db.session.delete(playlist_song)
            db.session.commit()
            print(f"Removed song {song_id} from playlist {playlist_id}")
            return make_response(jsonify({"message":f"Removed song {song_id} from playlist {playlist_id}"}), 200)

        else:
            return make_response(jsonify({"message":"Invalid query string."}), 400)