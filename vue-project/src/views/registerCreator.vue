<script setup>
import { fn } from 'jquery';
import userNav from '../components/userNav.vue'
import axios from 'axios';
</script>

<template>
    <userNav/>
    <div class="login login-card align-center container">
        <h2 class="green">Registering as Creator</h2>
        <br>
        <form @submit.prevent="registerCreator">
        <div class="form-group row">
            <label class="col" style="align-content: center;">Artist name: </label>
            <input id="name" class="col form-control" required />
        </div>
        <br>
        <div class="row">
            <button class="button btn btn-outline-success" type="submit">Confirm</button>
            <button class="button btn btn-outline-danger" id="cancel" onclick="history.go(-1)">Cancel</button>
        </div>
        </form>

    </div>
</template>

<script>
const API_BASE_URL = 'http://127.0.0.1:5000/api';
const BASE_URL = 'http://127.0.0.1:5000';

export default {
    data(){
        return {
            username:'',
            name: '',
            id: '',
            authToken: ''
        };
    },
    created() {
        this.authToken = localStorage.getItem('authToken');
        if (this.authToken) {
            ;
        } else {
            this.$router.push('/login');
        }
    },
    methods: {
        registerCreator(){
            this.name = document.getElementById("name").value
            this.username = localStorage.getItem("username")
            this.id = localStorage.getItem("userId")
            axios.post(`${API_BASE_URL}/artists`, {
                name: this.name,
                username: this.username ,
                id: this.id
            }, {
                headers: {
                    Authorization: `${this.authToken}`
                }
            })
            .then(response => {
                console.log(response.data.message);
                this.$router.push('/profile');
            })
            .catch(error => {
                console.error(error);
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