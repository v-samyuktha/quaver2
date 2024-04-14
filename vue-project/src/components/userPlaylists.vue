<template>
    <div v-if="playlists" class="heading" style="margin-top: 2%; margin-bottom: 0%;">
            <h3><strong>Your Playlists</strong></h3><br>
            <RouterLink to="/new_playlist" class="btn btn-outline-success">+ Create</RouterLink>
    </div>
    <div v-if="playlists && playlists.length>0" class="container d-flex" style="justify-content: center; margin-bottom: 2%; margin-top: 2%;">
        <div class="arrow-buttons">
            <button class="btn btn-dark" onclick="document.querySelector('.CC-2').scrollLeft -= 300;">←</button>
        </div>
        <div class="d-flex card-container CC-2  col-10" style="height: 38vh; width:100% ;justify-content: left;">
            <div v-for="playlist in playlists" :key="playlist.id" class="card">
                    <div class="card-header">
                        <h3 class="card-title"> {{ playlist.title }} </h3>
                    </div>
                    <div class="card-body">
                        <h5 class="card-text">{{ playlist.song_ids.length }} Songs</h5><br>
                    </div>
                    <div class="card-footer">
                        <RouterLink :to="{ path: '/playlists/'+playlist.playlist_id }" class="btn btn-outline-success">View</RouterLink>
                        <button class="btn btn-outline-dark" @click="deletePlaylist(playlist.playlist_id)">Delete</button>
                    </div>
            </div>
        </div>
        <div class="arrow-buttons">
            <button class="btn btn-dark" onclick="document.querySelector('.CC-2').scrollLeft += 300;">→</button>
        </div>
    </div>
    <div v-else class="container" style="padding-bottom: 2vh;">
        No playlists found.
    </div>
</template>

<script>
import axios from 'axios';
const API_BASE_URL = 'http://127.0.0.1:5000/api';

export default {
    data() {
        return {
            playlists: null,
            flashMessage: null,
            path: ''
        };
    },
    created() {
        this.authToken = localStorage.getItem("authToken");
        if (this.authToken) {
            this.getPlaylists();
        }
        else {
            this.$router.push('/login')
        }
    },
    methods: {
        getPlaylists() {
            axios.get(`${API_BASE_URL}/playlists`,{
                headers: {
                    Authorization: `${this.authToken}`
                },
                params: {
                    "userId": localStorage.getItem("userId")
                }
            })
            .then(response => {
                this.playlists = response.data;
            })
            .catch(error => {
                console.error("Error fetching playlists: ", error)
            });
        },
        deletePlaylist(playlist_id){
            console.log("To delete playlist " + playlist_id)
            if(confirm("Are you sure of deleting the playlist?")==true){
                console.log("confirmed")
                axios.delete(`${API_BASE_URL}/playlists/${playlist_id}`, {headers:{
                    Authorization: `${this.authToken}`
                    }
                })
                .then(response => {
                console.log(response.data); 
                location.reload();
            })
                .catch(error=> console.error(error))
            }
        }
    }
}
</script>
<style>
    .card-header{
        display:flex;
        width: 100%;
        padding: 2%;
        align-items: center;
    }
    .card-footer{
        display:flex;
        width: 100%;
        padding: 2%;
        align-items: center;
    }
    .card-footer>button{
        width:auto;
        margin: 2%
    }
    .card-title{
        font-size: x-large;
        font-family:'Gill Sans', 'Gill Sans MT', Calibri, 'Trebuchet MS', sans-serif;
        padding: 2%;
    }
    .card-header{
        background-color: rgba(122, 231, 195, 0.817);
    }
</style>