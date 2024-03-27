export function getCookie(c_name) {
    let cookies = document.cookie.split(/;/);
    for (let i = 0, len = cookies.length; i < len; i++) {
        let cookie = cookies[i].split(/=/);
        if ((cookie[0].trimStart() === c_name) &&
            (isNaN(Date.parse(cookie[1])))) {
            return cookie[1]
        }
    }
    return ""
}

export function setCookie(c_name, c_value) {
    document.cookie = c_name+'='+c_value+';samesite=strict';
}

export function delCookie(c_name) {
    document.cookie = c_name+'='+new Date(0);
}

export function getUrlParameter(sParam) {
    let sPageURL = window.location.search.substring(1),
        sURLVariables = sPageURL.split('&'),
        sParameterName,
        i;

    for (i = 0; i < sURLVariables.length; i++) {
        sParameterName = sURLVariables[i].split('=');

        if (sParameterName[0] === sParam) {
            return sParameterName[1] === undefined ? true : decodeURIComponent(sParameterName[1]);
        }
    }
    return false;
}

