from flask import jsonify, request, make_response
from application.models import *
from application.security_framework import user_datastore, bcrypt, current_user, login_user, logout_user, roles_accepted, auth_token_required
from flask_restful import Resource
from datetime import datetime, date, timedelta
import matplotlib
import matplotlib.pyplot as plt

class GraphsAPI(Resource):
    @roles_accepted('admin')
    @auth_token_required
    def get(self):
        matplotlib.use("agg")
        #Graph: Timeline for total accounts
        joining_dates=User.query.with_entities(User.joined_on).all()
        print(joining_dates)
        temp = []
        for x in joining_dates:
            print(x[0])
            if x[0] is not None:
                temp.append(x)
            else:
                print("Empty date")
        dates=[] #array of joining dates
        for i in sorted(temp):
            dates.append(datetime.strptime(getattr(i, "joined_on"), '%Y-%m-%d').date())
        #brute way to force the recent date onto graphs
        dates.append(date.today() + timedelta(days=1))
        x=[] #x axis: dates
        y=[] #y axis: number of accounts
        ct=0
        dates.sort()
        temp=dates[0]
        for j in dates:
            print("date: ", j)
            if j==temp:
                ct+=1
            else:
                x.append(f'{temp.day}-{temp.month}')
                y.append(ct)
                temp=j
                ct+=1
        print("X:", x)
        print("Y:", y)
        plt.plot(x,y, 'o')
        plt.plot(x,y, color='black')

        graph_directory = "./vue-project/src/assets"
        plt.savefig(graph_directory+"/joining_dates.png", bbox_inches='tight') 
        plt.clf()  

        #Graph: Timeline for total songs
        release_dates=Song.query.with_entities(Song.release_date).all()
        print(release_dates)
        temp = []
        for x in release_dates:
            print(x[0])
            if x[0] is not None:
                temp.append(x)
        dates=[] #array of release dates
        for i in sorted(temp):
            dates.append(datetime.strptime(getattr(i, "release_date"), '%Y-%m-%d').date())
        
        #brute way to force the recent date onto graphs
        dates.append(date.today() + timedelta(days=1))
        x=[] #x axis: dates
        y=[] #y axis: number of songs
        ct=0
        dates.sort()
        temp=dates[0]
        for j in dates:
            print("date: ", j)
            if j==temp:
                ct+=1
            else:
                x.append(f'{temp.day}-{temp.month}')
                y.append(ct)
                temp=j
                ct+=1
        print("X:", x)
        print("Y:", y)
        plt.plot(x,y, 'o')
        plt.plot(x,y, color='black')
        plt.savefig(graph_directory+"/song_releases.png", bbox_inches="tight")
        plt.clf()

        return make_response(jsonify({"message": "Graphs saved successfully"}))