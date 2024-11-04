<template>
  <tr class="width-height-table">
    <td>
      <tr>
        <a :href="getEntityRecordHref(relation, primaryKey)" class="cursor-hover">
          {{ relation.values[0][nameKey] }}
        </a>
      </tr>
      <tr v-if="relation.values[0].entity_omg">
        <a class="subtext">
          {{
            relation.values[0].entity_omg.titel.substr(0, 70) +
            (relation.values[0].entity_omg.titel.length > 70 ? '...' : '')
          }}
        </a>
      </tr>
    </td>
  </tr>
</template>

<script lang="ts">
import { defineComponent } from 'vue'

export default defineComponent({
  name: 'EvtpName',
  props: {
    relation: {
      type: Object,
      default: () => {}
    },
    nameKey: {
      type: String,
      required: true
    },
    primaryKey: {
      type: String,
      required: true
    }
  },
  methods: {
    getOmgRecordHref(relation, primaryKey) {
      return this.getEntityRecordHref(relation, primaryKey)
    },
    getEntityRecordHref(relation, primaryKey) {
      return this.$router.resolve({
        name: 'entityRecord',
        params: {
          id: relation.resource[primaryKey],
          resource: relation.resource,
          recordResource: relation.resource,
          tab: 'data'
        },
        query: {
          redirect: this.$route.fullPath
        }
      }).href
    }
  }
})
</script>
