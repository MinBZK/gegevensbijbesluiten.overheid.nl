<template>
  <div>
    <div class="column">
      <h1>{{ page.l_title }}</h1>
      <v-btn
        class="blue two-btns ja-nee"
        depressed
        color="primary"
        @click="handleLogOut()"
      >
        Ja
      </v-btn>
      <v-btn
        class="red two-btns ja-nee"
        depressed
        color="error"
        @click="toDashboardCharts()"
      >
        Nee
      </v-btn>
    </div>
    <div class="column">
      <h1>{{ page.r_title }}</h1>
      <p class="pt-0">
        {{ page.r_paragraphs.text_1 }}
      </p>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import content from '@/content.json'
import store from '@/store/index'

export default defineComponent({
  name: 'LogoutComponent',
  data: () => ({
    page: content.pages.logout,
  }),
  methods: {
    handleLogOut() {
      const isAuthEnabled = process.env.VUE_APP_USE_AUTH === 'true'

      if (isAuthEnabled) {
        store.state.keycloak.logout({ redirectUri: `${window.location.origin}/` })
        store.commit('changeUserEmail', '')
        store.commit('changeUserAdmin', false)
        store.commit('changeUserAuthenticated', false)
        store.commit('changeUserToken', '')
        store.commit('changeDocuments', [])
        console.log('logging out')
      } else {
        // Authentication is disabled, navigate to /dashboard
        this.$router.push('/')
      }
    },
    toDashboardCharts() {
      this.$router.push('/dashboard')
    },
  },
})
</script>
