<template>
    <div class="search-form">
        <form @submit.prevent="search">
                    <div class="form-group row" style="margin-bottom: 0px;">
                        <div class="col col-5 search-col">
                        <input class="form-control search-bar" type="search" id="search_text" placeholder="Search" aria-label="Search">
                        </div>
                        <div class="col col-1 search-icon-col">
                        <button class="btn btn-outline-dark" type="submit">
                            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-search" viewBox="0 0 16 16">
  <path d="M11.742 10.344a6.5 6.5 0 1 0-1.397 1.398h-.001q.044.06.098.115l3.85 3.85a1 1 0 0 0 1.415-1.414l-3.85-3.85a1 1 0 0 0-.115-.1zM12 6.5a5.5 5.5 0 1 1-11 0 5.5 5.5 0 0 1 11 0"/>
</svg>
                        </button>
                        </div>
                    </div>
        </form>
    </div>
</template>
<style>
.search-bar{
   border-color: rgb(66, 125, 60);
}
.search-col{
    padding-inline: 1%;
}
.search-icon-col{
    padding-inline: 1%;
}
.search-form{
    display: flex;
    position: relative;
    top: 0vh;
    justify-content: center;
}

</style>
<script>
export default {
    data(){
        return {
            search_phrase: null,
            authToken: ''
        };
    },
    created(){
        this.authToken = localStorage.getItem("authToken");
        if (this.authToken) {
            ;
        }
        else {
            this.$router.push('/login')
        }
    },
    methods: {
        search(){
            let temp = document.getElementById("search_text")
            if(temp.value && temp.value.trim()!=''){
                this.search_phrase = temp.value
                console.log(this.search_phrase)
                this.$router.push(`/search?key=${this.search_phrase}`)
                .then(() => { this.$router.go(0) })
            }
            else{
                console.log("Empty search")
            }
        }
    },
};
</script>