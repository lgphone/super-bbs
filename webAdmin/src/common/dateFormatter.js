export default (date, format) => {
  const o = {
    'M+': date.getMonth() + 1,
    'd+': date.getDate(),
    'h+': date.getHours(),
    'm+': date.getMinutes(),
    's+': date.getSeconds(),
    'q+': Math.floor((date.getMonth() + 3) / 3),
    'S+': date.getMilliseconds()
  }
  format = format.replace(/y+/, match =>
    (date.getFullYear() + '').substr(4 - match.length)
  )
  for (let k in o) {
    format = format.replace(new RegExp(k), match => {
      return match.length === 1
        ? o[k]
        : ('00' + o[k]).substr(('' + o[k]).length)
    })
  }
  return format
}
