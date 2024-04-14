<template>
    <div v-if="albums" class="container" style="margin-top: 2%; margin-bottom: 0%;">
            <h3><strong>Visible Albums</strong></h3>
    </div>
    <div v-if="albums" class="container d-flex" style="justify-content: center; margin-bottom: 2%;">
        <div class="arrow-buttons">
            <button class="btn btn-dark" onclick="document.querySelector('.CC-2').scrollLeft -= 300;">←</button>
        </div>
        <div class="d-flex card-container CC-2  col-10" style="height: 38vh; width:100% ;justify-content: left;">
            <div v-for="album in albums" :key="album.album_id" class="card mb-3">
                    <div class="card-header">
                        <h3 class="card-title"> {{ album.title }} </h3>
                    </div>
                    <div class="star-container-deactive card-body" style="padding-bottom:0 ;">
                        <span style="padding: 0%;margin: 0%;padding-bottom: 2%;">             
                            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-star" viewBox="0 0 16 16">
                                <path d="M2.866 14.85c-.078.444.36.791.746.593l4.39-2.256 4.389 2.256c.386.198.824-.149.746-.592l-.83-4.73 3.522-3.356c.33-.314.16-.888-.282-.95l-4.898-.696L8.465.792a.513.513 0 0 0-.927 0L5.354 5.12l-4.898.696c-.441.062-.612.636-.283.95l3.523 3.356-.83 4.73zm4.905-2.767-3.686 1.894.694-3.957a.565.565 0 0 0-.163-.505L1.71 6.745l4.052-.576a.525.525 0 0 0 .393-.288L8 2.223l1.847 3.658a.525.525 0 0 0 .393.288l4.052.575-2.906 2.77a.565.565 0 0 0-.163.506l.694 3.957-3.686-1.894a.503.503 0 0 0-.461 0z"></path>
                            </svg>    
                        </span>                   
                        <span v-if="album.rating==null" style="font-size: small;">
                                N/A
                        </span>
                        <span v-else style="font-size: small;">
                                {{ album.rating }}/5
                        </span>
                    </div>
                    <div class="card-body">
                        <h5 class="card-text">by <span style="font-style: italic;">{{ getArtistName(album.artist_id) }}</span></h5>
                        <h5 class="card-text"><span style="font-style: italic;">{{ album.genre }}</span></h5>
                    </div>
                    <div class="card-footer">
                        <button class="btn btn-outline-success" @click="viewAlbum(album.album_id)">View</button>
                        <button class="btn btn-outline-danger" @click="flagAlbum(album.album_id)">Flag</button>
                    </div>
            </div>
        </div>
        <div class="arrow-buttons">
            <button class="btn btn-dark" onclick="document.querySelector('.CC-2').scrollLeft += 300;">→</button>
        </div>
    </div>
    <div v-else class="container">
        No albums found.
    </div>
</template>

<script>
import axios from 'axios';
const API_BASE_URL = 'http://127.0.0.1:5000/api';

export default {
    data() {
        return {
            albums: null,
            flashMessage: null,
            path: '',
            artistName: '',
            song_ids: ''
        };
    },
    created() {
        this.authToken = localStorage.getItem("authToken");
        if (this.authToken) {
            this.getAlbums();
        }
        else {
            this.$router.push('/login')
        }
    },
    methods: {
        getAlbums() {
            axios.get(`${API_BASE_URL}/albums`,{
                headers: {
                    Authorization: `${this.authToken}`
                }
            })
            .then(response => {
                this.albums = response.data;
            })
            .catch(error => {
                console.error("Error fetching albums: ", error)
            });
        },
        flagAlbum(album_id) {
            console.log(`Flagging album ${album_id}`)
            axios.put(`${API_BASE_URL}/albums/${album_id}`,{
                headers: {
                    Authorization: `${this.authToken}`
                },
                params: {
                    "flag": "true"
                }
            })
            .then(response=>{
                console.log(response.data.message);
                axios.get(`${API_BASE_URL}/albums/${album_id}`)
                .then(response=>{
                    this.song_ids = response.data.song_ids;
                    this.song_ids.forEach(element => {
                        this.flagSong(element)
                    });
                })
            })
            .catch(error=>{
                console.error(error);
            })
        },
        getArtistName(artist_id){
            axios.get(`${API_BASE_URL}/artists?artistId=${artist_id}`)
                .then(response=>{
                    this.artistName = response.data.name;
                })
            return this.artistName
        },
        viewAlbum(album_id){
            this.$router.push(`/albums/${album_id}`)
        },
        flagSong(song_id) {
            console.log(`Flagging song ${song_id}`)
            axios.put(`${API_BASE_URL}/songs/${song_id}`,{
                headers: {
                    Authorization: `${this.authToken}`
                },
                params: {
                    "flag": "true"
                }
            })
            .then(response=>{
                console.log(response.data.message);
            })
            .catch(error=>{
                console.error(error);
            })
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
    h5{
        font-size: large;;
    }
    .star-container-deactive {
    display: inline-block;
    position: relative;
    }
    .star-container-deactive .bi-star {
    fill: gold;
    }
</style>