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
		width: 50px;
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
a {
    color: hsla(160, 100%, 37%, 1);
    text-decoration: none;
}

.navbar {
    background-color: rgb(122 161 144 / 24%);
    max-height: 10vh;
}
</style>