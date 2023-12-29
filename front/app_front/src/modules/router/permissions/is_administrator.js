import store from "../../store/index.js";
import {apiRequest} from "../../../additional/functions/api_request.js";

const isAdministrator = (to, from, next) => {
    fetch(store.state.backendUrl+'/api/v1/auth/check_admin/', {
        method: 'GET',
        headers: {
            'Authorization': 'Token '+store.state.iohk_token
        },
    })
        .then(resp => {
            if (resp.status === 403) {
                showMessage('error', 'У вас нет доступа на просмотр данного раздела', false)
                next('/main')
                return
            } else if (resp.status === 500) {
                showMessage('error', 'Произошла внутренняя ошибка сервера, повторите попытку позже', false)
                next('/main')
                return
            } else {
                next()
                return
            }
        })
}

export default isAdministrator