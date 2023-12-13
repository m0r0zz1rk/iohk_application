function removeTableHeaderRow() {
    let tables = document.querySelectorAll('ui5-table')
    for (let i=0;i<tables.length;i++) {
        try {
            tables[i].shadowRoot.querySelector('.ui5-table-header-row').remove()
        } catch (e) {}
    }
}

function noHeadTable() {
    let tables = document.querySelectorAll('.no-head-table')
    let headerRow = null
    for (let i=0;i<tables.length;i++) {
        try {
            headerRow = tables[i].shadowRoot.querySelector('.ui5-table-header-row')
            headerRow.parentNode.removeChild(headerRow)
        } catch (e) {}

    }
}

function changeTableView() {
    let TableColumns = document.querySelectorAll('ui5-table-column')
    for (let i=0;i<TableColumns.length;i++) {
        try {
            TableColumns[i].shadowRoot.querySelector("[part='column']").style['text-align'] = 'center'
            TableColumns[i].shadowRoot.querySelector("[part='column']").style['border'] = '1px solid #737270'
        } catch (e) {}

    }
}

function convertToJSDate(dateString) {
    let year = dateString.substring(6, 10)
    let month = dateString.substring(3, 5)
    let day = dateString.substring(0, 2)
    return year+'-'+month+'-'+day
}

function getDay(yesterday) {
    let date = new Date();
    if (yesterday) {
        date.setDate(date.getDate()-1)
    }
    return date.getDate()+'.'+(date.getMonth()+1)+'.'+date.getFullYear()
}