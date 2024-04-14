#NOT IN USE
#MOVED TO RESTFUL

from flask import request, jsonify, make_response
from flask import current_app as app
from .models import *
from .database import db
from app import user_datastore
from flask_security import login_user, current_user
import bcrypt
from datetime import date

@app.route('/', methods = ['GET', 'POST'])
def hello_world():
    if request.method=="GET":
        var1 = 'first variable'
        var2 = 1+2
        return make_response(jsonify({"v1":var1, "v2":var2}), 200)
    elif request.method=="POST":
        data=request.get_json()
        var1=data["v1"]
        var2=data["v2"]
        print(var1, var2)
        return make_response(jsonify({"message":"Post request"}), 200)
    
@app.route('/api/register', methods=["POST"])
def register():
    data = request.get_json()
    username = data["username"]
    password = data["password"]
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    try:
        new_user = user_datastore.create_user(username=username, password=hashed_password)
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
    
@app.route('/api/login', methods=["POST"])
def login():
    data = request.get_json()
    username = data["username"]
    password = data["password"]
    user = user_datastore.find_user(username=username)
    if user:
        if bcrypt.checkpw(password.encode('utf-8'), user.password):
            login_user(user) #session based login
            activity = UserActivity(user_id = user.id, activity_type="login")
            db.session.add(activity)
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
        make_response(jsonify({"message": "Invalid username or password."}), 400)

@app.route("/api/songs", methods=["GET", "POST"])
def songs_fn():
    if request.method=="GET":
        songs = Song.query.all()
        return make_response(jsonify([song.search() for song in songs]), 200)
    elif request.method=="POST":
        data = request.get_json()
        title = data["title"]
        release_date = date.today()
        genre = data["genre"]

        song = Song(title=title, release_date=release_date, genre=genre)
        db.session.add(song)
        db.session.commit()
        print("Added Song")

        artist = Artist.query.filter_by(username=current_user.username).first()
        temp = song_artist_association.insert().values(song_id=song.song_id, artist_id=artist.artist_id)
        db.session.execute(temp)
        db.session.commit()
        print("Artist updated")
        return make_response(jsonify({"message": "Song has been added successfully!"}), 200)

@app.route("/api/songs/<int:song_id>", methods = ["GET","PUT", "DELETE"])
def song_operation(song_id):
    if request.method == "GET":
        song = Song.query.filter_by(song_id=song_id).first()
        if not song:
            return make_response(jsonify({"message":"Song not found."}))
        return make_response(jsonify(song.search()))
    
    elif request.method=="PUT":
        data = request.get_json()
        song = Song.query.filter_by(song_id=song_id).first()
        if not song:
            return make_response(jsonify({"message":"Song not found."}))
        new_title = data.get("title")
        new_genre = data.get("genre")
        if new_title is not None:
            song.title=new_title
        if new_genre is not None:
            song.genre=new_genre
        db.session.commit()
        print(f'Updated song {song_id}')

        return make_response(jsonify({"message":"Song updated successfully!"}))

    elif request.method=="DELETE":
        song = Song.query.filter_by(song_id=song_id).first()
        if not song:
            return make_response(jsonify({"message":"Song not found."}))
        
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

        return make_response(jsonify({"message":"Song deleted successfully."}), 200)

@app.route("/api/playlists", methods=["GET", "POST", "PUT", "DELETE"])
def playlists_fn():
    if request.method=="GET":
        playlists = Playlist.query.all()
        return make_response(jsonify([playlist.search() for playlist in playlists]), 200) #??
    
@app.route("/api/artists", methods=["GET", "POST", "PUT", "DELETE"])
def artists_fn():
    if request.method=="GET":
        artists = Artist.query.all()
        return make_response(jsonify(artists.search()), 200)
    
    elif request.method=="POST":
        data = request.get_json()
        name = data["name"]
        username = current_user.username
        artist = Artist(name=name, username=username)
        db.session.add(artist)
        db.session.commit()
        print("Added Artist")
    
        user_datastore.add_role_to_user(current_user, "creator")
        db.session.commit()

        return make_response(jsonify({"message": "Registered as Creator Successfully!"}), 200)
