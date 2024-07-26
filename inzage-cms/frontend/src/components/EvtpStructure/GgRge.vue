<template>
  <tr
    v-for="(resource, index) in relation.values"
    :key="index"
    class="width-height-table"
  >
    <td
      v-if="resource.length > 0"
    >
      <tr
        v-for="(gstGg, indexGstGg) in sortedResource(resource)"
        :key="indexGstGg"
      >
        <td>
          <a
            v-if="getEntityRecordHref(relation, gstGg)"
            class="cursor-hover"
            :href="getEntityRecordHref(relation, gstGg)"
          >
            {{ gstGg[relation.nameKey] }}
          </a>
          <a
            v-else
          >
            {{ gstGg[relation.nameKey] }}
          </a>
        </td>
        <v-btn
          v-if="
            relation.label == 'gegevensgroepen' && !disableEvtp
          "
          width="20"
          height="20"
          class="btn-relation"
          icon="mdi-close"
          size="x-small"
          variant="outlined"
          @click="() => deleteGstGg(gstGg['gst_gg_cd'])"
        />
        <v-btn
          v-else-if="
            relation.label == 'regelingen' && !disableEvtp
          "
          width="20"
          height="20"
          class="btn-relation"
          icon="mdi-close"
          size="x-small"
          variant="outlined"
          @click="() => deleteGstRge(gstGg['gst_rge_cd'])"
        />
      </tr>
    </td>
    <td v-else>
      {{ messsageToBeFilled }}
    </td>

    <td class="right-align">
      <v-btn
        v-if="
          relation.label == 'gegevensstroom type' && !disableEvtp && resource.length > 0
        "
        class="btn-relation"
        icon="mdi-close"
        size="x-small"
        variant="outlined"
        @click="() => deleteGstGstt(resource[0]['gst_gstt_cd'])"
      />

      <v-btn
        v-if="relation.label == 'gegevensstroom type' && !disableEvtp && resource.length == 0"
        color="primary"
        variant="outlined"
        :to="{
          name: 'newEntityGstGsttWithRelation',
          params: {
            gstCd: gstCd[index],
            recordResource: 'gst-gstt',
            versieNr: versieNr
          },
          query: {
            redirect: $route.fullPath,
          },
        }"
      >
        <v-icon> mdi-plus-box-outline </v-icon>
      </v-btn>
      <v-btn
        v-if="relation.label == 'gegevensgroepen' && !disableEvtp"
        color="primary"
        variant="outlined"
        :to="{
          name: 'newEntityGstGgWithRelation',
          params: {
            gstCd: gstCd[index],
            recordResource: 'gst-gg',
            versieNr: versieNr
          },
          query: {
            redirect: $route.fullPath,
          },
        }"
      >
        <v-icon> mdi-plus-box-outline </v-icon>
      </v-btn>

      <v-btn
        v-else-if="relation.label == 'regelingen' && !disableEvtp"
        color="primary"
        variant="outlined"
        :to="{
          name: 'newEntityGstRgeWithRelation',
          params: {
            gstCd: gstCd[index],
            recordResource: 'gst-rge',
            versieNr: versieNr
          },
          query: {
            redirect: $route.fullPath,
          },
        }"
      >
        <v-icon> mdi-plus-box-outline </v-icon>
      </v-btn>
    </td>
  </tr>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import axios from 'axios'
import store from '@/store/index'

export default defineComponent({
  name: 'GgRge',
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
    gstCd: {
      type: Array<number>,
      required: true,
    },
    disableEvtp: {
      type: Boolean,
      default: false,
      required: false,
    },
    versieNr: {
      type: [String, Number],
      required: true,
    },
  },
  emits: ['recordUpdated'],
  data() {
    return {
      messsageToBeFilled:
        'Druk op toevoegen om een koppeling te maken' as string,
    }
  },
  methods: {
    sortedResource(resource){
      let res = resource.slice().sort((a: { sort_key: number }, b: { sort_key: number }) => a.sort_key - b.sort_key)
      return res
    },
    async deleteGstGg(gst_gg_cd: string) {
      await axios.delete(`${store.state.APIurl}/gst-gg/${gst_gg_cd}`)
      this.$emit('recordUpdated')
      store.commit('activateSnackbar', {
        show: true,
        text: store.state.snackbar.succesfullDeletion,
        color: store.state.snackbar.succes_color,
      })
    },
    async deleteGstRge(gst_rge_cd: string) {
      await axios.delete(`${store.state.APIurl}/gst-rge/${gst_rge_cd}`)
      this.$emit('recordUpdated')
      store.commit('activateSnackbar', {
        show: true,
        text: store.state.snackbar.succesfullDeletion,
        color: store.state.snackbar.succes_color,
      })
    },
    async deleteGstGstt(gst_gstt_cd: string) {
      await axios.delete(`${store.state.APIurl}/gst-gstt/${gst_gstt_cd}`)
      this.$emit('recordUpdated')
      store.commit('activateSnackbar', {
        show: true,
        text: store.state.snackbar.succesfullDeletion,
        color: store.state.snackbar.succes_color,
      })
    },
    getEntityRecordHref(relation, resource) {
      if (!relation.linkedRelation){
        return ''
      }
      return this.$router.resolve({
        name: 'entityRecord',
        params: {
          id: resource[relation.linkedRelationKey],
          resource: relation.linkedRelation,
          recordResource: relation.linkedRelation,
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
.no-hover {
  cursor: default;

}
</style>
