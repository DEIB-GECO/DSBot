module.exports = {
  assetsDir: 'static',
  devServer: {
    proxy: {
      '/socket.io': {
        target: 'http://localhost:5980/', // So that the client dev server can access your socket.io
      },
    },
  },
  publicPath: '/dsbot/',
}
