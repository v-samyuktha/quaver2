<template>
    <div class="container col-md-4 col-md-offset-4" style="margin-top: 2%;">
        <form enctype="multipart/form-data" @submit.prevent="newSong()">
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
            <button class="button btn btn-outline-success" id="create">Add to Album</button>
        </div>
        </form>
    </div>
</template>
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
            formData.append('audio', audioFile);
            formData.append('lyrics', lyricsFile);
            formData.append('artistId', artistId)
            axios.post(`${API_BASE_URL}/songs`, formData, {
                headers: {
                    Authorization: `${this.authToken}`
                }
            })
            .then(response => {
                console.log(response.data);
                this.$parent.atleastOneSong=true;
                console.log(`Atleast one song: ${this.$parent.atleastOneSong}`)

                let songs = null;
            axios.get(`${API_BASE_URL}/songs`, {
                headers: {
                    Authorization: `${this.authToken}`
                }
            })
            .then(response=>{
                console.log(response.data)
                songs = response.data[response.data.length-1].song_id;
                console.log(`New song id: ${parseInt(songs)}`)

                let temp1 = localStorage.getItem('song_ids');
            //Handles empty array case
            temp1 = (temp1) ? JSON.parse(temp1) : [];
            console.log(songs)
            temp1.push(parseInt(songs));
            console.log("temp1: ", temp1);
            localStorage.setItem('song_ids', JSON.stringify(temp1));

            let temp2 = localStorage.getItem('song_titles');
            temp2 = (temp2) ? JSON.parse(temp2) : [];
            temp2.push(document.getElementById("title").value);
            console.log("temp2: ", temp2);
            localStorage.setItem('song_titles', JSON.stringify(temp2));

            //Alert success
            alert(`Added ${document.getElementById("title").value} to album!`)

            //Clear the fields
            document.getElementById("title").value = '';
            document.getElementById("genre").value = '';
            document.getElementById("audio").value = null;
            document.getElementById("lyrics").value = null;

            })
            })
            .catch(error => {
                console.error("Error uploading song: ", error)
            })

        }
        }
};
</script>
<style>
.form-group.required .control-label:after {content:"*";color:rgb(154, 19, 19);}
</style>