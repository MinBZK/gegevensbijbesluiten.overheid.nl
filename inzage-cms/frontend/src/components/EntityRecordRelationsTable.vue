<template>
  <v-table>
    <thead>
      <tr>
        <th>Entiteit</th>
        <th>Rol</th>
        <th />
      </tr>
    </thead>
    <tbody>
      <tr
        v-for="relatedValue in relationValues"
        :key="relatedValue[primaryKey]"
      >
        <td>
          <router-link
            :to="{
              name: 'entityRecord',
              params: {
                id: relatedValue['relatedEntity'][primaryKey],
                resource: $route.params.resource,
                recordResource: $route.params.recordResource,
                tab: 'relations',
              },
            }"
          >
            {{ relatedValue['relatedEntity'][descriptionKey] }}
          </router-link>
        </td>
        <td>
          <v-btn
            class="btn-relation"
            icon="mdi-close"
            size="x-small"
            variant="outlined"
            @click="
              () =>
                relationKey == 'parents'
                  ? modifyRelation({
                    childId: recordId,
                    parentId: relatedValue['relatedEntity'][primaryKey],
                    method: 'delete',
                  })
                  : modifyRelation({
                    childId: relatedValue['relatedEntity'][primaryKey],
                    parentId: recordId,
                    method: 'delete',
                  })
            "
          />
        </td>
      </tr>
      <tr>
        <td
          v-if="relationValues.length == 0"
          colspan="3"
        >
          Geen {{ relationLabel.toLowerCase() }}
        </td>
      </tr>
      <tr>
        <td
          colspan="3"
          class="centered"
        >
          <v-btn
            color="primary"
            variant="outlined"
            :to="{
              name: 'newEntityGGStruct',
              params: {
                structCd: recordId,
                recordResource: resource,
                structRelation: relationKey,
              },
              query: {
                redirect: $route.fullPath,
              },
            }"
          >
            Toevoegen
          </v-btn>
        </td>
      </tr>
    </tbody>
  </v-table>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import store from '@/store/index'
import type { PropType } from 'vue'
import axios from 'axios'

export default defineComponent({
  name: 'EntityRecordRelationsTable',
  props: {
    relationValues: {
      type: Array as PropType<object[]>,
      default: () => [],
    },
    relationLabel: {
      type: String,
      required: true,
    },
    relationKey: {
      type: String,
      required: true,
    },
    primaryKey: {
      type: String,
      required: true,
    },
    descriptionKey: {
      type: String,
      required: true,
    },
    endpoint: {
      type: String,
      required: true,
    },
    resource: {
      type: String,
      required: true,
    },
    recordId: {
      type: [String, Number],
      required: true,
    },
  },
  emits: ['relationUpdated'],
  data() {
    return {
      relationResource: {
        Oes: 'Oestructuur',
        gg: 'GgStruct',
      },
    }
  },
  methods: {
    async modifyRelation({ childId, parentId, method }) {
      const endpoint = `${store.state.APIurl}/${this.resource}/${childId}/parent/${parentId}`
      await axios({
        url: endpoint,
        method,
      })
      this.$emit('relationUpdated')
    },
  },
})
</script>

<style scoped lang="scss">
@import '/src/styles/styles.scss';
</style>
