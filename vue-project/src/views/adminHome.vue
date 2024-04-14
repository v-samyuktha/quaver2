<script setup>
import adminNav from "../components/adminNav.vue"
</script>

<template>
    <adminNav />
    <div class="container green" style="padding: 1%;">
        <strong>App Overview</strong>
    </div>
    <div class="container">
        <div class="row justify-content-md-center gap-4">
          <div class="stat-box col-lg-4">
            <p>Total Accounts:</p>
            <h3 id="circle">{{regulars.length}}</h3>
          </div>
          <div class="stat-box col-lg-4">
            <p>Creators:</p>
            <h3 id="circle">{{creators.length}}</h3>
          </div>
        </div>
        <br>
        <div class="row justify-content-md-center gap-4">
            <div class="stat-box col-lg-4">
              <p>Tracks:</p>
              <h3 id="circle">{{stats.total_songs}}</h3>
            </div>
            <div class="stat-box col-lg-4">
              <p>Albums:</p>
              <h3 id="circle">{{stats.total_albums}}</h3>
            </div>
          </div>
    </div>
    <br>
    <div class="container" style="margin-bottom: 3%;">
        <div class="row">
            <div class="col green">
                <p style="font-size: x-large; font-weight: bolder;">Accounts Created</p>
                <img class="graph-img" src="@/assets/joining_dates.png" alt="Graph showing timeline of #accounts">
            </div>
            <div class="col green">
                <p style="font-size: x-large; font-weight: bolder;">Songs Released</p>
                <img class="graph-img" src="@/assets/song_releases.png" alt="Graph showing timeline of #songs">
            </div>
        </div>
    </div>
</template>
<script>
import axios from 'axios';
const API_BASE_URL = 'http://127.0.0.1:5000/api';
export default {
    data(){
        return {
        regulars: [],
        creators: [],
        stats: {},
        graphsSet: false
        }
    },
    created() {
        this.authToken = localStorage.getItem("authToken");
        if (this.authToken) {
            this.getStats();
            //this.setGraphs();
            console.log(localStorage.getItem("graphsSet")=="true")
            if (localStorage.getItem("graphsSet")!="true" && this.$route.name === 'adminHome') {
                this.setGraphs();
                this.graphsSet=true;
                localStorage.setItem("graphsSet", true)
        }
        }
        else {
            this.$router.push('/login')
        }
    },
    methods:{
        getStats(){
            axios.get(`${API_BASE_URL}/users?role=creator`)
            .then(response=>{
                this.creators = response.data;
                console.log(`${this.creators.length} creators found`);
            })
            .catch(error=>console.error(error))

            axios.get(`${API_BASE_URL}/users?role=user`)
            .then(response=>{
                this.regulars = response.data;
                console.log(`${this.regulars.length} users found`);
            })
            .catch(error=>console.error(error))

            axios.get(`${API_BASE_URL}/songs`)
            .then(response=>{
                this.stats["total_songs"]=response.data.length;
            })
            axios.get(`${API_BASE_URL}/albums`)
            .then(response=>{
                this.stats["total_albums"]=response.data.length;
            })
        },
        setGraphs(){
            axios.get(`${API_BASE_URL}/graphs`)
            .then(response=>{
                console.log(response.data.message);
            })
            .catch(error=>{
                console.error(error);
            })
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
.graph-img{
    width:450px;
    height:350px
}
</style>