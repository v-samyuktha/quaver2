<script setup>
import creatorNav from '../components/creatorNav.vue'
import songForm from '../components/songForm.vue'
let song_titles = localStorage.getItem('song_titles')
</script>

<template>
    <creatorNav />
    <div class="heading" style="margin: 0%;">
        <h3 class="green" style="margin: 0%;">Album Upload</h3>
    </div>
    <div v-show="songsDone==false" class="container col-md-4 col-md-offset-4" style="margin-top: 0%;">
        <p>To get started, add the album's songs:</p>
    </div>
    <songForm v-show="songsDone==false"/>
    <div v-show="songsDone==false" class="container col-md-4 col-md-offset-4" style="margin-top: 0%;">
        <button class="btn btn-outline-dark" @click="updateSongsDone()">Done</button>
    </div>
    <div v-show="song_titles.length>0" class="container col-md-4 col-md-offset-4" style="margin-top: 0%;">
        Songs added:<br>
        <div v-for="title in song_titles">
            {{ title }}
        </div>
    </div>
    <div v-show="songsDone==true" class="container col-md-4 col-md-offset-4" style="margin-top: 2%;">
        <form @submit.prevent="newAlbum">
            <div class="form-group">
                <label aria-required="true">Title: </label>   
                <input type="text" class="form-control" placeholder="Enter Title" id="albumTitle" name="albumTitle" required>
            </div>
            <br>
            <div class="form-group">
                <label aria-required="true">Genre: </label>   
                <input type="text" class="form-control" placeholder="Enter Genre" id="albumGenre" name="albumGenre" required>
            </div>
            <br>
            <div class="form-group">
                <label>Description: </label>   
                <input type="text" class="form-control" placeholder="(Optional)" id="desc" name="desc">
            </div>
        <br>
        <div class="row">
            <button class="button btn btn-outline-success" id="create" type="submit">Upload!</button>
        </div>
        </form>
    </div>
    <div class="container col-md-4 col-md-offset-4" style="margin-top: 0%;">
        <button class="button btn btn-outline-danger" id="cancel" @click="cancelUpload()">Cancel</button>
    </div>
</template>
<style>
.add-btn{
    padding:2%;
    font-size: small;
}
form{
    min-width: 30%;
}
#song-selected{
    color:hsla(160, 100%, 37%, 1);
    font-weight: 600;
}
#create, #cancel{
    margin: 2%;
}
</style>
<script>
import axios from 'axios';

const API_BASE_URL = 'http://localhost:5000/api';

export default {
    data(){
        return{
            songsDone: false
        }
    },
    created() {
        this.authToken = localStorage.getItem('authToken');
        if (this.authToken) {
            localStorage.setItem("song_ids", []);
            localStorage.setItem("song_titles", []);

        } else {
            this.$router.push('/login');
        }
    },
    methods: {
        newAlbum() {
            axios.post(`${API_BASE_URL}/albums`,{
                headers: {
                    Authorization: `${this.authToken}`
                },
                params: {
                    "artistId": localStorage.getItem("artistId"),
                    "title": document.getElementById("albumTitle").value,
                    "genre": document.getElementById("albumGenre").value,
                    "description": document.getElementById("desc").value,
                    "song_ids": JSON.parse(localStorage.getItem("song_ids"))
                }
            })
            .then(response => {
                console.log(response.data)
                //Reset localStorage
                localStorage.setItem("song_ids", []);
                localStorage.setItem("song_titles", [])
                this.$router.push("/creator_home")
            })
            .catch(error => {
                console.error("Error making album: ", error)
            })
        },
        updateSongsDone(){
            if (localStorage.getItem('song_ids').length==0){
                alert("Please upload atleast one song!")
            }
            else{
            this.songsDone=true;
            }
        },
        cancelUpload(){
            console.log("Cancelling album upload")
            if (localStorage.getItem('song_ids').length==0){
                this.$router.push("/creator_home")
            }
            else{
            let song_ids = JSON.parse(localStorage.getItem("song_ids"))
            song_ids.forEach(song_id => {
                axios.delete(`${API_BASE_URL}/songs/${song_id}`,{
                    headers: {
                    Authorization: `${this.authToken}`
                }
                })
                .then(response=>{
                    console.log(response);
                    //Reset localStorage
                    localStorage.setItem("song_ids", []);
                    localStorage.setItem("song_titles", [])
                })
                .catch(error=>console.error(error))
            })
            this.$router.push("/creator_home")
            }
        }
        }
};
</script>