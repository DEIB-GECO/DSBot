export default {
  modules: ['nuxt-socket-io'],
  assetsDir: 'static',
  devServer: {
    proxy: {
      '/socket.io': {
        target: 'https://localhost:5000/', // So that the client dev server can access your socket.io
      },
    },
  },
  publicPath: '/inspire/',
  io: {
    sockets: [
      {
        name: 'main',
        url: 'http://localhost:5000',
      },
    ],
  },
}
