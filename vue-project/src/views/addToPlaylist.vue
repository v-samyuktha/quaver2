<script setup>
import userNav from '../components/userNav.vue'
</script>

<template>
    <userNav />
    <div class="heading">
        <h3 class="green">Where would you like to include "{{ song.title }}" ?</h3>
    </div>
    <div class="container playlist-form">
        <select class="form-select" placeholder="Select a playlist" id="selected_playlist">
            <option v-for="playlist in playlists" :value="playlist.playlist_id">{{ playlist.title }}</option>
        </select>
    </div>
    <div class="container">
        <button type="button" class="btn btn-outline-success" style="margin: 2%;" @click="addSong()">Confirm</button>
        <button class="button btn btn-outline-danger" id="cancel" onclick="history.go(-1)">Cancel</button>
    </div>
</template>
<script>
import axios from 'axios';
const API_BASE_URL = 'http://127.0.0.1:5000/api';

export default {
    data() {
        return {
            song_id:'',
            song: null,
            playlists: null,
            selected_id: null
        };
    },
    created() {
        this.authToken = localStorage.getItem("authToken");
        if (this.authToken) {
            this.getSong();
            this.getPlaylists();
        }
        else {
            this.$router.push('/login')
        }
    },
    methods: {
        getSong() {
            this.song_id = this.$route.query.song_id;
            console.log(this.$route.query.song_id)
            axios.get(`${API_BASE_URL}/songs/${this.song_id}`,{
                headers: {
                    Authorization: `${this.authToken}`
                }
            })
            .then(response => {
                this.song = response.data;
                console.log("Fetched song details")
            })
            .catch(error => {
                console.error("Error fetching song: ", error)
            });
        },
        getPlaylists() {
            axios.get(`${API_BASE_URL}/playlists`,{
                headers: {
                    Authorization: `${this.authToken}`
                }
            })
            .then(response => {
                this.playlists = response.data;
                console.log("Fetched playlists")
            })
            .catch(error => {
                console.error("Error fetching playlists: ", error)
            });
        },
        addSong(){
            this.selected_id = document.getElementById("selected_playlist").value;
            console.log(this.selected_id + " selected");
            axios.put(`${API_BASE_URL}/playlists/${this.selected_id}?add_song=${this.song_id}`,{
                headers: {
                    Authorization: `${this.authToken}`
                }
            })
            .then(response => {
                console.log(response.data.message);
                this.goToPlaylists();
            })
            .catch(error => {
                console.error("Error adding song to playlist: ", error)
            });
        },
        goToPlaylists(){
            this.$router.push("/playlists")
        }
    }
}
</script>
<style>
.playlist-form{
    max-width: 30%;
}
</style>