<script setup>
import axios from "axios";
import creatorNav from "../components/creatorNav.vue"
</script>

<template>
    <creatorNav />
    <div class="container">
        <h3 class="green">{{ artistName }}'s profile</h3>
    </div>
    <div class="grid stat-grid">
        <hr>
        <div class="row stat-head-row">
            <div class="col stat-heading">
                Songs uploaded
            </div>
            <div class="col stat-heading">
                Albums uploaded
            </div>
        </div>
        <div class="row">
            <div class="col stat-value">
                {{ songs }}
            </div>
            <div class="col stat-value">
                {{ albums }}
            </div>
        </div>
        <hr>
        <div class="row stat-head-row">
            <div class="col stat-heading">
                Average song rating
            </div>
            <div class="col stat-heading">
                Average album rating
            </div>
        </div>
        <div class="row">
            <div class="col stat-value">
                {{ avgSongRating }}
            </div>
            <div class="col stat-value">
                {{ avgAlbumRating }}
            </div>
        </div>
        <hr>
    </div>
    <div class="container">
        <RouterLink to="/home" class="btn btn-success">User Dashboard</RouterLink>
    </div>
</template>
<script>
import axios from 'axios';
const API_BASE_URL = 'http://127.0.0.1:5000/api';

export default {
    data(){
        return{
        artistName: null,
        username: null,
        songs: null,
        albums: null,
        avgSongRating: null,
        avgAlbumRating: null
        };
    },
    created() {
        this.authToken = localStorage.getItem("authToken");
        if (this.authToken) {
            this.artistName = localStorage.getItem("artistName"),
            this.username = localStorage.getItem("username")

            //Song stats
            axios.get(`${API_BASE_URL}/songs?by=${localStorage.getItem('artistId')}`)
            .then(response=>{
                let song_list = response.data
                this.songs = song_list.length
                let temp = 0
                let n = 0
                for (var i in song_list){
                    console.log("Song: ", song_list[i])
                    if (song_list[i].rating){
                        console.log("Found song rating: ", song_list[i].rating)
                        temp += song_list[i].rating
                        n += 1
                    }
                }
                if (n!=0){
                    this.avgSongRating = temp/n;
                }
                console.log("Song stats updated")
                console.log(song_list)
                console.log(this.songs)

                //Album stats
                axios.get(`${API_BASE_URL}/albums?by=${localStorage.getItem('artistId')}`)
                .then(response=>{
                    let album_list = response.data
                    this.albums= album_list.length
                    let temp = 0
                    let n = 0
                    for (var j in album_list){
                        if (album_list[j].rating){
                            console.log("Found album rating: ", album_list[j].rating)
                            temp += album_list[j].rating
                            n += 1
                        }
                    }
                    if (n!=0){
                        this.avgAlbumRating = temp/n
                    }
                    console.log("Album stats updated")
                    console.log(album_list)
                    console.log(this.albums)
                })
                })
                
            }
        else {
            this.$router.push('/login')
        }
    },
}
</script>
<style>
.profile-star {
    display: flex;
    justify-content: center;
}
.stat-heading{
    font-size: large;
    font-weight: 700;
}
.stat-head-row{
    margin-bottom: 0% !important;
}
.stat-grid {
    background-color: rgba(148, 207, 215, 0.192);
    max-width: 60%;
    position: relative;
    left: 20%;
    display: grid;
    justify-items: stretch;
    justify-content: center;
    place-content: normal;
    margin-top: 2%;
}
hr{
    border-width: 3px;
    width: inherit;
    margin: 0%;
}
.stat-grid>.row{
    height: 50px;
}
.stat-value{
    font-size: 50px;
    color: hsla(160, 100%, 37%, 1);
}
</style>