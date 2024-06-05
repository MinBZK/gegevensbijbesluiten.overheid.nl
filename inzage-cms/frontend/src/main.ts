import { createApp } from 'vue'
import App from './App.vue'
import store from './store'
import router from './router'
import 'vuetify/styles' // Global CSS has to be imported
import { createVuetify } from 'vuetify'
import Keycloak from 'keycloak-js'
import axios from 'axios'

const isAuthEnabled = process.env.VUE_APP_USE_AUTH === 'true'

if (process.env.NODE_ENV === 'production') {
  store.commit('changeAPIurl', `${window.location.origin}/api`)
}

const vuetify = createVuetify({
  theme: {
    themes: {
      light: {
        dark: false,
        colors: {
          primary: '#01689B',
          secondary: '#94c7e0',
          tertiary: '#bedef0',
          quaternary: '#cae3f0',
          quinary: '#d2e5ee',
          accent: '#82B1FF',
          error: '#FF5252',
          info: '#2196F3',
          success: '#4CAF50',
          warning: '#FFC107',
          headerTextColour: '#000000',
          headerHoverColour: '#FCF29A',
        },
      },
    },
    cspNonce: 'eQw4j9WgXcB',
  },
})

export function getConfigs(): Promise<any> {
  return new Promise((resolve) => {
    axios
      .get(`${store.state.APIurl}/config/keycloak-env`, { timeout: 2000 })
      .then((response) => {
        console.log(response.data)
        resolve(response.data)
      })
      .catch(function (err) {
        console.log('failed to get config ' + err)
      })
  })
}

if (isAuthEnabled) {
  // Authentication is enabled
  getConfigs().then((response: any) => {
    const initOptions: any = {
      url: `${response.keycloak_uri}`,
      realm: `${response.keycloak_realm}`,
      clientId: `${response.keycloak_client}`,
      onLoad: 'check-sso',
    }
    const keycloak = new Keycloak(initOptions)

    console.log('initializing keycloak')
    keycloak
      .init({ onLoad: initOptions.onLoad })
      .then((auth) => {
        if (!auth) {
          console.log('not yet Authenticated.')
        } else {
          console.log('Authenticated')
        }

        // always add the authentication header to axios requests
        axios.interceptors.request.use(function (config) {
          const token = keycloak!.idToken
          config.headers!.Authorization = `Bearer ${token}`
          return config
        })

        // commit keycloak to store
        store.commit('changeKeycloak', keycloak)

        // create application
        createApp(App)
          .use(router)
          .use(store)
          .use(vuetify)
          .mount('#app')

        //Token Refresh
        setInterval(() => {
          keycloak
            .updateToken(70)
            .then((refreshed) => {
              if (refreshed) {
                console.log('Token refreshed' + refreshed)
              } else {
                console.log(
                  'Token not refreshed, valid for ' +
                    Math.round(
                      keycloak.tokenParsed!.exp! +
                        keycloak.timeSkew! -
                        new Date().getTime() / 1000
                    ) +
                    ' seconds'
                )
              }
            })
            .catch(() => {
              console.error('Failed to refresh token')
            })
        }, 6000)
      })
      .catch((error) => {
        console.error('error initializing keycloak')
        console.log(error)
      })
      .catch(function (err) {
        console.log('failed to get config from backend ' + err)
      })
  })
} else {
  // Authentication is disabled
  // Create the application without Keycloak
  createApp(App)
    .use(router)
    .use(store)
    .use(vuetify)
    .mount('#app')
}
