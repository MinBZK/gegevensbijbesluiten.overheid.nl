<template>
  <v-footer
    class="footer"
    :color="colour"
    padless
  />
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import store from '@/store/index'
import { getEnvironment } from '@/util/misc'
import axios from 'axios'

export default defineComponent({
  name: 'FOOTER',
  data() {
    return {
      envObj: [] as Array<object>,
      colour: '' as string,
      environment: '' as string,
    }
  },
  async created() {
    try {
      const { data } = await axios.get(`${store.state.APIurl}/config/pod-env`)
      this.envObj = data
      this.environment = getEnvironment(this.envObj, 'ENVIRONMENT')
      this.getColour(this.environment)
    } catch (e) {
      console.error(e)
    }
  },
  methods: {
    getColour(environment: string) {
      if (environment === 'productie') {
        this.colour = 'primary'
      } else if (environment === 'acceptatie') {
        this.colour = 'green'
      } else if (environment === 'test') {
        this.colour = 'orange'
      } else {
        this.colour = 'primary'
      }
    },
  },
})
</script>

<style lang="scss">
@import '@/styles/styles.scss';

.v-footer {
  display: unset !important;
  height: 26px;
}

.footer-title {
  color: white !important;
  padding: 0 26px;
  font-weight: unset;
}

.footer-link-text {
  color: white;
}

ul {
  list-style-type: none;
  padding-left: 0 !important;
}
</style>
