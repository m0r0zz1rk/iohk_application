import isAuthenticated from "./permissions/is_authenticated.js";
import isAdministrator from "./permissions/is_administrator.js";

import Login from "../../views/Login.vue";
import Main from "../../views/Main.vue";
import Profile from "../../views/Profile.vue";

import Guides from "../../views/admins/Guides.vue";

const routes = [
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
    },
    {
        path: '/admin/guides',
        name: 'Guides',
        component: Guides,
        beforeEnter: isAdministrator
    }
]

export default routes