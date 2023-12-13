import store from "../../store/index.js";

const isAuthenticated = (to, from, next) => {
    if (!(store.getters.isAuthenticated)) {
        showMessage('error', 'Пожалуйста, войдите в систему', false)
        next('/?nextUrl='+to.path)
        return
    } else {
        fetch(store.state.backendUrl+'/api/v1/auth/check_auth/', {
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
                    next()
                    return
                }
            })
    }
}

export default isAuthenticated