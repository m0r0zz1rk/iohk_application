import event_statuses from "../consts/event_statuses.js";

export function event_status_display_name(event_status) {
    return event_statuses[event_status]
}

export function event_status_db_name(display_status) {
    let res_key = ''
    Object.keys(event_statuses).map((key) => {
      if (event_statuses[key] === display_status) {
          res_key = key
      }
    })
    return res_key
}