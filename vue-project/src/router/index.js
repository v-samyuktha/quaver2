import { createRouter, createWebHistory } from 'vue-router'
import login from '../views/login.vue'
import home from '../views/home.vue'
import playlists from '../views/playlists.vue'
import profile from '../views/profile.vue'
import viewPlaylist from '../views/viewPlaylist.vue'
import newPlaylist from '../views/newPlaylist.vue'
import registerCreator from '../views/registerCreator.vue'
import creatorHome from '../views/creatorHome.vue'
import search from '../views/search.vue'
import newSong from '../views/newSong.vue'
import creatorProfile from '../views/creatorProfile.vue'
import adminHome from '../views/adminHome.vue'
import adminUploads from '../views/adminUploads.vue'
import adminFlagged from '../views/adminFlagged.vue'
import register from '../views/register.vue'
import newAlbum from '../views/newAlbum.vue'
import viewAlbum from '../views/viewAlbum.vue'
import viewSong from '../views/viewSong.vue'
import addToPlaylist from '../views/addToPlaylist.vue'
import editSong from '../views/editSong.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      redirect: {path: '/login'}
    },
    {
      path: '/login',
      name: 'login',
      component: login
    },
    {
      path: '/home',
      name: 'home',
      component: home
    },
    {
      path: '/playlists',
      name: 'playlists',
      component: playlists
    },
    {
      path: '/profile',
      name: 'profile',
      component: profile
    },
    {
      path: '/playlists/:playlist_id',
      name: 'viewPlaylist',
      component: viewPlaylist
    },
    {
      path: '/new_playlist',
      name: 'newPlaylist',
      component: newPlaylist
    },
    {
      path: '/register_creator',
      name: 'registerCreator',
      component: registerCreator
    },
    {
      path: '/creator_home',
      name: 'creatorHome',
      component: creatorHome
    },
    {
      path: '/search',
      name: 'search',
      component: search
    },
    {
      path: '/new_song',
      name: 'newSong',
      component: newSong
    },
    {
      path: '/creator_profile',
      name: 'creatorProfile',
      component: creatorProfile
    },
    {
      path: '/dashboard',
      name: 'adminHome',
      component: adminHome
    },
    {
      path: '/uploads',
      name: 'adminUploads',
      component: adminUploads
    },
    {
      path: '/flagged',
      name: 'adminFlagged',
      component: adminFlagged
    },
    {
      path: '/register',
      name: 'register',
      component: register
    },
    {
      path: '/new_album',
      name: 'newAlbum',
      component: newAlbum
    },
    {
      path: '/albums/:album_id',
      name: 'viewAlbum',
      component: viewAlbum
    },
    {
      path: '/songs/:song_id',
      name: 'viewSong',
      component: viewSong
    },
    {
      path: '/add_to_playlist',
      name: 'addToPlaylist',
      component: addToPlaylist
    },
    {
      path: '/edit_song/:song_id',
      name: editSong,
      component: editSong
    }
  ]
})

export default router
