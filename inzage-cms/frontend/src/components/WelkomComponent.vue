<template>
  <div class="Parent">
    <div
      style="
        position: absolute;
        up: 0;
        right: 0;
        width: 300px;
        text-align: center;
      "
    >
      <em> {{ `${environment} omgeving versie ${version}` }} </em>
    </div>
    <div
      class="column"
      aria-label="hidden"
    >
      <v-img
        width="100%"
        alt="welkom image"
        :src="require('@/assets/welkom.png')"
      />
    </div>
    <div class="column">
      <h1>{{ page.title }}</h1>
      <p class="pt-0">
        {{ page.paragraphs.text_1 }}
      </p>
      <p />
      <button
        color="primary"
        class="link"
        @click="handleLoginClick"
      >
        Login voor toegang
      </button>
    </div>
  </div>
</template>

<script lang="ts">
import content from '@/content.json'
import { defineComponent } from 'vue'
import axios from 'axios'
import store from '@/store'
import { getEnvironment } from '@/util/misc'

export default defineComponent({
  name: 'WelkomComponent',
  data() {
    return {
      page: content.pages.welkom,
      links: content.links,
      environment: '' as string,
      version: '' as string,
      envObj: [] as Array<object>,
      keycloak: store.state.keycloak,
    }
  },
  async created() {
    try {
      const { data } = await axios.get(`${store.state.APIurl}/config/pod-env`)
      this.envObj = data
      this.version = getEnvironment(this.envObj, 'VERSION')
      this.environment = getEnvironment(this.envObj, 'ENVIRONMENT')
    } catch (e) {
      console.error(e)
    }
  },
  methods: {
    handleLoginClick() {
      const isAuthEnabled = process.env.VUE_APP_USE_AUTH === 'true'

      if (isAuthEnabled) {
        // Authentication is enabled, call keycloak.login()
        this.keycloak.login()
      } else {
        // Authentication is disabled, navigate to /dashboard
        this.$router.push('/dashboard')
      }
    },
  },
})
</script>

<style lang="scss" scoped>
.link {
  font-size: large;
  background-color: unset;
  color: #01689b;

  &:hover {
    text-decoration: underline;
    cursor: pointer;
  }
}
</style>
