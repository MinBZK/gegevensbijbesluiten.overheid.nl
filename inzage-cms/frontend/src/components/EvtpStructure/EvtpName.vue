<template>
  <tr class="width-height-table">
    <td>
      <a :href="getEntityRecordHref(relation, primaryKey)">
        {{ relation.values[0][nameKey] }}
      </a>
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
      default: () => {},
    },
    nameKey: {
      type: String,
      required: true,
    },
    primaryKey: {
      type: String,
      required: true,
    },
  },
  methods: {
    getEntityRecordHref(relation, primaryKey) {
      return this.$router.resolve({
        name: 'entityRecord',
        params: {
          id: relation.resource[primaryKey],
          resource: relation.resource,
          recordResource: relation.resource,
          tab: 'data',
        },
      }).href
    },
  },
})
</script>
