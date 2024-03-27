import {getCookie} from "./cookie.js";

export function apiRequest(url, method, token_required, body, body_form, only_resp, check_admin) {
    let backend_url = ''
    if (import.meta.env.VITE_START_MODE === 'DEV') {
        backend_url = import.meta.env.VITE_BACKEND_URL + url
    } else {
        backend_url = url
    }
    let headers = {
        'X-CSRFToken': getCookie('csrftoken'),
    }
    if (!(body_form)) {
        headers['Content-Type'] = 'application/json;charset=UTF-8'
    }
    if (token_required) {
        headers['Authorization'] = 'Token '+getCookie('iohk_token')
    }
    let request_parameters = {
        'method': method,
        'headers': headers
    }
    if (body) {
        if (body_form) {
            request_parameters['body'] = body
        } else {
            request_parameters['body'] = JSON.stringify(body)
        }
    }
    if (only_resp) {
        return fetch(backend_url, request_parameters)
            .then(resp => (resp))
    }
    return fetch(backend_url, request_parameters)
        .then(resp => {
            if (resp.status === 401) {
                showMessage('error', 'Пожалуйста, войдите в систему', false)
                this.$router.push('/?nextUrl='+window.location.href.split('/')[3])
                return false
            } else if (check_admin && resp.status === 403) {
                showMessage('error', 'Доступ запещен', false)
                this.$router.push('/main')
                return false
            } else if (resp.status === 500) {
                showMessage('error', 'Внутренняя ошибка сервера', false)
                return false
            } else {
                return resp.json()
            }
        })
        .then(data => (data))
        .catch(e => {})
}