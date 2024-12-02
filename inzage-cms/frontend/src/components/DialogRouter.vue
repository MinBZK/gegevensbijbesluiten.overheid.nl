<template>
  <v-tooltip v-model="showToolTip"></v-tooltip>
  <v-dialog
    no-click-animation
    scrollable
    persistent
    :max-width="maxWidthDialog"
    :model-value="true"
    @click:outside="close()"
  >
    <v-card>
      <v-card-title v-if="component.name !== 'OverviewEvtpTree'">{{ title }}</v-card-title>
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
import OverviewEvtpTree from '@/components/EvtpTable/OverviewEvtpTree.vue'

export default defineComponent({
  name: 'DialogRouter',
  components: {
    OverviewEvtpTree
  },
  props: {
    component: {
      type: Object,
      default: () => {}
    },
    childProps: {
      type: Object,
      default: () => {}
    },
    maxWidthDialog: {
      type: Number,
      default: 0
    },
    title: {
      type: String,
      default: ''
    }
  },
  emits: ['recordUpdated'],
  data() {
    return {
      showToolTip: false,
      modelShow: true
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
    }
  }
})
</script>
