import base_routes from "./routes/base_routes.js";
import admin_routes from "./routes/admin_routes.js";

const routes = base_routes.concat(admin_routes)

export default routes