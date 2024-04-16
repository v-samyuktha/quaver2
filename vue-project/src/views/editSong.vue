<script setup>
import creatorNav from '../components/creatorNav.vue'
</script>

<template>
    <creatorNav />
    <div class="heading">
        <h3 class="green">Editing Song "{{ song.title }}"</h3>
    </div>
    <div class="container col-md-4 col-md-offset-4" style="margin-top: 2%;">
        <form @submit.prevent="editSong" enctype="multipart/form-data">
            <div class="form-group required">
                <label class="control-label" aria-required="true">Title: </label>   
                <input type="text" class="form-control" placeholder="Enter Title" id="title" v-model="song.title" name="title" required>
            </div>
            <br>
            <div class="form-group required">
                <label class="control-label" aria-required="true">Genre: </label>   
                <input type="text" class="form-control" placeholder="Enter Genre" id="genre" v-model="song.genre" name="genre" required>
            </div>
            <br>
            <div class="form-group">
                <label class="control-label">Attach audio, if updated: </label>  
                <input type="file" class="form-control" accept=".mp3" id="audio" name="audio">  
            </div>
            <br>
            <div class="form-group">
                <label>Attach lyrics, if updated: </label>  
                <input type="file" class="form-control" accept=".txt" id="lyrics" name="lyrics">  
            </div>
        <br>
        <div class="row">
            <button class="button btn btn-outline-success" id="create" type="submit">Confirm</button>
            <button class="button btn btn-outline-danger" id="cancel" onclick="history.go(-1)">Cancel</button>
        </div>
        </form>
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
.form-group.required .control-label:after {content:"*";color:rgb(154, 19, 19);}
</style>
<script>
import axios from 'axios';

const API_BASE_URL = 'http://localhost:5000/api';

export default {
    data(){
        return{
            song: null
        }
    },
    created() {
        this.authToken = localStorage.getItem('authToken');
        if (this.authToken) {
            this.getSong();
        } else {
            this.$router.push('/login');
        }
    },
    methods: {
        getSong(){
            console.log(`Song id: ${this.$route.params.song_id}`)
            axios.get(`${API_BASE_URL}/songs/${this.$route.params.song_id}`)
            .then(response=>{
                console.log(response.data)
                this.song = response.data;
            })
            .catch(error=>{
                console.error(error)
            })
        },
        editSong() {
            console.log("Editing song")
            var audioFile = document.getElementById('audio').files[0];
            var lyricsFile = document.getElementById('lyrics').files[0]; 
            var artistId = localStorage.getItem("artistId")
            var formData = new FormData();
            formData.append('title', this.song.title);
            formData.append('genre', this.song.genre);
            formData.append('artistId', artistId)
            if (audioFile) {
                formData.append('audio', audioFile);
            }
            if (lyricsFile) {
                formData.append('lyrics', lyricsFile);
            }
            for (var pair of formData.entries()) {
                console.log(pair[0] + ', ' + pair[1]);
            }
            axios.put(`${API_BASE_URL}/songs/${this.$route.params.song_id}`, formData)
            .then(response => {
                console.log(response.data)
                this.$router.push("/creator_home")
            })
            .catch(error => {
                console.error("Error fetching songs: ", error)
            })}
        }
};
</script>