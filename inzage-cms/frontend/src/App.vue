<template>
  <v-app>
    <HeaderCms />
    <v-main>
      <router-view />
      <v-snackbar
        v-model="getSnackbar"
        :timeout="2000"
        :color="getFeedbackMessageColor()"
      >
        {{ getFeedbackMessage() }}
        <template #actions>
          <v-btn
            variant="text"
            @click="closeSnackbar"
          >
            <v-icon>mdi-window-close</v-icon>
          </v-btn>
        </template>
      </v-snackbar>
    </v-main>
    <FooterCms />
  </v-app>
</template>

<script lang="ts">
import HeaderCms from './components/HeaderCms.vue'
import FooterCms from './components/FooterCms.vue'
import store from '@/store'

export default {
  name: 'App',
  components: {
    HeaderCms,
    FooterCms,
  },
  computed: {
    getSnackbar: {
      get() {
        return store.state.snackbar.show
      },
      set(value) {
        store.commit('activateSnackbar', { show: value })
      },
    },
  },
  methods: {
    closeSnackbar() {
      store.commit('activateSnackbar', { show: false, text: '' })
    },
    getFeedbackMessage() {
      return store.state.snackbar.feedbackMessage
    },
    getFeedbackMessageColor() {
      return store.state.snackbar.color
    },
  },
}
</script>
