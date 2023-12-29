import isAuthenticated from "../permissions/is_authenticated.js";
import Events from "../../../views/users/Events.vue";


const users_routes = [
    {
        path: '/events',
        name: 'Events',
        component: Events,
        beforeEnter: [isAuthenticated, ]
    },
]

export default users_routes