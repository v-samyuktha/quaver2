<script setup>
import userNav from '../components/userNav.vue'
let username = localStorage.getItem("username");
</script>

<template>
    <userNav />
    <div class="container">
        <h3 class="green">{{ username }}'s profile</h3>
    </div>
    <div class="container">
        <div class="col">
            <div class="row">
                Joined on: {{ joined_on }}
            </div>
            <div class="row">
                Playlists created:  {{ no_of_playlists }}
            </div>
        </div>
    </div>
    <div class="container" v-if="notCreator">
        <RouterLink to="/register_creator" class="btn btn-outline-success">Register as Creator</RouterLink>
    </div>
    <div class="container" v-else>
        <RouterLink to="/creator_home" class="btn btn-success">Creator Dashboard</RouterLink>
    </div>
</template>

<style>
    .container{
        display:flex;
        margin-top: 2%;
        width: 80%;
        justify-content: center;
    }
</style>
<script>
import axios from 'axios';
const API_BASE_URL = 'http://127.0.0.1:5000/api';

export default {
    data() {
        return {
            joined_on: null,
            no_of_playlists: null,
            notCreator: true
        };
    },
    created() {
        this.authToken = localStorage.getItem("authToken");
        if (this.authToken) {
            this.setStats();
            this.checkCreator();
        }
        else {
            this.$router.push('/login')
        }
    },
    methods: {
        setStats() {
            axios.get(`${API_BASE_URL}/users/${localStorage.getItem('userId')}`)
            .then(response=>this.joined_on=response.data.joined_on)
            .catch(error=>console.error(error))

            axios.get(`${API_BASE_URL}/playlists?userId=${localStorage.getItem('userId')}`)
            .then(response=>this.no_of_playlists=response.data.length)
            .catch(error=>console.error(error))
        },
        checkCreator() {
            if (localStorage.getItem('creatorRole')){
                this.notCreator=false;
            }
        }
    }
}
</script>