/**
 * 延迟 timeout
 * 延迟10ms：sleep(10)；延迟 20ms 后返回 1：sleep(20, 1)
 * @param timeout
 * @param data
 */
export default (timeout, data) =>
  new Promise(resolve => setTimeout(() => resolve(data), timeout))
