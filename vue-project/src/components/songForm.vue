<template>
    <div class="container col-md-4 col-md-offset-4" style="margin-top: 2%;">
        <form enctype="multipart/form-data">
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
                <input type="file" class="form-control" accept=".mp3" id="audio" name="audio">  
            </div>
            <br>
            <div class="form-group">
                <label>Upload lyrics </label>  
                <input type="file" class="form-control" accept=".txt" id="lyrics" name="lyrics">  
            </div>
        <br>
        <div class="row">
            <button class="button btn btn-outline-success" id="create" @click="newSong()">Add to Album</button>
        </div>
        </form>
    </div>
</template>
<script>
import axios from 'axios';

const API_BASE_URL = 'http://localhost:5000/api';

export default {
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
            formData.append('audio', audioFile);
            formData.append('lyrics', lyricsFile);
            formData.append('artistId', artistId)
            axios.post(`${API_BASE_URL}/songs`, formData)
            .then(response => {
                console.log(response.data);
                this.$parent.songs+=1;
            })
            .catch(error => {
                console.error("Error uploading song: ", error)
            })}
        }
};
</script>
<style>
.form-group.required .control-label:after {content:"*";color:rgb(154, 19, 19);}
</style>