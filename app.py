from flask import Flask
from application.security_framework import security, user_datastore
from flask_cors import CORS
from flask_restful import Api
from application.database import db
from application.models import * 
import bcrypt
import secrets
from flask_caching import Cache
from application.mailer import mail, Message

from application.worker import celery_init_app
from celery.schedules import crontab
from application.tasks import daily_reminder, monthly_reminder

app = Flask(__name__)

#db config
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///./quaver2_db.sqlite3'

#flask-security config
app.config['SECRET_KEY']='your-secret-key'
app.config['SECURITY_PASSWORD_HASH']='bcrypt'
app.config['SECURITY_PASSWORD_SALT']=secrets.SystemRandom().getrandbits(128)
# app.config['SECURITY_TOKEN_AUTHENTICATION_HEADER'] = 'Authorization'

#flask-mail config
app.config['MAIL_SERVER'] ='localhost'
app.config['MAIL_PORT'] = 1025
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = None
app.config['MAIL_PASSWORD'] = None
app.config['MAIL_DEFAULT_SENDER'] = 'no-reply@quaver.com'

api = Api(app)
app.app_context().push()

db.init_app(app)
app.app_context().push()

CORS(app)
mail.init_app(app)
celery_app = celery_init_app(app)

cache = Cache(app, config={
    'CACHE_TYPE': 'redis',
    'CACHE_REDIS_URL': "redis://127.0.0.1:6380/0",
    'CACHE_DEFAULT_TIMEOUT': 600 #default timeout = 10min
})

#moved to security_framework
#user_datastore = SQLAlchemyUserDatastore(db, User, Role)
#security = Security(app, user_datastore)

security.init_app(app, user_datastore)

def create_roles():
    roles_permissions = {
        'admin': 'admin-access',
        'user': 'user-access',
        'creator': 'creator-access'
    }

    for role_name, role_permissions in roles_permissions.items():
        role=Role.query.filter_by(name=role_name).first()
        #Add new roles to the db
        if not role:
            role=Role(name=role_name, description=role_permissions)
            db.session.add(role)
    db.session.commit()

def admin_user_creation():
    admin_role=Role.query.filter_by(name='admin').first()
    admin_user=User.query.filter(User.roles.any(id=admin_role.id)).first()
    #If there's no admin, create one
    if not admin_user:
        admin_username="admin123"
        admin_password="123"
        hashed_password=bcrypt.hashpw(admin_password.encode('utf-8'), bcrypt.gensalt())

        #Create the new user, and make him admin
        new_user=user_datastore.create_user(username=admin_username, password=hashed_password)
        user_datastore.add_role_to_user(new_user, 'admin')
        db.session.commit()
        return True
    return False

@app.route('/send_test_email')
def send_test_email():
    recipient_email = 'testuser@gmail.com'
    subject = "Quaver: Reminder to unwind today!"
    message = "Hey there, \n\nLooks like you have not unwinded with our collection of songs and albums today... \nTune in right now and listen to our top hits! \n\nWith love, \nTeam Quaver"

    msg = Message(subject=subject, recipients=[recipient_email])
    msg.body=message
    mail.send(msg)
    return "Test email sent"

'''
def send_email(username):
    recipient_email = f'{username}@gmail.com'
    subject = "Quaver: Reminder to unwind today!"
    message = "Hey there, \n\nLooks like you have not unwinded with our collection of songs and albums today... \nTune in right now and listen to our top hits! \n\nWith love, \nTeam Quaver"

    msg = Message(subject=subject, recipients=[recipient_email])
    msg.body=message
    mail.send(msg)
    return "Test email sent"
'''
@celery_app.on_after_configure.connect
def send_email(sender, **kwargs):
    sender.add_periodic_task(
        crontab(hour=18, minute=00), #send reminder at 6pm IST
        #crontab(hour=15, minute=43), #for testing
        daily_reminder.s('no-reply@quaver.com', 'Quaver: Reminder to Tune-in!'),
    )

@celery_app.on_after_configure.connect
def monthly_email(sender, **kwargs):
    sender.add_periodic_task(
        crontab(0,0,day_of_month=1), #send reminder on the 1st of every month
        #crontab(hour=15, minute=31), #for testing
        monthly_reminder.s('no-reply@quaver.com', 'Quaver: Monthly Report'),
    )

#from application.controllers import *
from routes.auth import RegisterAPI, LoginAPI, LogoutAPI
api.add_resource(RegisterAPI, '/api/register')
api.add_resource(LoginAPI, '/api/login')
api.add_resource(LogoutAPI, '/api/logout')

from routes.songs import SongsAPI, SongAPI
api.add_resource(SongsAPI, '/api/songs')
api.add_resource(SongAPI, '/api/songs/<int:song_id>')

from routes.playlists import PlaylistsAPI, PlaylistAPI
api.add_resource(PlaylistsAPI, '/api/playlists')
api.add_resource(PlaylistAPI, '/api/playlists/<int:playlist_id>')

from routes.artists import ArtistsAPI
api.add_resource(ArtistsAPI, '/api/artists')

from routes.users import UserAPI, UsersAPI
api.add_resource(UserAPI, '/api/users/<int:user_id>')
api.add_resource(UsersAPI, '/api/users')

from routes.albums import AlbumsAPI, AlbumAPI
api.add_resource(AlbumsAPI, '/api/albums')
api.add_resource(AlbumAPI, '/api/albums/<int:album_id>')

from routes.graphs import GraphsAPI
api.add_resource(GraphsAPI, '/api/graphs')

if __name__=="__main__":
    db.create_all()
    create_roles()
    admin_user_creation()
    app.run(debug=True)