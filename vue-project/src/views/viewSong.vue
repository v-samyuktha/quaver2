<script setup>
import loginNav from '../components/loginNav.vue'
</script>

<template>
    <loginNav />
    <div v-if="song" class="heading">
        <h3 class="green">{{ song.title }}
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

        </h3>
        <h4>by {{ song.artist }}</h4>
        <h4>Genre: {{ song.genre }}</h4>
    </div>
    <div class="container">
        <audio id="audio" controls>
            <source id="audioSource" src="" type="audio/mpeg">
                Your browser does not support the audio tag.
        </source>
        </audio>
    </div>
    <div class="container embed-responsive embed-responsive-16by9">
        <iframe id="lyricsFrame" class="embed-responsive-item" src="" allowfullscreen style="height: 30vh; width: 60vh"></iframe>
    </div>
    <div class="container back-btn">
        <button class="button btn btn-outline-dark" id="back" onclick="history.go(-1)">Back</button>
    </div>
</template>

<script>
import axios from 'axios';
const API_BASE_URL = 'http://127.0.0.1:5000/api';

export default {
    data() {
        return {
            songId: null,
            song: null,
        };
    },
    created() {
        this.authToken = localStorage.getItem("authToken");
        if (this.authToken) {
            this.getSong();
        }
        else {
            this.$router.push('/login')
        }
    },
    methods: {
        getSong() {
            this.songId=this.$route.params.song_id;
            axios.get(`${API_BASE_URL}/songs/${this.songId}`)
            .then(response=>{
                this.song=response.data;
                this.playSong();
                this.setLyrics();
            })
        },
        playSong() {
        var audio = document.getElementById('audio');
        var source = document.getElementById('audioSource');

        source.src = `/src/assets/audio/${this.songId}.mp3`;

        audio.load();
        },
        setLyrics() {
            var lyricsFrame = document.getElementById('lyricsFrame');
            lyricsFrame.src = `/src/assets/lyrics/${this.songId}.txt`;
        },
        rateSong() {
            const song_id = this.songId;
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
        },
        
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
    .back-btn{
        position:absolute;
        bottom: 10vh;
        left:10vw;
    }
</style>