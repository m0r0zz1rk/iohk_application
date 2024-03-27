import '../../../additional/init.js'
import store from "../../store/index.js";
import {showMessage} from "../../../additional/functions/message-strips.js";
import {setCookie} from "../../../additional/functions/cookie.js";

const isAuthenticated = (to, from, next) => {
    if (!(store.getters.isAuthenticated)) {
        showMessage('error', 'Пожалуйста, войдите в систему', false)
        next('/?nextUrl='+to.path)
        return
    } else {
        fetch('/api/v1/auth/check_auth/', {
            method: 'GET',
            headers: {
                'Authorization': 'Token '+store.state.iohk_token
            },
        })
            .then(resp => {
                if (resp.status === 401 || resp.status === 403) {
                    showMessage('error', 'Пожалуйста, войдите в систему', false)
                    next('/?nextUrl='+to.path)
                    return
                } else if (resp.status === 500) {
                    showMessage('error', 'Произошла внутренняя ошибка сервера, повторите попытку позже', false)
                    next('/?nextUrl='+to.path)
                    return
                } else {
                    setCookie('iohk_token', store.state.iohk_token)
                    next()
                    return
                }
            })
    }
}

export default isAuthenticated