import {delCookie, getCookie, setCookie} from "../../additional/functions/cookie.js";
import {showMessage} from "../../additional/functions/message-strips.js";
import { createStore } from 'vuex'
import createPersistedState from 'vuex-persistedstate'
import {apiRequest} from "../../additional/functions/api_request.js";

export default createStore({
    plugins: [createPersistedState({
        storage: window.localStorage,
    })],
    state: {
        backendUrl: import.meta.env.VITE_BACKEND_URL,
        recCountOptions: import.meta.env.VITE_APP_REC_COUNT_OPTIONS,
        iohk_token: getCookie('iohk_token') || '',
        status: '',
    },
    getters: {
        getServerUrl: state => state.backendUrl,
        isAuthenticated: state => !!state.iohk_token,
        authStatus: state => state.status,
    },
    mutations: {
        AUTH_REQUEST (state) {
            state.status = 'loading'
        },
        AUTH_SUCCESS (state, token) {
            state.status = 'success'
            state.iohk_token = token
        },
        AUTH_LOGOUT (state) {
            state.iohk_token = ''
        },
        AUTH_ERROR (state) {
            state.status = 'error'
        },
    },
    actions: {
        AUTH_REQUEST ({commit, dispatch}, user ) {
            return new Promise((resolve, reject) => { // The Promise used for router redirect in login
                commit('AUTH_REQUEST');
                apiRequest(
                    '/api/v1/auth/login/',
                    'POST',
                    false,
                    {
                        'username': user.username,
                        'password': user.password
                    },
                    false,
                    false
                )
                    .then(data => {
                        if (!('iohk_token' in data)){
                            commit('AUTH_ERROR', data.error)
                            showMessage('error', data.error, false)
                            reject(data.error)
                        } else {
                            const token = data.iohk_token
                            commit('AUTH_SUCCESS', token)
                            setCookie('iohk_token', token)
                            showMessage('success', 'Вход выполнен успешно', false);
                            resolve();
                        }
                    })
                    .catch(err => {
                        commit('AUTH_ERROR', err)
                        delCookie('iohk_token') // if the request fails, remove any possible user token if possible
                        delCookie('iohk_is_admin') // if the request fails, remove any possible user token if possible
                        reject(err)
                        showMessage('error', 'Неудачная попытка входа в систему. Попробуйте еще раз', false)
                    })
            })
        },
        AUTH_LOGOUT ({commit, dispatch}) {
            return new Promise((resolve, reject) => {
                delCookie('iohk_token') // clear your user's token from localstorage
                commit('AUTH_LOGOUT')
                resolve()
            })
        }
    },
    modules: {
    }
})