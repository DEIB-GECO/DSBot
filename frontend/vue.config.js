module.exports = {
  assetsDir: 'static',
  devServer: {
    proxy: {
      '/socket.io': {
        target: 'https://localhost:5000/', // So that the client dev server can access your socket.io
      },
    },
  },
  publicPath: '/inspire/',
}
