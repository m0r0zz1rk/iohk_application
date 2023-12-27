const statuses = {
    'CREATED': 'Создано',
    'PUBLISHED': 'Опубликовано',
    'CANCELED': 'Отменено',
    'ONGOING': 'В процессе',
    'COMPLETED': 'Завершено',
    'REMOVED': 'Снято с публикации',
}

export function event_status_display_name(event_status) {
    return statuses[event_status]
}

export function event_status_db_name(display_status) {
    let res_key = ''
    Object.keys(statuses).map((key) => {
      if (statuses[key] === display_status) {
          res_key = key
      }
    })
    return res_key
}