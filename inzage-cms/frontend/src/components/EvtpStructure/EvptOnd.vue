<template>
  <tr v-for="(resource, index) in relation.values" :key="index" class="width-height-table">
    <td class="left-align">
      <a
        v-if="getEntityRecordHref(relation, resource)"
        class="cursor-hover"
        :href="getEntityRecordHref(relation, resource)"
      >
        {{ resource[relation.nameKey] }}
      </a>
      <a v-else>
        {{ resource[relation.nameKey] }}
      </a>
    </td>
    <td class="right-align">
      <v-btn
        v-if="relation.resource == 'ond' && !disableEvtp"
        class="btn-relation"
        icon="mdi-close"
        size="x-small"
        variant="outlined"
        @click="() => deleteOnd(resource)"
      />
      <v-btn
        v-if="relation.resource == 'oe-com-type' && !disableEvtp"
        class="btn-relation"
        icon="mdi-close"
        size="x-small"
        variant="outlined"
        @click="() => deleteOeComType(resource)"
      />
    </td>
  </tr>
  <br />
  <v-btn
    v-if="relation.resource == 'ond' && !disableEvtp"
    color="primary"
    variant="outlined"
    :to="{
      name: 'newEntityEvtpOndWithRelation',
      params: {
        evtpCd: evtpCd,
        versieNr: versieNr,
        recordResource: 'evtp-ond'
      },
      query: {
        redirect: $route.fullPath
      }
    }"
  >
    <v-icon> mdi-plus-box-outline </v-icon>
  </v-btn>

  <v-btn
    v-if="relation.resource == 'oe-com-type' && !disableEvtp"
    color="primary"
    variant="outlined"
    :to="{
      name: 'newEntityEvtpOeComTypeWithRelation',
      params: {
        evtpCd: evtpCd,
        versieNr: versieNr,
        recordResource: 'evtp-oe-com-type'
      },
      query: {
        redirect: $route.fullPath
      }
    }"
  >
    <v-icon> mdi-plus-box-outline </v-icon>
  </v-btn>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import axios from 'axios'
import store from '@/store/index'

export default defineComponent({
  name: 'EvptOnd',
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
    },
    evtpCd: {
      type: [String, Number],
      required: true
    },
    versieNr: {
      type: [String, Number],
      required: true
    },
    disableEvtp: {
      type: Boolean,
      default: false,
      required: false
    }
  },
  emits: ['recordUpdated'],
  methods: {
    async deleteOeComType(oeComTypeObject) {
      const postPromisesoeoeComType = await axios.delete(
        `${store.state.APIurl}/evtp-oe-com-type/${oeComTypeObject.evtp_oe_com_type_cd}`
      )
      const postPromise = [postPromisesoeoeComType]
      Promise.all(postPromise)
        .then(() => {
          store.commit('activateSnackbar', {
            show: true,
            text: store.state.snackbar.succesfullDeletion,
            color: store.state.snackbar.succes_color
          })
        })
        .catch(() => {
          store.commit('activateSnackbar', {
            show: true,
            text: store.state.snackbar.unknown,
            color: store.state.snackbar.error_color
          })
        })
        .finally(() => {
          this.$emit('recordUpdated')
        })
    },
    async deleteOnd(ondObject) {
      // 2. Delete evtp_ond
      const postPromisesEvtpOnd = await axios.delete(
        `${store.state.APIurl}/evtp-ond/${ondObject.evtp_ond_cd}`
      )
      const postPromise = [postPromisesEvtpOnd]
      Promise.all(postPromise)
        .then(() => {
          // 4. Delete ond
          // axios.delete(`${store.state.APIurl}/ond/${ondObject.ond_cd}`)
          store.commit('activateSnackbar', {
            show: true,
            text: store.state.snackbar.succesfullDeletion,
            color: store.state.snackbar.succes_color
          })
        })
        .catch(() => {
          store.commit('activateSnackbar', {
            show: true,
            text: store.state.snackbar.unknown,
            color: store.state.snackbar.error_color
          })
        })
        .finally(() => {
          this.$emit('recordUpdated')
        })
    },
    getEntityRecordHref(relation, resource) {
      if (!relation.linkedRelation) {
        return ''
      }
      return this.$router.resolve({
        name: 'entityRecord',
        params: {
          id: resource[relation.linkedRelationKey],
          resource: relation.linkedRelation,
          recordResource: relation.linkedRelation,
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

<style scoped lang="scss">
@import '/src/styles/styles.scss';
</style>
