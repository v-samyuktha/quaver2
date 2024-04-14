from flask import jsonify, request, make_response
from application.models import *
from application.security_framework import user_datastore, bcrypt, current_user, login_user, logout_user, roles_accepted
from flask_restful import Resource
from datetime import date
import os

class SongsAPI(Resource):
    def get(self):
        if request.args.get("by"):
            songs=[]
            artist_id = request.args.get("by")
            print(artist_id)
            artist = Artist.query.filter_by(artist_id = artist_id).first()
            return make_response(jsonify([song.search() for song in artist.songs]), 200)
        
        elif request.args.get("key"):
            songs=[]
            key=request.args.get("key")
            results = Song.query.all()
            for song in results:
                if key.lower() in song.title.lower() and song.flag=="false":
                    songs.append(song)
            return make_response(jsonify([song.search() for song in songs]), 200)
        elif request.args.get("flag"):
            songs=[]
            results = Song.query.all()
            for song in results:
                if song.flag=="true":
                    songs.append(song)
            return make_response(jsonify([song.search() for song in songs]), 200)
        else:
            songs=[]
            results = Song.query.order_by(Song.rating.desc()).all()
            for song in results:
                if song.flag=="false":
                    songs.append(song)
            return make_response(jsonify([song.search() for song in songs]), 200)
    def post(self):
        print(request.form.keys())
        title = request.form['title']
        genre = request.form['genre']
        release_date = date.today()
        audio_file = request.files['audio']
        
        if 'lyrics' in request.files:
            lyrics_file = request.files['lyrics']
        else:
            lyrics_file = None
        song = Song(title=title, release_date=release_date, genre=genre)
        db.session.add(song)
        db.session.commit()
        print("Added Song")

        if lyrics_file:
            lyrics_file.save(os.path.join('vue-project/src/assets','lyrics', str(song.song_id)+".txt"))
        audio_file.save(os.path.join('vue-project/src/assets','audio', str(song.song_id)+".mp3"))

        print("Saved files")

        temp = song_artist_association.insert().values(song_id=song.song_id, artist_id=request.form["artistId"])
        db.session.execute(temp)
        db.session.commit()
        print("Artist updated")
        return make_response(jsonify({"message": "Song has been added successfully!"}), 200)
    
class SongAPI(Resource):
    def get(self, song_id):
        song = Song.query.filter_by(song_id=song_id).first()
        if (not song) or (song.flag=="true"):
            return make_response(jsonify({"message":"Song not found."}), 400)
        return make_response(jsonify(song.search()), 200)
    
    def put(self, song_id):
        data = request.get_json()['params']
        if "rating" in data.keys():
            song = Song.query.filter_by(song_id=song_id).first()
            if song.rating is None:
                song.rating = data["rating"]
                song.no_users_rated = 1
            else:
                song.rating= (song.no_users_rated*song.rating + int(data["rating"]))*1.0/(song.no_users_rated+1)
                song.rating = round(song.rating, 2)
                song.no_users_rated += 1
            print("Updated rating")
        elif "flag" in data.keys():
            song = Song.query.filter_by(song_id=song_id).first()
            if data["flag"]=="true":
                song.flag="true"
            elif data["flag"]=="false":
                song.flag="false"
            else:
                return make_response(jsonify({"message":"Invalid request params"}))
            db.session.commit()
            print(f"Updated flag for song {song_id}")
        else:
            data = request.get_json()
            song = Song.query.filter_by(song_id=song_id).first()
            if not song:
                return make_response(jsonify({"message":"Song not found."}), 400)
            new_title = data.get("title")
            new_genre = data.get("genre")
            if new_title is not None:
                song.title=new_title
            if new_genre is not None:
                song.genre=new_genre
        db.session.commit()
        print(f'Updated song {song_id}')
        return make_response(jsonify({"message":"Song updated successfully!"}), 200)

    def delete(self, song_id):
        song = Song.query.filter_by(song_id=song_id).first()
        if not song:
            return make_response(jsonify({"message":"Song not found."}), 400)
        
        album_song=AlbumSong.query.filter_by(song_id=song_id).all()
        for i in album_song:
            db.session.delete(i)
        db.session.commit()
        print(f"Removed from {len(album_song)} albums") #necessary?
        
        playlist_song=PlaylistSong.query.filter_by(song_id=song_id).all()
        for i in playlist_song:
            db.session.delete(i)
        db.session.commit()
        print(f"Removed from {len(playlist_song)} playlists") #necessary?

        db.session.delete(song)
        db.session.commit()
        print("Deleted song")

        if os.path.exists(f'vue-project/src/assets/lyrics/{song_id}.txt'):
            os.remove(f'vue-project/src/assets/lyrics/{song_id}.txt')

        if os.path.exists(f'vue-project/src/assets/audio/{song_id}.mp3'):
            os.remove(f'vue-project/src/assets/audio/{song_id}.mp3')

        print(f"Removed files for song {song_id}")

        return make_response(jsonify({"message":"Song deleted successfully."}), 200)
    