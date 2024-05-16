const { defineConfig } = require("@vue/cli-service")

module.exports = defineConfig({
  transpileDependencies: ["vuetify"],
  configureWebpack: {
    devtool: "source-map",
    module: {
      rules: [
        {
          test: /urlsEnv.*urlsEnv\.ts$/,
          use: [
            {
              loader: "file-loader",
              options: {
                name: "urlsEnv.ts",
              },
            },
          ],
        },
      ],
    },
  },
  chainWebpack: (config) => {
    config.plugin("html").tap((args) => {
      args[0].title = process.env.VUE_APP_TITLE
      return args
    })
  },
  lintOnSave: false,
  pluginOptions: {
    vuetify: {
      // https://github.com/vuetifyjs/vuetify-loader/tree/next/packages/vuetify-loader
    },
  },
})
