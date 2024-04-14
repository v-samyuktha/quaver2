<script setup>
import adminNav from "../components/adminNav.vue"
import adminSongs from "../components/adminSongs.vue"
import adminAlbums from "../components/adminAlbums.vue"
</script>

<template>
    <adminNav />
    <adminSongs />
    <adminAlbums />
</template>
<script>
import axios from 'axios';
const API_BASE_URL = 'http://127.0.0.1:5000/api';
export default {

    created() {
        this.authToken = localStorage.getItem("authToken");
        if (this.authToken) {
            ;
        }
        else {
            this.$router.push('/login')
        }
    },
}
</script>
<style>
.row-head {
    display: flex;
    width: 50vw;
    padding: 0%;
    margin: 0%;
    place-items: center;
    justify-content: center;
}
.col-4{
    padding-inline: 5%;
    margin-inline: 2%;
}
.stat-box {
  border-radius: 25px;
  background: #cfe8d6;
  padding: 15px;
  width: 200px;
  height: 150px;
  display: inline-flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}

.stat-box > p{
    font-size: x-large;
    font-weight: 400;
    color: #000000;
}

.stat-box > h3{
    font-size: xx-large;
    font-weight: 500;
    color: #000000;
}
</style>