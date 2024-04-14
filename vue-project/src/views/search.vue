<script setup>
import userNav from '@/components/userNav.vue'
import userSearch from '@/components/userSearch.vue';
import axios from 'axios';
</script>
<template>
    <div v-if="userRole">
        <userNav />
        <br>
        <userSearch />
    </div>

    <div v-if="songs && songs.length!=0" class="container" style="margin-top: 2%; margin-bottom: 0%;">
            <h4>{{ songs.length }} songs found for "{{ key }}"</h4>
    </div>
    <div v-if="songs && songs.length!=0" class="container d-flex" style="justify-content: center; margin-bottom: 2%;">
        <div class="arrow-buttons">
            <button class="btn btn-dark" onclick="document.querySelector('.CC-1').scrollLeft -= 300;">←</button>
        </div>
        <div class="d-flex card-container CC-1  col-10" style="height: 38vh; width:100% ;justify-content: left;">
            <div v-for="song in songs" :key="song.song_id" class="card mb-3">
                <div class="card-header">
                        <h3 class="card-title"> {{ song.title }} </h3>
                    </div>
                    <div class="star-container card-body" style="padding-bottom:0 ;">
                        <button class="btn btn-sm" style="padding: 0%;margin: 0%;padding-bottom: 2%;" @click="rateSong(song.song_id)">             
                            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-star" viewBox="0 0 16 16">
                                <path d="M2.866 14.85c-.078.444.36.791.746.593l4.39-2.256 4.389 2.256c.386.198.824-.149.746-.592l-.83-4.73 3.522-3.356c.33-.314.16-.888-.282-.95l-4.898-.696L8.465.792a.513.513 0 0 0-.927 0L5.354 5.12l-4.898.696c-.441.062-.612.636-.283.95l3.523 3.356-.83 4.73zm4.905-2.767-3.686 1.894.694-3.957a.565.565 0 0 0-.163-.505L1.71 6.745l4.052-.576a.525.525 0 0 0 .393-.288L8 2.223l1.847 3.658a.525.525 0 0 0 .393.288l4.052.575-2.906 2.77a.565.565 0 0 0-.163.506l.694 3.957-3.686-1.894a.503.503 0 0 0-.461 0z"></path>
                            </svg>    
                        </button>                   
                        <span v-if="song.rating==null" style="font-size: small;">
                                N/A
                        </span>
                        <span v-else style="font-size: small;">
                                {{ song.rating }}/5
                        </span>
                    </div>
                    <div class="card-body">
                        <h5 class="card-text">by <span style="font-style: italic;">{{ song.artist }}</span></h5>
                        <h5 class="card-text"><span style="font-style: italic;">{{ song.genre }}</span></h5>
                    </div>
                    <div class="card-footer">
                        <button class="btn btn-outline-success" @click="playSong(song.song_id)">Listen</button>
                        <button class="btn btn-outline-dark">+ Playlist</button>
                    </div>
            </div>
        </div>
        <div class="arrow-buttons">
            <button class="btn btn-dark" onclick="document.querySelector('.CC-1').scrollLeft += 300;">→</button>
        </div>
    </div>
    <div v-else class="container" style="margin-top: 2%; margin-bottom: 0%;">
            <h4>No songs found for "{{ key }}"</h4>
    </div>

    <div v-if="albums && albums.length!=0" class="container" style="margin-top: 2%; margin-bottom: 0%;">
            <h4>{{ albums.length }} albums found for "{{ key }}"</h4>
    </div>
    <div v-if="albums && albums.length!=0" class="container d-flex" style="justify-content: center; margin-bottom: 2%;">
        <div class="arrow-buttons">
            <button class="btn btn-dark" onclick="document.querySelector('.CC-2').scrollLeft -= 300;">←</button>
        </div>
        <div class="d-flex card-container CC-2  col-10" style="height: 38vh; width:100% ;justify-content: left;">
            <div v-for="album in albums" :key="album.album_id" class="card mb-3">
                    <div class="card-header">
                        <h3 class="card-title"> {{ album.title }} </h3>
                    </div>
                    <div class="card-body">
                        <h5 class="card-text">by <span style="font-style: italic;">{{ album.artist }}</span></h5>
                        <h5 class="card-text"><span style="font-style: italic;">{{ album.song_ids.length }} songs</span></h5>
                    </div>
                    <div class="card-footer">
                        <button class="btn btn-outline-success">View</button>
                    </div>
            </div>
        </div>
        <div class="arrow-buttons">
            <button class="btn btn-dark" onclick="document.querySelector('.CC-2').scrollLeft += 300;">→</button>
        </div>
    </div>
    <div v-else class="container" style="margin-top: 2%; margin-bottom: 0%;">
            <h4>No albums found for "{{ key }}"</h4>
    </div>

    <div v-if="playlists && playlists.length!=0" class="container" style="margin-top: 2%; margin-bottom: 0%;">
            <h4>{{ playlists.length }} playlists found for "{{ key }}"</h4>
    </div>
    <div v-if="playlists && playlists.length!=0" class="container d-flex" style="justify-content: center; margin-bottom: 2%;">
        <div class="arrow-buttons">
            <button class="btn btn-dark" onclick="document.querySelector('.CC-3').scrollLeft -= 300;">←</button>
        </div>
        <div class="d-flex card-container CC-3  col-10" style="height: 38vh; width:100% ;justify-content: left;">
            <div v-for="playlist in playlists" :key="playlist.playlist_id" class="card mb-3">
                    <div class="card-header">
                        <h3 class="card-title"> {{ playlist.title }} </h3>
                    </div>
                    <div class="card-body">
                        <h5 class="card-text"><span style="font-style: italic;">{{ playlist.song_ids.length }} songs</span></h5>
                    </div>
                    <div class="card-footer">
                        <RouterLink :to="{ path: '/playlists/'+playlist.playlist_id }" class="btn btn-outline-success">View</RouterLink>
                        <button class="btn btn-outline-dark" @click="deletePlaylist(playlist.playlist_id)">Delete</button>
                    </div>
            </div>
        </div>
        <div class="arrow-buttons">
            <button class="btn btn-dark" onclick="document.querySelector('.CC-3').scrollLeft += 300;">→</button>
        </div>
    </div>
    <div v-else class="container" style="margin-top: 2%; margin-bottom: 0%;">
            <h4>No playlists found for "{{ key }}"</h4>
    </div>
</template>
<script>
const API_BASE_URL = 'http://127.0.0.1:5000/api';
    export default {
        data() {
            return {
                key: null,
                userRole: false,
                songs: null,
                albums: null,
                playlists: null
            };
        },
        created() {
                this.key = this.$route.query["key"];
                if(localStorage.getItem("userRole"))
                    this.userRole=true;
                this.getSongs();
                this.getAlbums();
                this.getPlaylists();
        },
        methods: {
            getSongs(){
                axios.get(`${API_BASE_URL}/songs?key=${this.key}`)
                .then(response=>{
                    this.songs = response.data;
                    console.log(this.songs.length)
                })
                .catch(error=>console.error(error))
            },
            getAlbums(){
                axios.get(`${API_BASE_URL}/albums?key=${this.key}`)
                .then(response=>{
                    this.albums = response.data;
                    console.log(this.albums.length)
                })
                .catch(error=>console.error(error))
            },
            getPlaylists(){
                axios.get(`${API_BASE_URL}/playlists?key=${this.key}`,{
                headers: {
                    Authorization: `${this.authToken}`
                },
                params: {
                    "userId": localStorage.getItem("userId")
                }
            })
                .then(response=>{
                    this.playlists = response.data;
                    console.log(this.playlists.length)
                })
                .catch(error=>console.error(error))
            },
            rateSong(song_id) {
            console.log(`Rating song ${song_id}`);
            let rating = prompt("Rate the song on a scale of 1 to 5:")
            if (rating !== null){
                let possible_ratings = ['1','2','3','4','5']
                if (possible_ratings.includes(rating)){
                    this.putRating(song_id, rating)
                }
                else{
                    alert("Please rate a valid number between 1-5")
                }
            }
        },
        putRating(song_id, rating){
            axios.put(`${API_BASE_URL}/songs/${song_id}`,{
                headers: {
                    Authorization: `${this.authToken}`
                },
                params: {
                    "rating": rating
                }
            })
            .then(response=>{
                console.log(response.data.message);
                alert("Thank you for rating!");
            })
            .catch(error=>{
                console.error(error);
            })
        }
        }
    };
</script>