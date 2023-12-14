import Login from "../../../views/Login.vue";
import Main from "../../../views/Main.vue";
import isAuthenticated from "../permissions/is_authenticated.js";
import Profile from "../../../views/Profile.vue";

const base_routes = [
    {
        path: '/',
        name: 'Login',
        component: Login,
    },
    {
        path: '/main',
        name: 'Main',
        component: Main,
        beforeEnter: isAuthenticated
    },
    {
        path: '/profile',
        name: 'Profile',
        component: Profile,
        beforeEnter: isAuthenticated
    }
]

export default base_routes