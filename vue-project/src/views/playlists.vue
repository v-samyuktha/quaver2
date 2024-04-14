<script setup>
import userNav from '../components/userNav.vue'
import userPlaylists from '../components/userPlaylists.vue'
let userId = localStorage.getItem("userId");
</script>

<template>
    <userNav />
    <userPlaylists />
</template>

<style>
    .container{
        display:flex;
        margin-top: 5%;
        width: 80%;
        justify-content: center;
    }
</style>