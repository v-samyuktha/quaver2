<script setup>
import loginNav from '@/components/loginNav.vue';
</script>
<template>
    <loginNav />
    <div class="login login-card align-center container">
        <h2 class="green">Register to Quaver</h2>
        <br>
        <form @submit.prevent="registerUser">
        <div class="form-group row">
            <label class="col" style="align-content: center;">Pick a username: </label>
            <input type="text" id="username" class="col form-control" placeholder="Enter username" required />
        </div>
        <div class="form-group row">
            <label class="col" style="align-content: center;">Set a password: </label>
            <input type="password" id="password" class="col form-control" placeholder="Enter password" required />
        </div>
        <div class="form-group row">
            <label class="col" style="align-content: center;">Re-type password: </label>
            <input type="password" id="password2" class="col form-control" placeholder="Re-enter password" required />
        </div>
        <br>
        <div class="row">
            <button class="button btn btn-outline-success" type="submit">Confirm</button>
            <button class="button btn btn-outline-danger" id="cancel" onclick="history.go(-1)">Cancel</button>
        </div>
        </form>
        <p v-if="message" style="color: rgb(189, 0, 0)">{{ message }}</p>

    </div>
</template>

<script>
import axios from 'axios';

const API_BASE_URL = 'http://127.0.0.1:5000/api';
const BASE_URL = 'http://127.0.0.1:5000';

export default {
    data(){
        return {
            username:'',
            password: '',
            password2: '',
            message: ''
        };
    },

    methods: {
        registerUser(){
            this.username = document.getElementById("username").value
            this.password = document.getElementById("password").value
            this.password2 = document.getElementById("password2").value

            if (this.password==this.password2){
                axios.post(`${API_BASE_URL}/register`, {
                    username: this.username,
                    password: this.password ,
                })
                .then(response => {
                    console.log(response.data.message);
                    this.$router.push('/login');
                })
                .catch(error => {
                    if(error.response && error.response.data.message){
                        this.message = error.response.data.message;
                    }
                    else{
                        this.message = error.message;
                    }
                });
            }
            else {
                this.message = "Passwords do not match!";
            }
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