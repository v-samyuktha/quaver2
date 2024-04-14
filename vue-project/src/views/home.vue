<script setup>
import userNav from '../components/userNav.vue'
import userPlaylists from '../components/userPlaylists.vue'
import userSongs from '../components/userSongs.vue'
import userMusic from '../components/userMusic.vue'
import userSearch from '../components/userSearch.vue'
import userAlbums from '../components/userAlbums.vue'
let uname = localStorage.getItem("username");
</script>

<template>
    <userNav />
    <div class="heading" style="margin-bottom: 0px;">
        <h3 class="green">Welcome, {{uname}}!</h3>
    </div>
    <userSearch />
    <userSongs />
    <userAlbums />
    <userPlaylists />
    <!--userMusic /-->
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
    margin:0%;
    padding: 0%;
}
</style>