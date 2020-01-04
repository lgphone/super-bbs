import dateFormatter from './dateFormatter'

export const getThisWeek = () => {
  let date = new Date()
  let day = date.getDay() || 7
  date.setDate(date.getDate() - day)
  return date
}

export const getThisMonth = () => {
  let date = new Date()
  date.setDate(1)
  return date
}

export const getThisYear = () => {
  let date = new Date()
  return date.getFullYear()
}

export const getToday = () => {
  let date = new Date()
  date.setHours(0)
  date.setMinutes(0)
  date.setSeconds(0)
  date.setMilliseconds(0)
  return date
}

export const getMonthStart = date => {
  let startTime = new Date(date)
  startTime.setDate(1)
  startTime.setHours(0, 0, 0, 0)
  return dateFormatter(startTime, 'yyyy-MM-dd hh:mm:ss')
}

export const getMonthEnd = date => {
  let endTime = new Date(date)
  endTime.setMonth(endTime.getMonth() + 1)
  endTime.setDate(1)
  endTime.setHours(0, 0, 0, 0)
  return dateFormatter(endTime, 'yyyy-MM-dd hh:mm:ss')
}
