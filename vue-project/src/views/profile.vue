<script setup>
import userNav from '../components/userNav.vue'
let username = localStorage.getItem("username");
</script>

<template>
    <userNav />
    <div class="container">
        <h3 class="green">{{ username }}'s profile</h3>
    </div>
    <div class="grid stat-grid">
        <hr>
        <div class="row stat-head-row">
            <div class="col stat-heading">
                Joined on: 
            </div>
            <div class="col stat-heading">
                Playlists created:  
            </div>
        </div>
        <div class="row stat-head-row">
            <div class="col stat-value1">
                {{ joined_on }}
            </div>
            <div class="col stat-value1">
                {{ no_of_playlists }}
            </div>
        </div>
        <hr>
    </div>
    <div class="container" v-if="notCreator">
        <RouterLink to="/register_creator" class="btn btn-outline-success">Register as Creator</RouterLink>
    </div>
    <div class="container" v-else>
        <RouterLink to="/creator_home" class="btn btn-success">Creator Dashboard</RouterLink>
    </div>
</template>

<script>
import axios from 'axios';
const API_BASE_URL = 'http://127.0.0.1:5000/api';

export default {
    data() {
        return {
            joined_on: null,
            no_of_playlists: null,
            notCreator: true,
            authToken: ''
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
            axios.get(`${API_BASE_URL}/users/${localStorage.getItem('userId')}`, {
                headers: {
                    Authorization: `${this.authToken}`
                }
            })
            .then(response=>this.joined_on=response.data.joined_on)
            .catch(error=>console.error(error))

            axios.get(`${API_BASE_URL}/playlists?userId=${localStorage.getItem('userId')}`,{
                headers: {
                    Authorization: `${this.authToken}`
                }
            })
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

<style>
    .container{
        display:flex;
        margin-top: 2%;
        width: 80%;
        justify-content: center;
    }
    .stat-heading{
        font-size: large;
        font-weight: 700;
    }
    .stat-head-row{
        margin-bottom: 0% !important;
    }
    .stat-grid {
        background-color: rgba(148, 207, 215, 0.192);
        max-width: 60%;
        position: relative;
        left: 20%;
        display: grid;
        justify-items: stretch;
        justify-content: center;
        place-content: normal;
        margin-top: 2%;
    }
    hr{
        border-width: 3px;
        width: inherit;
        margin: 0%;
    }
    .stat-grid>.row{
        height: 50px;
    }
    .stat-value1{
        color: hsla(160, 100%, 37%, 1);
        font-size: 30px;
    }
</style>