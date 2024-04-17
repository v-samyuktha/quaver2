<script setup>
import creatorNav from '../components/creatorNav.vue'
</script>

<template>
    <creatorNav />
    <div class="heading">
        <h3 class="green">Song Upload</h3>
    </div>
    <div class="container col-md-4 col-md-offset-4" style="margin-top: 2%;">
        <form @submit.prevent="newSong" enctype="multipart/form-data">
            <div class="form-group required">
                <label class="control-label" aria-required="true">Title: </label>   
                <input type="text" class="form-control" placeholder="Enter Title" id="title" name="title" required>
            </div>
            <br>
            <div class="form-group required">
                <label class="control-label" aria-required="true">Genre: </label>   
                <input type="text" class="form-control" placeholder="Enter Genre" id="genre" name="genre" required>
            </div>
            <br>
            <div class="form-group required">
                <label class="control-label">Upload audio</label>  
                <input type="file" class="form-control" accept=".mp3" id="audio" name="audio" required>  
            </div>
            <br>
            <div class="form-group">
                <label>Upload lyrics </label>  
                <input type="file" class="form-control" accept=".txt" id="lyrics" name="lyrics">  
            </div>
        <br>
        <div class="row">
            <button class="button btn btn-outline-success" id="create" type="submit">Upload!</button>
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
            authToken: ''
        }
    },
    created() {
        this.authToken = localStorage.getItem('authToken');
        if (this.authToken) {
            ;
        } else {
            this.$router.push('/login');
        }
    },
    methods: {
        newSong() {
            var audioFile = document.getElementById('audio').files[0];
            var lyricsFile = document.getElementById('lyrics').files[0]; 
            var title = document.getElementById("title").value
            var genre = document.getElementById("genre").value
            var artistId = localStorage.getItem("artistId")
            var formData = new FormData();
            formData.append('title', title);
            formData.append('genre', genre);
            formData.append('artistId', artistId)
            formData.append('audio', audioFile);
            if (lyricsFile) {
                formData.append('lyrics', lyricsFile);
            }
            
            axios.post(`${API_BASE_URL}/songs`, formData, {
                headers: {
                    Authorization: this.authToken
                }
            })
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