<template>
  <v-row v-if="disableEvtp">
    <v-alert
      type="warning"
      dismissible
      elevation="2"
      class="mt-2"
    >
      <strong>Let op!</strong> Dit besluit is inmiddels gepubliceerd of
      verouderd en kan niet meer worden gewijzigd.
    </v-alert>
  </v-row>
  <v-row class="py-1">
    <v-col>
      <v-card-subtitle class="text-h7">
        <strong>{{ title }}</strong>
        <br><br>
        <v-select
          v-if="isEvtp"
          v-model="selectedVersion"
          :items="versionList"
          label="Selecteer versie"
          :item-value="null"
          :item-text="null"
          density="compact"
          filled
          variant="outlined"
          no-data-text="Geen versies beschikbaar"
        />
      </v-card-subtitle>
    </v-col>
  </v-row>
  <div
    v-show="tabs.filter((t) => t.show).length > 1"
    v-if="recordLoaded"
    background-color="secondary"
  >
    <v-tabs
      v-model="activeTab"
      color="primary"
    >
      <v-tab
        v-for="t in tabs"
        v-show="t.show"
        :key="t.key"
        height="48px"
        :color="activeTab === t.key ? 'secondary' : undefined"
        :to="{
          params: { tab: t.key },
        }"
      >
        {{ t.label }}
      </v-tab>
    </v-tabs>
  </div>
  <v-divider />
  <template v-if="selectedTab && selectedTab.key == 'data' && selectedTab.show">
    <EntityRecordData
      v-if="(isNewRow || recordLoaded) && modelLoaded && table"
      :table="table"
      :record="record"
      :table-model="tableModel"
      :primary-key="primaryKey"
      :is-new-row="isNewRow"
      :evtp-cd="evtpCd"
      :gst-cd="gstCd"
      :struct-cd="structCd"
      :struct-relation="structRelation"
      :versie-nr="versieNr"
      :disable-evtp="disableEvtp"
      @close="() => $emit('close')"
      @confirm="(payload, files) => upsert(record[primaryKey], payload, files)"
    />
  </template>
  <template v-else-if="table && table.label == 'Besluiten'">
    <EvtpStructureOverview
      :evtp-cd="id"
      :record="record"
      :record-loaded="recordLoaded"
      :resource="resource"
      :versie-nr="selectedVersion"
      :disable-evtp="disableEvtp"
    />
  </template>
  <template v-else-if="selectedTab && selectedTab.show">
    <EntityRecordRelations
      v-if="recordLoaded && modelLoaded && table"
      :primary-key="primaryKey"
      :record="record"
      :resource="table.resource"
      :foreign-keys="tableModel.foreign_keys"
      :description-key="tableModel.description_key"
      @relation-updated="() => getRecord(id, resource, true)"
      @close="() => $emit('close')"
    />
  </template>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import { TableModel, Table } from '@/types/Tables'
import EntityRecordRelations from '@/components/EntityRecordRelations.vue'
import EvtpStructureOverview from '@/components/EvtpStructure/EvtpStructureOverview.vue'
import EntityRecordData from '@/components/EntityRecordData.vue'
import store from '@/store/index'
import axios from 'axios'
import { getPrimaryKey } from '@/util/misc'
import { tables } from '@/config/tables'

export default defineComponent({
  name: 'EntityRecord',
  components: {
    EntityRecordRelations,
    EvtpStructureOverview,
    EntityRecordData,
  },
  props: {
    resource: {
      type: String,
      required: true,
    },
    id: {
      type: [String, Number],
      required: false,
      default: null,
    },
    tab: {
      type: String,
      default: null,
      required: false,
    },
    gstCd: {
      type: String,
      default: null,
      required: false,
    },
    evtpCd: {
      type: String,
      default: null,
      required: false,
    },
    structCd: {
      type: String,
      default: null,
      required: false,
    },
    structRelation: {
      type: String,
      default: null,
      required: false,
    },
    versieNr: {
      type: String,
      default: null,
      required: false,
    },
  },
  emits: ['close', 'confirm', 'error', 'recordUpdated'],
  data() {
    return {
      dialog: true,
      record: {} as object,
      tableModel: {
        primary_key: '',
        resource: '',
        foreign_keys: [],
        fields: {},
        input_schema: null,
        description_key: '',
        foreign_key_mapping: {},
      } as TableModel,
      evtp_gst_model: {
        evtp_cd: null,
        versie_nr: null,
        gst_cd: null as number | null,
      },
      recordLoaded: false as boolean,
      modelLoaded: false as boolean,
      relations: '' as string,
      files: [],
      evtpVersions: [] as Array<number>,
      selectedVersion: this.versieNr,
      newId: null as number | null,
      dataPostPut: {} as object,
      activeTab: null,
      succesUpload: true as boolean,
    }
  },
  computed: {
    disableEvtp() {
      return (
        this.record['id_publicatiestatus'] == 3 && !this.isDuplicateEvtpVersion ||
        this.record['versie_nr'] < this.versieNr && !this.isDuplicateEvtpVersion
      )
    },
    table() {
      const table: Table | undefined = tables.find(
        (t) => t.resource == this.resource
      )
      return table
    },
    tabs() {
      const countRelations = this.record
        ? (this.record['child_entities'] || []).length +
        (this.record['parent_entities'] || []).length +
        (this.record['count_evtp_gst'] || [])
        : 0
      const tabs: Array<{ key: string; label: string; show: boolean }> = [
        { key: 'data', label: 'Data', show: true },
        {
          key: 'relations',
          label: `Relaties (${countRelations})`,
          show: !!this.record['parent_entities'] || !!this.record['child_entities'],
        },
      ]
      return this.isNewRow ? tabs.slice(0, 1) : tabs
    },
    selectedTab() {
      return this.tabs.find((t) => t.key == this.tab) || this.tabs[0]
    },
    primaryKey() {
      return getPrimaryKey(this.tableModel)
    },
    title() {
      if (this.isNewGSTRelation) {
        return `Toevoegen nieuwe relatie onder besluit: ${this.record['evtp_nm']}`
      } else if (this.isNewGGRelation) {
        return `Toevoegen nieuwe relatie gst: ${this.record['omschrijving']}`
      } else if (this.isDuplicateEvtpVersion) {
        return `Duplicaat van dit besluit aanmaken`
      } else if (
        !this.isNewRow &&
        !this.isNewGGRelation &&
        !this.isNewGSTRelation &&
        !this.isNewVersion
      ) {
        return this.tableModel.description_key
          ? `Wijzigen: ${this.record[this.tableModel.description_key]}`
          : 'Wijzigen koppeling'
      } else if (this.isNewVersion) {
        return `Nieuwe versie aanmaken`
      } else {
        return 'Toevoegen'
      }
    },
    isNewRow() {
      return !this.id
    },
    isNewVersion() {
      return this.tab == 'new-version-data'
    },
    adjustCurrentVersion() {
      return this.tab == 'adjust-version-data'
    },
    isDuplicateEvtpVersion() {
      return this.tab == 'duplicate-evtp-data'
    },
    isNewGSTRelation() {
      if ((this.evtpCd) && this.resource == 'gst') {
        this.getRecord(this.evtpCd, 'evtp-version', true)
        return true
      } else {
        return false
      }
    },
    isNewONDRelation() {
      if (this.resource == 'evtp-ond') {
        this.getRecord(this.evtpCd, 'evtp-version', true)
        return true
      } else {
        return false
      }
    },
    isNewGGRelation() {
      if (this.gstCd) {
        this.getRecord(this.gstCd, 'gst', true)
        return true
      } else {
        return false
      }
    },
    versionList() {
      return this.evtpVersions.map((version) => version)
    },
    isEvtp() {
      return this.resource == 'evtp-version'
    },
  },
  watch: {
    resource() {
      this.modelLoaded = false
      this.getTableModel()
      if (this.$route.params.tab) this.getRecord(this.id, this.resource, true)
    },
    id() {
      this.recordLoaded = false
      if (this.id) this.getRecord(this.id, this.resource, true)
    },
    async selectedVersion() {
      if (this.tab === 'relations') {
        if (this.selectedVersion) {
          await this.fetchRelations(this.resource, this.id, this.selectedVersion)
        }
        else {
          await this.fetchRelations(this.resource, this.id, this.versieNr)
        }
      } else if (this.resource === 'evtp-version' && !this.isNewVersion) {
        const { data } = await axios.get(
          `${store.state.APIurl}/${this.resource}/${this.id}/${this.selectedVersion}`
        )
        this.record = data
        this.recordLoaded = true
      }
    },
  },
  async created() {
    // In case of adjusting existing record or evtp-structure
    if (this.isNewVersion) {
      this.getRecordVersion(this.id, this.versieNr)
    } else if (!this.isNewRow || this.tab == 'relations') {
      this.getRecord(this.id, this.resource, true)
    } else {
      this.recordLoaded = true
    }
    this.getTableModel()
  },
  methods: {
    async getVersions(primaryKey: number) {
      this.selectedVersion = this.record['versie_nr']
      const { data } = await axios.get(
        `${store.state.APIurl}/${this.resource}-versions/${primaryKey}`
      )
      this.evtpVersions = data
    },
    //@ts-ignore
    async getRecordVersion(primaryKey: any, versieNr: int) {
      const endpoint = `${store.state.APIurl}/${this.resource}/${primaryKey}/${versieNr - 1
        }`
      const { data } = await axios.get(endpoint)
      this.record = data
      this.record['id_publicatiestatus'] = 1
      this.record['versie_nr'] = this.versieNr
      this.selectedVersion = this.versieNr
      this.recordLoaded = true
    },
    async fetchRelations(inputResource: string, primaryKey: string | number, versieNr: string) {
      const endpoint = `${store.state.APIurl}/${inputResource}/relations/${primaryKey}/${versieNr}`
      const { data } = await axios.get(endpoint)
      this.record = data
      this.recordLoaded = true
    },
    async getRecord(
      primaryKey: any,
      inputResource: string,
      relationRow = true as boolean
    ) {
      if (this.resource == 'evtp-version' && relationRow && this.tab == 'relations') {
        await this.fetchRelations(inputResource, primaryKey, this.versieNr)
        await this.getVersions(Number(this.id))
      } else if (
        this.resource == 'evtp-version' &&
        Number(this.versieNr) &&
        !this.isNewVersion
      ) {
        const endpoint = `${store.state.APIurl}/${this.resource}/${primaryKey}/${this.versieNr}`
        const { data } = await axios.get(endpoint)
        this.record = data
        this.recordLoaded = true
        await this.getVersions(primaryKey)
      } else {
        const endpoint = `${store.state.APIurl}/${inputResource}/${primaryKey}`
        const { data } = await axios.get(endpoint)
        this.record = data
        this.recordLoaded = true
      }
    },
    //@ts-ignore
    async getTableModel(inputResource = this.resource) {
      const { data } = await axios.get(
        `${store.state.APIurl}/table/${inputResource}/model`
      )
      this.tableModel = data
      this.modelLoaded = true
    },
    async uploadFiles(files, data) {
      this.files = files
      const formData = new FormData()
      this.$data.files.forEach((file) => {
        formData.append('documents', file)
      })
      const headers = {
        'Content-Type': 'multipart/form-data',
      }
      await axios
        .post(
          `${store.state.APIurl}/evtp-acc/upload-files/${data['evtp_cd']}/${data['oe_cd']}/${data['volg_nr']}/${data['bestand_acc_cd']}`,
          formData,
          {
            headers: headers,
          }
        )
        .then((response) => {
          console.log(response)
        })
        .catch((error) => {
          if (error.response.status === 422) {
            store.commit('activateSnackbar', {
              show: true,
              text: store.state.snackbar.malwareDetected,
              color: store.state.snackbar.error_color,
            })
          } else if (error.response.status === 415) {
            store.commit('activateSnackbar', {
              show: true,
              text: store.state.snackbar.wrongFileExtension,
              color: store.state.snackbar.error_color,
            })
          } else {
            console.error(error)
          }
          this.succesUpload = false
          console.log('error')
        })
    },
    async upsert(id, payload, files) {
      const isNewRecord = !id
      const baseEndpoint = isNewRecord
        ? `${store.state.APIurl}/${this.resource}/`
        : `${store.state.APIurl}/${this.resource}`
      const endpoint = isNewRecord ? baseEndpoint : `${baseEndpoint}/${id}`

      try {
        if (this.isNewVersion && this.resource == 'evtp-version') {
          const { data } = await axios.post(
            `${store.state.APIurl}/${this.resource}-version/${this.id}`,
            payload
          )
          this.newId = data[this.primaryKey]
        }
        else if (this.isDuplicateEvtpVersion && this.resource == 'evtp-version') {
          const { data } = await axios.post(
            `${store.state.APIurl}/${this.resource}-duplicate/${this.id}`,
            payload
          )
          this.newId = data[this.primaryKey]
        } else {
          const method = isNewRecord ? 'POST' : 'PUT'
          const { data } = await axios({
            method,
            url: endpoint,
            data: payload,
          })
          this.newId = data[this.primaryKey]
          this.dataPostPut = data
        }

        this.$emit('recordUpdated')
        this.$emit('close')

        const hasRedirect = this.$route.query.redirect
        if (files.length > 0) {
          this.uploadFiles(files, this.dataPostPut)
        }
        // For creating a new record
        if (
          id !== this.newId &&
          !this.isNewGSTRelation &&
          !this.isNewGGRelation
        ) {
          if (this.succesUpload) {
            store.commit('activateSnackbar', {
              show: true,
              text: store.state.snackbar.succesfullAdditions,
              color: store.state.snackbar.succes_color,
            })
          }
          // For updating a record
        } else if (
          hasRedirect &&
          !this.isNewGSTRelation &&
          !this.isNewGGRelation
        ) {
          this.$emit('confirm')
          if (this.succesUpload) {
            store.commit('activateSnackbar', {
              show: true,
              text: store.state.snackbar.succesfullMutations,
              color: store.state.snackbar.succes_color,
            })
          }
          // For adding a new gst relation
        } else if (this.isNewGSTRelation) {
          this.evtp_gst_model.evtp_cd = this.record['evtp_cd']
          this.evtp_gst_model.versie_nr = this.record['versie_nr']
          this.evtp_gst_model.gst_cd = this.newId
          const endpoint_evtp_gst = `${store.state.APIurl}/evtp-gst/`
          await axios.post(endpoint_evtp_gst, this.evtp_gst_model)

          if (this.succesUpload) {
            store.commit('activateSnackbar', {
              show: true,
              text: store.state.snackbar.succesfullAdditions,
              color: store.state.snackbar.succes_color,
            })
          }
        } else {
          if (this.id) await this.getRecord(this.id, this.resource, false)
          this.$emit('confirm')
          if (this.succesUpload) {
            store.commit('activateSnackbar', {
              show: true,
              text: store.state.snackbar.succesfullMutations,
              color: store.state.snackbar.succes_color,
            })
          }
        }
      } catch (error) {
        this.$emit('error', error)
      }
    },
  },
})
</script>

<style lang="scss">
@import '/src/styles/styles.scss';

.alert {
  color: red;
}
</style>
