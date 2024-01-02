import isAuthenticated from "../permissions/is_authenticated.js";
import Events from "../../../views/users/Events.vue";
import AppView from "../../../views/users/apps/AppView.vue";


const users_routes = [
    {
        path: '/events',
        name: 'Events',
        component: Events,
        beforeEnter: [isAuthenticated, ]
    },
    {
        path: '/apps/app_detail/:eventId',
        name: 'AppView',
        component: AppView,
        beforeEnter: [isAuthenticated, ]
    }
]

export default users_routes