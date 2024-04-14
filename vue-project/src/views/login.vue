<script setup>
import { fn } from 'jquery';
import loginNav from '../components/loginNav.vue'
import axios from 'axios';
</script>

<template>
    <loginNav/>
    <div class="login login-card align-center container">
        <h2 class="green">Welcome to Quaver!</h2>
        <br>
        <form @submit.prevent="loginUser">
        <div class="row">
            <label class="col-4">Username: </label>
            <input class="col-6" type="username" v-model="username" required />
        </div>
        <div class="row">
            <label class="col-4">Password: </label>
            <input class="col-6" type="password" v-model="password" required/>
        </div>
        <br>
        <div class="row">
            <button class="button btn btn-outline-success" type="submit">Login</button>
        </div>
        </form>
        <p v-if="message" style="color: rgb(189, 0, 0)">{{ message }}</p>
        <br>
        <p>
            New to Quaver?
            <a class="sign-in-link"><RouterLink to="/register">Sign-up</RouterLink></a>
        </p>
    </div>
</template>

<script>
const API_BASE_URL = 'http://127.0.0.1:5000/api';
const BASE_URL = 'http://127.0.0.1:5000';

export default {
    data(){
        return {
            username: '',
            password: '',
            message: ''
        };
    },

    methods: {
        loginUser(){
            axios.post(`${API_BASE_URL}/login`, {
                username: this.username,
                password: this.password,
            })
            .then(response => {
                this.message = response.data.message;
                this.username = '';
                this.password = '';

                localStorage.setItem('username', response.data.username);
                localStorage.setItem('userRole', response.data.roles[0]);
                localStorage.setItem('graphsSet', false)
                console.log(response.data.roles)
                if(response.data.roles.length>1){
                        localStorage.setItem('creatorRole', response.data.roles[1]);
                        axios.get(`${API_BASE_URL}/artists?username=${localStorage.getItem("username")}`)
                    .then(response=>{
                        localStorage.setItem("artistName", response.data.name);
                        localStorage.setItem("artistId", response.data.artist_id);
                        console.log(`Artist login: ${response.data.name}`);
                    });   
                }
                localStorage.setItem('authToken', response.data.auth_token);
                localStorage.setItem('userId', response.data.id);

                this.$router.push(response.data.roles.includes('admin') ? '/dashboard' : '/home')
            })
            .catch(error => {
                if(error.response && error.response.data.message){
                    this.message = error.response.data.message;
                }
                else{
                    this.message = error.message;
                }
            });
        },
    },
};
</script>

<style>
    .align-center{
        display: grid;
        width: auto;
        padding: 10%;
        place-items: center;
        justify-content: center;
    }

    #form{
        display:grid;
        width:auto;
    }

    .login-card{
        width:max-content;
    }

    .row{
        width:inherit;
        justify-content: center;
        margin-bottom:5%;
    }

    .button{
        width:auto;
        align-self: center;
    }

    .sign-in-link {
	position: relative;
	transition: color .3s ease-in-out;
	
	&::before {
		content: '';
		position: absolute;
		top: 100%;
		width: 65px;
		height: 3px;
		background-color: hsla(160, 100%, 37%, 1);
		transform: scaleX(0);
		transition: transform .3s ease-in-out;
	}
	
	&:hover {
		color: hsla(160, 100%, 37%, 1);
	}
	
	&:hover::before {
		transform: scaleX(1);
	}	
}
.login-card{
    padding-top: 5%;
    flex-direction: column;
}
</style>