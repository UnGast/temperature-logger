const path = require('path')

module.exports = {

    configureWebpack: {

        resolve: {

            alias: {

                '~': path.resolve(__dirname, 'src'),
                'style': path.resolve(__dirname, 'src/assets/style/index.scss')
            }
        }
    },

    pluginOptions: {

        electronBuilder: {

            builderOptions: {

                appId: "de.adrianzimmermann.temperature-logger-client",

                productName: "Temperature Logger Client"
            }
        }
    }
}