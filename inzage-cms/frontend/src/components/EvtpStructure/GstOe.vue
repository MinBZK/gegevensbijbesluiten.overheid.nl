<template>
  <tr
    v-for="(resource, index) in relation.values"
    :key="index"
    class="width-height-table"
  >
    <td class="left-align">
      <tr>
        <a :href="getEntityRecordHref(relation, resource, primaryKey)">
          {{ resource[relation.nameKey] }}
        </a>
      </tr>
      <tr>
        <a
          v-if="resource.conditie"
          class="condition"
        >
          {{ resource.conditie.substr(0, 70) + (resource.conditie.length > 70 ? '...' : '') }}
        </a>
      </tr>
    </td>
    <td class="right-align">
      <tr>
        <v-btn
          v-if="relation.resource == 'gst' && !disableEvtp"
          class="btn-relation"
          icon="mdi-close"
          size="x-small"
          variant="outlined"
          @click="() => deleteGst(resource, index)"
        />
      </tr>
      <tr>
        <v-btn
          v-if="
            relation.resource == 'gst' && resource.conditie && !disableEvtp
          "
          width="20"
          height="20"
          class="btn-relation"
          icon="mdi-close"
          size="x-small"
          variant="outlined"
          @click="() => deleteCondition(resource)"
        />

        <v-btn
          v-if="
            relation.resource == 'gst' && !resource.conditie && !disableEvtp
          "
          color="primary"
          variant="plain"
          size="x-small"

          :to="getEvtpGstRecordHref(resource.evtp_gst_cd)"
        >
          <v-icon> mdi-asterisk </v-icon>
        </v-btn>
      </tr>
    </td>
  </tr>
  <br>
  <v-btn
    v-if="relation.resource == 'gst' && !disableEvtp"
    color="primary"
    variant="outlined"
    :to="{
      name: 'newEntityGstWithRelation',
      params: { evtpCd: evtpCd, recordResource: relation.resource },
      query: {
        redirect: $route.fullPath,
      },
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
  name: 'GstOe',
  props: {
    relation: {
      type: Object,
      default: () => { },
    },
    nameKey: {
      type: String,
      required: true,
    },
    primaryKey: {
      type: String,
      required: true,
    },
    evtpCd: {
      type: [String, Number],
      required: true,
    },
    gstGgCd: {
      type: Object,
      required: true,
    },
    disableEvtp: {
      type: Boolean,
      default: false,
      required: false,
    },
  },
  emits: ['recordUpdated'],
  computed: {
    getgstGg() {
      return this.gstGgCd
    },
  },
  methods: {
    async deleteGst(gstObject, index) {
      // 1. Delete gst_gg
      const postPromisesgstGg = await this.getgstGg[index].map((gst_gg) => {
        axios.delete(`${store.state.APIurl}/gst-gg/${gst_gg}`)
      })

      // 2. Delete evtp_gst
      const postPromisesEvtpGst = axios.delete(
        `${store.state.APIurl}/evtp-gst/${gstObject.evtp_gst_cd}`
      )

      // 3. Delete gst_gstt
      const postPromisesGstGsttype = await gstObject.entities_gst_gstt.map(
        (gst_gsttype) => {
          axios.delete(
            `${store.state.APIurl}/gst-gstt/${gst_gsttype.gst_gstt_cd}`
          )
        }
      )

      const postPromise = [
        postPromisesEvtpGst,
        postPromisesgstGg,
        postPromisesGstGsttype,
      ]
      Promise.all(postPromise)
        .then(() => {
          // 4. Delete gst
          store.commit('activateSnackbar', {
            show: true,
            text: store.state.snackbar.succesfullDeletion,
            color: store.state.snackbar.succes_color,
          })
        })
        .catch(() => {
          store.commit('activateSnackbar', {
            show: true,
            text: store.state.snackbar.unknown,
            color: store.state.snackbar.error_color,
          })
        })
        .finally(() => {
          this.$emit('recordUpdated')
        })
    },
    async deleteCondition(gstObject) {
      const postPromisesEvtpGstConditie = axios.delete(
        `${store.state.APIurl}/evtp-gst/attribute/conditie/${gstObject.evtp_gst_cd}`
      )
      const postPromise = [
        postPromisesEvtpGstConditie,
      ]
      Promise.all(postPromise)
        .then(() => {
          store.commit('activateSnackbar', {
            show: true,
            text: store.state.snackbar.succesfullDeletion,
            color: store.state.snackbar.succes_color,
          })
        })
        .catch(() => {
          store.commit('activateSnackbar', {
            show: true,
            text: store.state.snackbar.unknown,
            color: store.state.snackbar.error_color,
          })
        })
        .finally(() => {
          this.$emit('recordUpdated')
        })
    },
    getEntityRecordHref(relation, resource, primaryKey) {
      return this.$router.resolve({
        name: 'entityRecord',
        params: {
          id: resource[primaryKey],
          resource: relation.resource,
          recordResource: relation.resource,
          tab: 'data',
        },
      }).href
    },
    getEvtpGstRecordHref(evtp_gst_cd) {
      return this.$router.resolve({
        name: 'entityRecord',
        params: {
          id: evtp_gst_cd,
          resource: 'evtp-gst',
          recordResource: 'evtp-gst',
          tab: 'data',
        },
        query: {
            redirect: this.$route.fullPath
        },
      }).href
    },
  },
})
</script>

<style scoped lang="scss">
@import '/src/styles/styles.scss';
.condition {
  font-style: italic;
  color: black;
}
</style>
