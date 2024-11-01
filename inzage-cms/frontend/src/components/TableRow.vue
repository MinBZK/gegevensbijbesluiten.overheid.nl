<template>
  <tr>
    <td class="text-left">
      <v-row class="centered" style="white-space: nowrap; display: inline-block">
        <v-btn
          v-if="id && resource === 'evtp-version' && currentVersion"
          color="primary"
          class="mx-2 table-button"
          flat
          :to="{
            name: 'adjustEvtpVersion',
            params: {
              id,
              resource,
              recordResource: resource,
              versieNr: versieNr
            }
          }"
        >
          <v-tooltip activator="parent" location="top"> Wijzigen </v-tooltip>
          <v-icon>mdi-pencil</v-icon>
        </v-btn>
        <v-btn
          v-if="id && resource !== 'evtp-version' && currentVersion"
          color="primary"
          class="mx-2 table-button"
          flat
          :to="{
            name: 'entityRecord',
            params: {
              id,
              resource,
              recordResource: resource,
              tab: 'data'
            }
          }"
        >
          <v-tooltip activator="parent" location="top"> Wijzigen </v-tooltip>
          <v-icon>mdi-pencil</v-icon>
        </v-btn>
        <v-btn
          v-if="['evtp-version'].includes(resource)"
          :to="{
            name: 'newEvtpVersion',
            params: {
              id,
              resource,
              recordResource: resource,
              versieNr: versieNr ? versieNr + 1 : null
            }
          }"
          color="warning"
          flat
          class="mx-2 table-button"
        >
          <v-tooltip activator="parent" location="top"> Nieuwe versie aanmaken </v-tooltip>
          <v-icon>mdi-table-multiple</v-icon>
        </v-btn>
        <v-btn
          v-if="['evtp-version'].includes(resource)"
          :to="{
            name: 'duplicateEvtpVersion',
            params: {
              id,
              resource,
              recordResource: resource,
              versieNr: versieNr ? versieNr + 1 : null
            }
          }"
          color="green"
          flat
          class="mx-2 table-button"
        >
          <v-tooltip activator="parent" location="top"> Soortgelijke besluit maken </v-tooltip>
          <v-icon>mdi-plus-box-multiple-outline</v-icon>
        </v-btn>
        <v-btn
          v-if="['gg', 'gg-koepel', 'oe', 'oe-koepel'].includes(resource)"
          :to="{
            name: 'entityRecordRelations',
            params: {
              id,
              resource,
              recordResource: resource,
              tab: 'relations'
            }
          }"
          color="secondary"
          flat
          class="mx-2 table-button"
        >
          <v-tooltip activator="parent" location="top">
            {{
              ['gg', 'gg-koepel'].includes(resource)
                ? 'Relatie gegevensgroep'
                : ['oe', 'oe-koepel'].includes(resource)
                ? 'Relatie organisatie'
                : ''
            }}
          </v-tooltip>
          <v-icon>mdi-arrow-up-down-bold-outline</v-icon>
        </v-btn>
        <v-btn
          v-if="['evtp-version'].includes(resource)"
          :to="{
            name: 'entityEvtpStructure',
            params: {
              id,
              resource,
              recordResource: resource,
              tab: 'relations',
              versieNr: versieNr
            }
          }"
          color="secondary"
          flat
          class="mx-2 table-button"
        >
          <v-tooltip activator="parent" location="top">
            {{ 'Besluitenboom structuur' }}
          </v-tooltip>
          <v-icon>mdi-arrow-up-down-bold-outline</v-icon>
        </v-btn>
        <v-btn
          v-if="id && !idPublicatiestatusBool && currentVersion"
          color="error"
          class="mx-2 table-button"
          flat
          @click="deleteObject(id)"
        >
          <v-tooltip activator="parent" location="top"> Verwijderen </v-tooltip>
          <v-icon>mdi-close</v-icon>
        </v-btn>
        <span v-if="!currentVersion" color="primary" class="mx-2 table-button">
          <v-tooltip activator="parent" location="top"> Oudere versie </v-tooltip>
          <v-icon> mdi-file-hidden </v-icon>
        </span>
      </v-row>
    </td>
    <td v-for="dC in dataColumns" :key="dC">
      {{ getValue(dC) }}
    </td>
  </tr>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import type { PropType } from 'vue'
import axios from 'axios'
import store from '@/store/index'
import { TableModelForeignKey } from '@/types/Tables'
import { getTableValue, formatDateToLocale } from '@/util/misc'
import { getPublicatieStatus } from '@/types/PublicatieStatus'

export default defineComponent({
  name: 'TableRow',
  props: {
    dataColumns: {
      type: Object as PropType<Array<string>>,
      required: true
    },
    row: {
      type: Object,
      default: () => {}
    },
    primaryKey: {
      type: [Number, String],
      required: true
    },
    foreignKeys: {
      type: Object as PropType<Array<TableModelForeignKey>>,
      required: true
    },
    idPublicatiestatusBool: {
      type: Boolean,
      required: true
    },
    versieNr: {
      type: Number,
      default: 1,
      required: false
    }
  },
  emits: ['relationUpdated'],
  computed: {
    id() {
      return this.row[this.primaryKey]
    },
    resource() {
      return this.$route.params.resource as string
    },
    nRelations() {
      return this.row['count_parents'] + this.row['count_children']
    },
    currentVersion() {
      if (this.row['ts_end'] !== undefined) {
        const tsEnd = new Date(this.row['ts_end']).getTime()
        return new Date().getTime() < tsEnd
      } else {
        return true
      }
    }
  },
  methods: {
    getForeignKey(fieldKey: string) {
      return this.foreignKeys.find((fK) => fK.foreign_key == fieldKey)
    },
    getValue(column) {
      const foreignKey = this.getForeignKey(column)
      const value = getTableValue(foreignKey, this.row[column])
      const versionNumber = ['entity_evtp_version', 'entity_evtp_version_oe_com_type'].includes(
        column
      )
        ? this.row[column]['versie_nr']
        : 0
      const maxLength = 100

      // Helper function
      const formatPublicatiestatus = (val) => {
        if (['id_publicatiestatus'].includes(column)) {
          return getPublicatieStatus(val)
        }
        return val
      }

      // Helper function to format the value with version number
      const formatValueWithVersion = (val) => {
        if (versionNumber) {
          return `${val} `
        }
        return val
      }

      // Helper function to truncate the value if it exceeds the maximum length
      const truncateValue = (val) => {
        if (val.length > maxLength) {
          return `${val.substr(0, maxLength)}...`
        }
        return val
      }

      const valueFormatted = formatDateToLocale(column, value)
      const formattedValueWithVersion = formatValueWithVersion(valueFormatted)
      const formatted3 = formatPublicatiestatus(formattedValueWithVersion)
      return truncateValue(formatted3)
    },
    async deleteObject(id: string) {
      try {
        await axios.delete(`${store.state.APIurl}/${this.resource}/${id}`)
        this.$emit('relationUpdated')
        store.commit('activateSnackbar', {
          show: true,
          text: store.state.snackbar.succesfullDeletion,
          color: store.state.snackbar.succes_color
        })
      } catch (e) {
        store.commit('activateSnackbar', {
          show: true,
          text: store.state.snackbar.foreignKeyConstraints,
          color: store.state.snackbar.error_color
        })
      }
    }
  }
})
</script>

<style>
@import '/src/styles/styles.scss';
</style>
