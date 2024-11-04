import { createStore } from 'vuex'
import Keycloak from 'keycloak-js'

const store = createStore({
  state: {
    keycloak: {} as Keycloak,
    user: {
      email: '',
      token: '',
      admin: false,
      isAuthenticated: false
    },
    APIurl: 'http://localhost:8000/api',
    snackbar: {
      color: '',
      feedbackMessage: '',
      error_color: 'red',
      succes_color: 'green-lighten-4',
      succesfullAdditions: 'Uw toevoeging is succesvol opgeslagen',
      succesfullMutations: 'Uw wijziging is succesvol opgeslagen',
      succesfullDeletion: 'Uw verwijdering is definitief',
      foreignKeyConstraints:
        'Error: er zijn nog verwijzingen naar deze rij vanuit een andere tabel',
      wrongFileExtension: 'Let op, bestand is niet geupload omdat deze geen pdf of word betreft.',
      malwareDetected:
        'Let op, bestand is niet geupload vanwege een potentiele virus in het bestand',
      unknown: 'Er is iets mis gegaan',
      duplication: 'Error: deze koppeling bestaat al in de tabel',
      show: false
    }
  },
  mutations: {
    changeUserEmail(state, payload) {
      state.user.email = payload
    },
    changeUserToken(state, payload) {
      state.user.token = payload
    },
    changeKeycloak(state, payload) {
      state.keycloak = payload
    },
    changeUserAuthenticated(state, payload) {
      state.user.isAuthenticated = payload
    },
    changeAPIurl(state, payload) {
      state.APIurl = payload
    },
    activateSnackbar(state, { show, text, color }) {
      state.snackbar.feedbackMessage = text
      state.snackbar.show = show
      state.snackbar.color = color
    }
  },
  actions: {
    updateUserEmail({ commit }, payload) {
      commit('changeUserEmail', payload)
    },
    updateUserToken({ commit }, payload) {
      commit('changeUserToken', payload)
    },
    updateUserAuthenticated({ commit }, payload) {
      commit('changeUserAuthenticated', payload)
    },
    updateAPIurl({ commit }, payload) {
      commit('changeAPIurl', payload)
    }
  },
  modules: {}
})

export default store
