const path = require('path')

const resolve = dir => path.join(__dirname, dir)

let assetsDir = (() => {
  return 'static/'
})()

module.exports = {
  baseUrl: process.env.BASE_URL,
  devServer: {
    hot: true,
    host: '0.0.0.0',
    port: 80,
    open: false,
    disableHostCheck: true,
    https: false,
    hotOnly: false,
    proxy: {
      '/api': {
        target: 'http://172.17.76.64:5000',
        changeOrigin: true
      }
    }
  },
  configureWebpack: {
    resolve: {
      alias: {
        '@': resolve('src')
      }
    }
  },
  assetsDir: assetsDir,
  productionSourceMap: false
}
