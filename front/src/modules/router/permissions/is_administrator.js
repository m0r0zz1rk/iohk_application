import '../../../additional/init.js'
import store from "../../store/index.js";
import {showMessage} from "../../../additional/functions/message-strips.js";

const isAdministrator = (to, from, next) => {
    fetch('/api/v1/auth/check_admin/', {
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