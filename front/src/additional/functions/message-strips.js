export function showMessage(type, text, noHide){

    document.getElementById(type+'-strip').classList.remove("strip-hidden");
    document.getElementById(type+'-strip').classList.add("strip-visible");

    if (type != 'load') {
        document.getElementById(type+'-message').innerHTML = text;
    }

    if (!(noHide)) {
        setTimeout(() => { hideMessage(type) }, 3000);
    }
}

export function hideMessage(type){
    document.getElementById(type+'-strip').classList.remove('strip-visible')
    document.getElementById(type+'-strip').classList.add('strip-hidden')
}