from .database import db
from flask_security import UserMixin, RoleMixin, AsaList
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.mutable import MutableList
from sqlalchemy import Boolean, DateTime, Column, Integer, String, ForeignKey
from datetime import datetime, timedelta

class RolesUsers(db.Model):
    __tablename__ = 'roles_users'
    id = Column(Integer(), primary_key=True)
    user_id = Column('user_id', Integer(), ForeignKey('users.id'))
    role_id = Column('role_id', Integer(), ForeignKey('roles.id'))

class Role(db.Model, RoleMixin):
    __tablename__ = 'roles'
    id = Column(Integer, primary_key=True)
    name = Column(String(80), unique=True)
    description = Column(String(255))
    permissions = Column(MutableList.as_mutable(AsaList()), nullable=True)

#MAD1 => username was primary key!!
#flagged user(creator) has active=False
class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String)
    password = Column(String, nullable=False)
    #acc_type = Column(String, default="user")
    joined_on = Column(String)
    last_login_at = Column(DateTime())
    current_login_at = Column(DateTime())
    last_login_ip = Column(String(100))
    current_login_ip = Column(String(100))
    login_count = Column(Integer)
    active = Column(Boolean())
    fs_uniquifier = Column(String(64), unique=True, nullable=False)
    confirmed_at = Column(DateTime())
    roles = relationship('Role', secondary='roles_users',
                         backref=backref('users', lazy='dynamic'))
    def search(self):
        return {
            "user_id": self.id,
            "username": self.username,
            "joined_on": self.joined_on
        }
    
    def loginToday(self):
        if(self.last_login_at):
            recentLogin = self.last_login_at.strftime("%d/%m/%Y")
            print(f"Last seen: {recentLogin}")
            todaysDate = datetime.now().strftime("%d/%m/%Y")
            print(f"Today's date: {todaysDate}")
            if recentLogin==todaysDate:
                print("MATCHED")
                return True
        return False
    
class UserActivity(db.Model):
    __tablename__ = 'user_activity'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False) 
    activity_type = db.Column(db.String(50), nullable=False)  
    activity_timestamp = db.Column(db.DateTime, default=datetime.utcnow)

# Song-Artist relationship table
song_artist_association = db.Table('song_artist_association', db.Model.metadata,
    db.Column('song_id', db.Integer, db.ForeignKey('songs.song_id')),
    db.Column('artist_id', db.Integer, db.ForeignKey('artists.artist_id'))
)

class Song(db.Model):
    __tablename__ = 'songs'
    song_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    duration = db.Column(db.String(20))
    release_date = db.Column(db.String)
    genre = db.Column(db.String(50))
    rating = db.Column(db.Integer)
    no_users_rated = db.Column(db.Integer, default=0)
    flag = db.Column(db.String(5), default="false")
    artists = db.relationship('Artist', secondary=song_artist_association, back_populates='songs')

    # enables json serialization
    def search(self):
        # to do: songs with multiple artists
        return {
            "song_id": self.song_id,
            "title": self.title,
            "release_date": self.release_date,
            "genre": self.genre,
            "rating": self.rating,
            "no_users_rated": self.no_users_rated,
            "flag": self.flag,
            "artist": self.artists[0].__dict__["name"]
        }

class Artist(db.Model):
    __tablename__ = 'artists'
    artist_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    bio = db.Column(db.Text)
    username = db.Column(db.String(), db.ForeignKey('users.username'))
    songs = db.relationship('Song', secondary=song_artist_association, back_populates='artists')

    def search(self):
        return {
                    "artist_id": self.artist_id,
                    "name": self.name,
                    "bio": self.bio,
                    "username": self.username,
                }
    
class PlaylistSong(db.Model):
    __tablename__ = 'playlist_songs'
    id = db.Column(db.Integer, primary_key=True)
    playlist_id = db.Column(db.Integer, db.ForeignKey('playlists.playlist_id'))
    song_id = db.Column(db.Integer, db.ForeignKey('songs.song_id'))
    position = db.Column(db.Integer)
    playlists = db.relationship('Playlist', back_populates='songs')

class Playlist(db.Model):
    __tablename__ = 'playlists'
    playlist_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(255))
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    songs = db.relationship('PlaylistSong', order_by='PlaylistSong.position', back_populates='playlists')
    def search(self):
        songs = PlaylistSong.query.filter_by(playlist_id=self.playlist_id).all()
        song_ids = []
        for song in songs:
            song_ids.append(song.song_id)
        return {
            "playlist_id": self.playlist_id,
            "title": self.title,
            "description": self.description,
            "created_at": self.created_at,
            "created_by": self.created_by,
            "song_ids": song_ids
        }

class AlbumSong(db.Model):
    __tablename__ = 'album_songs'
    id = db.Column(db.Integer, primary_key=True)
    album_id = db.Column(db.Integer, db.ForeignKey('albums.album_id'))
    song_id = db.Column(db.Integer, db.ForeignKey('songs.song_id'))
    albums = db.relationship('Album', back_populates='songs')

class Album(db.Model):
    __tablename__ = 'albums'
    album_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    description = db.Column(db.Text)
    created_at = db.Column(db.String)
    artist_id = db.Column(db.String, db.ForeignKey('artists.artist_id'))
    rating = db.Column(db.Integer)
    no_users_rated = db.Column(db.Integer, default=0)
    genre = db.Column(db.String)
    flag = db.Column(db.String(5), default="false")
    songs = db.relationship('AlbumSong', back_populates='albums')

    def search(self):
        songs = AlbumSong.query.filter_by(album_id=self.album_id).all()
        song_ids = []
        for song in songs:
            song_ids.append(song.song_id)

        artist = Artist.query.filter_by(artist_id = self.artist_id).first()
        return {
            "album_id": self.album_id,
            "title": self.title,
            "description": self.description,
            "created_at": self.created_at,
            "artist_id": self.artist_id,
            "genre": self.genre,
            "rating": self.rating,
            "no_users_rated": self.no_users_rated,
            "flag": self.flag,
            "song_ids": song_ids,
            "artist_name": artist.name
        }
