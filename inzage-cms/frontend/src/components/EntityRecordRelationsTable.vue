<template>
  <v-table>
    <thead>
      <tr>
        <th>Entiteit</th>
        <th />
      </tr>
    </thead>
    <tbody>
      <tr
        v-for="relatedValue in relationValues"
        :key="getPrimaryKey(relatedValue)"
      >
        <td>
          {{ getDescription(relatedValue) }}
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
                    parentId: getPrimaryKey(relatedValue),
                    method: 'delete',
                  })
                  : modifyRelation({
                    childId: getPrimaryKey(relatedValue),
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
          v-if="['gg-struct'].includes(resource)"
          colspan="3"
          class="centered"
        >
          <v-btn
            v-if="(relationLabel === 'Bovenliggende entiteit' && relationValues.length === 0) || (relationLabel === 'Onderliggende entiteiten')"
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
        <td
          v-else-if="['oe-koepel-oe'].includes(resource)"
          colspan="3"
          class="centered"
        >
          <v-btn
            v-if="(relationLabel === 'Bovenliggende entiteit' && relationValues.length <= 1 )"
            color="primary"
            variant="outlined"
            :to="{
              name: 'newEntityOeKoepel',
              params: {
                structCd: recordId,
                recordResource: resource,
                structRelation: 'oe-koepel',
              },
              query: {
                redirect: $route.fullPath,
              },
            }"
          >
            Toevoegen
          </v-btn>
          <v-btn
            v-else-if="(relationLabel === 'Onderliggende entiteiten')"
            color="primary"
            variant="outlined"
            :to="{
              name: 'newEntityOeKoepelOe',
              params: {
                structCd: recordId,
                recordResource: resource,
                structRelation: 'oe-koepel-oe',
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
        gg: 'GgStruct',
      },
    }
  },
  methods: {
    getPrimaryKey(relatedValue: object) {
      if (this.resource == 'oe-koepel-oe') {
        if (relatedValue['relatedEntity']['oe_koepel_cd']) {
          return relatedValue['relatedEntity']['oe_koepel_cd']
        }
        else {
          return relatedValue['relatedEntity']['oe_cd']
        }
      }
      else {
        return relatedValue['relatedEntity'][this.primaryKey]
      }
    },
    getDescription(relatedValue: any) {
      if (this.resource == 'oe-koepel-oe') {
        if (relatedValue['relatedEntity']['titel']) {
          return relatedValue['relatedEntity']['titel']
        }
        else {
          return relatedValue['relatedEntity']['naam_officieel']
        }
      }
      else {
        return relatedValue['relatedEntity'][this.descriptionKey]
      }
    },
    async modifyRelation({ childId, parentId, method }) {
      const endpoint = `${store.state.APIurl}/${this.resource}/${childId}/parent/${parentId}`
      await axios({
        url: endpoint,
        method,
      })
      this.$emit('relationUpdated')
    },
  }
})
</script>

<style scoped lang="scss">
@import '/src/styles/styles.scss';
</style>
