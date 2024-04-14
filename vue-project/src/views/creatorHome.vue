<script setup>
import creatorSongs from "../components/creatorSongs.vue"
import creatorNav from "../components/creatorNav.vue"
import creatorAlbums from "../components/creatorAlbums.vue"
</script>

<template>
    <creatorNav />
    <creatorSongs />
    <creatorAlbums />
</template>
<script>

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