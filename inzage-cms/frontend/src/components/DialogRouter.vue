<template>
  <v-dialog
    :max-width="maxWidthDialog"
    no-click-animation
    scrollable
    :model-value="true"
    persistent
    @click:outside="close()"
  >
    <v-card :class="{ 'no-horizontal-scroll': childProps.tab !== 'relations' }">
      <v-card-title>{{ $attrs.title }}</v-card-title>
      <component
        :is="component"
        v-bind="childProps"
        @confirm="close()"
        @close="close()"
        @record-updated="$emit('recordUpdated')"
      />
    </v-card>
  </v-dialog>
</template>

<script lang="ts">
import { defineComponent } from 'vue'

export default defineComponent({
  name: 'DialogRouter',
  props: {
    component: {
      type: Object,
      default: () => {},
    },
    childProps: {
      type: Object,
      default: () => {},
    },
    maxWidthDialog: {
      type: Number,
      default: 0,
    },
  },
  emits: ['recordUpdated'],
  data() {
    return {
      modelShow: true,
    }
  },
  methods: {
    close() {
      const parentRoute = this.$route.matched[0]
      const params = this.$route.params
      const redirectUrl = this.$route.query['redirect']
      if (redirectUrl) {
        this.$router.push(redirectUrl.toString())
      } else {
        this.$router.push({ name: parentRoute.name, state: { params } })
      }
    },
  },
})
</script>

<style scoped>
.v-card {
  display: flex !important;
  flex-direction: column;
  overflow-x: auto;
}
.no-horizontal-scroll {
  overflow-x: hidden;
}
</style>
