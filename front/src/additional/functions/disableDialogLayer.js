export function disableDialogLayer() {
    let staticAreas = document.querySelectorAll('ui5-static-area-item')
    for (let i=0;i<staticAreas.length;i++) {
        if (staticAreas[i].shadowRoot.querySelectorAll('.ui5-block-layer').length > 0) {
            staticAreas[i].shadowRoot.querySelector('.ui5-block-layer').style.display = 'none'
        }
    }
}