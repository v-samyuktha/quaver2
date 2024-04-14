<script setup>
import loginNav from '../components/loginNav.vue'
</script>

<template>
    <loginNav />
    <div v-if="songs" class="heading">
        <h3 class="green">{{ title }}
            <span class="star-container-deactive" id="test">
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-star" viewBox="0 0 16 16">
                    <path d="M2.866 14.85c-.078.444.36.791.746.593l4.39-2.256 4.389 2.256c.386.198.824-.149.746-.592l-.83-4.73 3.522-3.356c.33-.314.16-.888-.282-.95l-4.898-.696L8.465.792a.513.513 0 0 0-.927 0L5.354 5.12l-4.898.696c-.441.062-.612.636-.283.95l3.523 3.356-.83 4.73zm4.905-2.767-3.686 1.894.694-3.957a.565.565 0 0 0-.163-.505L1.71 6.745l4.052-.576a.525.525 0 0 0 .393-.288L8 2.223l1.847 3.658a.525.525 0 0 0 .393.288l4.052.575-2.906 2.77a.565.565 0 0 0-.163.506l.694 3.957-3.686-1.894a.503.503 0 0 0-.461 0z"></path>
                </svg>                   
            </span>
            <span v-if="rating==null" style="font-size: small; color: black;">
                    N/A
            </span>
            <span v-else style="font-size: small;">
                    {{ rating }}/5
            </span> 
        </h3>
        <h4>by {{ artistName }}</h4>
        <h5 v-if="desc"> "{{ desc }}"</h5>
    </div>
    <div v-if="songs && songs.length>0" class="container d-flex" style="justify-content: center; margin-bottom: 2%;">
        <div class="arrow-buttons">
            <button class="btn btn-dark" onclick="document.querySelector('.CC-1').scrollLeft -= 300;">←</button>
        </div>
        <div class="d-flex card-container CC-1  col-10" style="height: 38vh; width:100% ;justify-content: left;">
            <div v-for="song in songs" :key="song.song_id" class="card mb-3">
                    <div class="card-header">
                        <h3 class="card-title"> {{ song.title }} </h3>
                    </div>
                    <div class="card-body">
                            <h4 class="card-title">
                                <div class="star-container-deactive" id="test">
                                        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-star" viewBox="0 0 16 16">
                                            <path d="M2.866 14.85c-.078.444.36.791.746.593l4.39-2.256 4.389 2.256c.386.198.824-.149.746-.592l-.83-4.73 3.522-3.356c.33-.314.16-.888-.282-.95l-4.898-.696L8.465.792a.513.513 0 0 0-.927 0L5.354 5.12l-4.898.696c-.441.062-.612.636-.283.95l3.523 3.356-.83 4.73zm4.905-2.767-3.686 1.894.694-3.957a.565.565 0 0 0-.163-.505L1.71 6.745l4.052-.576a.525.525 0 0 0 .393-.288L8 2.223l1.847 3.658a.525.525 0 0 0 .393.288l4.052.575-2.906 2.77a.565.565 0 0 0-.163.506l.694 3.957-3.686-1.894a.503.503 0 0 0-.461 0z"></path>
                                        </svg>                   
                                </div> 
                                
                                <span v-if="song.rating==null" style="font-size: small;">
                                        N/A
                                </span>
                                <span v-else style="font-size: small;">
                                        {{ song.rating }}/5
                                </span>
                            </h4>
                            <h5 class="card-text">{{ song.genre }}</h5>
                        </div>
                    <div class="card-footer">
                        <button class="btn btn-outline-success" @click="playSong(song.song_id)">Listen</button>
                    </div>
            </div>
        </div>
        <div class="arrow-buttons">
            <button class="btn btn-dark" onclick="document.querySelector('.CC-1').scrollLeft += 300;">→</button>
        </div>
    </div>
    <div v-else class="container">
        No songs found.
    </div>
    <br>
    <div class="container">
        <button class="button btn btn-outline-dark back-button" id="back" onclick="history.go(-1)">Back</button>
    </div>
</template>

<style>
    .container{
        display:flex;
        width: 80%;
        justify-content: center;
    }
    .heading {
    display: flex;
    flex-direction: column;
    align-items: center;
    margin: 2%;
    padding: 1%;
}
</style>

<script>
import axios from 'axios';
const API_BASE_URL = 'http://127.0.0.1:5000/api';

export default {
    data() {
        return {
            songs: [],
            title: '',
            flashMessage: null,
            path: '',
            desc: null,
            artistName: '',
            artistId: '',
            rating: null
        };
    },
    created() {
        this.authToken = localStorage.getItem("authToken");
        if (this.authToken) {
            this.getSongs();
        }
        else {
            this.$router.push('/login')
        }
    },
    methods: {
        getSongs() {
            axios.get(`${API_BASE_URL}/albums/${this.$route.params.album_id}`,{
                headers: {
                    Authorization: `${this.authToken}`
                },
            })
            .then(response => {
                this.title=response.data.title;
                this.artistId=response.data.artist_id;
                this.rating=response.data.rating;
                if (response.data.description!='')
                    this.desc=response.data.description;
                console.log("song ids: " + response.data.song_ids)
                let song_ids = response.data.song_ids;
                song_ids.forEach(id => {
                    axios.get(`${API_BASE_URL}/songs/${id}`, {
                        headers: {
                    Authorization: `${this.authToken}`
                    },
                    })
                    .then(response => this.songs.push(response.data))
                });
                
                axios.get(`${API_BASE_URL}/artists?artistId=${this.artistId}`)
                .then(response=>{
                    this.artistName = response.data.name;
                })
            })
            .catch(error => {
                console.error("Error fetching playlists: ", error)
            });
        },
        playSong(song_id){
            this.$router.push(`/songs/${song_id}`)
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
        background-color: #30a36d96;
    }
    h5{
        font-size: x-large;
        font-style: italic ;
    }
        .star-container-deactive {
    display: inline-block;
    position: relative;
    }
    .star-container-deactive .bi-star {
    fill: gold;
    }
    .back-button{
        display: flex;
    }
</style>