import isAdministrator from "../permissions/is_administrator.js";

import Guides from "../../../views/admins/Guides.vue";
import Users from "../../../views/admins/Users.vue";

const admin_routes = [
    {
        path: '/guides',
        name: 'Guides',
        component: Guides,
        beforeEnter: isAdministrator
    },
    {
        path: '/users',
        name: 'Users',
        component: Users,
        beforeEnter: isAdministrator
    },

]

export default admin_routes