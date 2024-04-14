<script setup>
import userNav from '../components/userNav.vue'
let userId = localStorage.getItem("userId");
</script>

<template>
    <userNav />
    <div class="heading">
        <h3 class="green">New Playlist</h3>
    </div>
    <div class="container col-md-4 col-md-offset-4" style="margin-top: 2%;">
        <form @submit.prevent="createPlaylist">
            <div class="form-group">
                <label aria-required="true">Title : </label>   
                <input type="text" class="form-control" placeholder="Enter Title" id="title" name="title" required>
            </div>
            <br>
            <div class="form-group">
                <label>Description : </label>   
                <input type="text" class="form-control" placeholder="(Optional)" id="description" name="description">
            </div>
            <br>
            <label class="form-label" for="form1">Add a song:</label>
            <div class="input-group form-control">
                <select class="form-select" placeholder="Select a song" id="selected_song">
                    <option v-for="song in song_list" :value="song.song_id">{{ song.title }}</option>
                </select>
                <button type="button" class="btn btn-outline-success rounded-circle btn-sm" style="margin: 2%;" @click="addSong()">+</button>
            </div>
            Selected songs:<br>
                <div v-if="added_song_ids.length!=0">
                <span id="song-selected" v-for="title in added_song_titles">
                    {{ title }} <br>
                </span>
                </div>
                <p v-else style="color: red;">None</p>
        <br>
        <div class="row">
            <button class="button btn btn-outline-success" id="create" onclick="createPlaylist()">Create!</button>
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
</style>
<script>
import axios from 'axios';

const API_BASE_URL = 'http://localhost:5000/api';

export default {
    data() {
        return {
            added_song_ids: [],
            added_song_titles: [],
            song_list: null,
            flashMessage: '',
            path: '',
            selected_id: null
        };
    },
    created() {
        this.authToken = localStorage.getItem('authToken');
        if (this.authToken) {
            this.getSongs();
        } else {
            this.$router.push('/login');
        }
    },
    methods: {
        getSongs() {
            axios.get(`${API_BASE_URL}/songs`,{
                headers: {
                    Authorization: `${this.authToken}`
                }
            })
            .then(response => {
                console.log(response.data)
                this.song_list = response.data;
            })
            .catch(error => {
                console.error("Error fetching songs: ", error)
            })},
        addSong(){
            this.selected_id = document.getElementById("selected_song").value;
            console.log(this.selected_id + " selected");
            this.added_song_ids.push(this.selected_id);
            this.added_song_titles.push(document.getElementById("selected_song").options[document.getElementById("selected_song").selectedIndex].text)
            let temp_list = []
            this.song_list.forEach(song => {
                if (song.song_id!=this.selected_id){
                    temp_list.push(song)
                }
                else{
                    console.log(`Removed ${song.title} from options`)
                }
            });
            this.song_list=temp_list;
        },
        createPlaylist(){
            const options = {
                method: "POST",
                url: `${API_BASE_URL}/playlists`,
                headers: {
                    'content-type': 'application/json',
                    'Authorization': `${this.authToken}`
                },
                data: 
                    {
                        "title": document.getElementById("title").value,
                        "desc": document.getElementById("description").value,
                        "song_ids": this.added_song_ids,
                        "userId": localStorage.getItem("userId")
                    }
                
            }

            axios.request(options)
            .then(response => {
                console.log(response.data)
                this.goToPlaylists()
            })
            .catch(error => {
                console.error(error)
            })  
        
        },
        goToPlaylists(){
            this.$router.push("/playlists")
        }
    },
};
</script>