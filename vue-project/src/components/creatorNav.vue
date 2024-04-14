<template>
    <nav class="navbar navbar-expand-md navbar-light">
        <div class="mx-left order-0">
            <ul class="navbar-nav mr-auto">
                <li class="nav-item">
                    <a>
                        <img src="@/assets/quaver_logo.png" height="40" alt="Quaver" style="padding-left: 10%;">
                    </a>
                </li>
            </ul>
        </div>
        <div class="mx-auto order-1 abs-center-x">
            <ul class="navbar-nav mr-auto">
            <li class="nav-item"><a class="nav-link"><RouterLink to="/creator_home">Uploads</RouterLink></a></li>
            <li class="nav-item"><a class="nav-link"><RouterLink to="/creator_profile">Profile</RouterLink></a></li>
            </ul>
        </div>
        <div class="mx-end order-2 abs-end-x">
            <ul class="navbar-nav mr-auto">
            <li class="nav-item"><button class="btn red" @click=logoutUser()>Logout</button></li>
            </ul>
        </div>
    </nav>
</template>
<style>
.nav-link {
	position: relative;
	transition: color .3s ease-in-out;
	padding:2px;
	&::before {
		content: '';
		position: absolute;
		top: 100%;
		width: 55px;
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

.abs-center-x {
    position: absolute;
    left: 50%;
    transform: translateX(-50%);
}
.abs-end-x {
    position: absolute;
    right: 2%;
}

a {
    color: hsla(160, 100%, 37%, 1);
    text-decoration: none;
}

.navbar {
    background-color: rgb(122 161 144 / 24%);
    max-height: 10vh;
}

.red {
    color:rgba(244, 94, 94, 0.763);
	position: relative;
	transition: color .3s ease-in-out;
	padding:2px;
	&:hover {
		color: red;
        background-color:lightpink;
	}
	
	
}
</style>
<script>
    import axios from 'axios';
    const API_BASE_URL = 'http://127.0.0.1:5000/api';
    export default {
    methods: {
        logoutUser() {
                axios.post(`${API_BASE_URL}/logout`, {
                    uid: localStorage.getItem('userId'),
                })
                    .then(response => {
                        localStorage.removeItem('userRole');
                        localStorage.removeItem('authToken');
                        localStorage.removeItem('userId');
                        localStorage.removeItem('username');
                        localStorage.removeItem('artistName');
                        localStorage.removeItem('artistId');
                        localStorage.removeItem('creatorRole');
                        localStorage.removeItem('graphsSet');
                        this.$router.push('/login');
                    })
                    .catch(error => {
                        console.error('Logout error:', error);
                    });
            }
        
    }
}
</script>