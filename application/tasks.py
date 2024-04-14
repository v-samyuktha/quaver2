from celery import shared_task
from .models import *
import flask_excel as excel
from .mail_service import send_message
from jinja2 import Template

'''
@shared_task(ignore_result=False)
def create_resource_csv():
    stud_res = StudyResource.query.with_entities(
        StudyResource.topic, StudyResource.description).all()

    csv_output = excel.make_response_from_query_sets(
        stud_res, ["topic", "description"], "csv")
    filename = "test.csv"

    with open(filename, 'wb') as f:
        f.write(csv_output.data)

    return filename
'''

@shared_task(ignore_result=True)
def daily_reminder(to, subject):
    users = User.query.filter(User.roles.any(Role.name == 'user')).all()
    for user in users:
        if not user.loginToday():
            with open('application/test.html', 'r') as f:
                template = Template(f.read())
                send_message(f'{user.username}@gmail.com', subject,
                                template.render(email=f'{user.username}@gmail.com'))
    return "OK"

@shared_task(ignore_result=True)
def monthly_reminder(to, subject):
    artists = Artist.query.all()
    for artist in artists:
        #Song stats
        songs = artist.songs
        no_of_songs = len(songs)
        avg_song_rating = None
        temp = 0
        n = 0
        for song in songs:
            if song.rating:
                temp += song.rating
                n += 1
        if n!=0:
            avg_song_rating = temp/n
        print("Song stats updated")

        #Album stats
        albums = Album.query.filter_by(artist_id = artist.artist_id).all()
        no_of_albums = len(albums)
        avg_album_rating = None
        temp = 0
        n = 0
        for album in albums:
            if album.rating:
                temp += album.rating
                n += 1
        if n!=0:
            avg_album_rating = temp/n
        print("Album stats updated")

        with open('application/monthly_report.html', 'r') as f:
            template = Template(f.read())
            send_message(f'{artist.username}@gmail.com', subject,
                template.render(songs=no_of_songs, avgSongRating = avg_song_rating, albums = no_of_albums, avgAlbumRating = avg_album_rating))
    return "OK"

