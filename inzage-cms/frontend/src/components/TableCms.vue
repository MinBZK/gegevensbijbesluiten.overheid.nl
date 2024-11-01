<template>
  <v-container>
    <h1>{{ table?.label }}</h1>
    <v-container fill-height>
      <v-row justify="space-around" class="centered" no-gutters>
        <v-col cols="3" justify="center">
          <v-text-field
            v-model="searchFieldText"
            label="Zoeken"
            hide-details
            placeholder="..."
            variant="outlined"
            prepend-inner-icon="mdi-magnify"
            density="compact"
            append-inner-icon="mdi-magnify"
            @click:append-inner="onSearchClick"
            @keyup.enter="onSearchClick"
          />
        </v-col>
        <v-col cols="6">
          <v-pagination
            v-if="!loading"
            v-model="page"
            :length="nPages"
            prev-icon="mdi-menu-left"
            next-icon="mdi-menu-right"
            class="table-pagination"
          />
        </v-col>
        <v-col cols="3" justify="center">
          <v-btn
            elevation="0"
            tile
            color="primary"
            :to="{
              name: 'newEntityRecord',
              params: {
                recordResource: table?.resource,
                resource: $route.resource || table?.resource
              }
            }"
            @click="addNewRow"
          >
            <v-icon> mdi-plus-box-outline </v-icon>
            Toevoegen
          </v-btn>
        </v-col>
      </v-row>
    </v-container>
    <v-table>
      <thead v-if="tableModelLoaded">
        <tr>
          <th />
          <TableHeader
            v-for="header in includedFields"
            :key="header"
            :header="table?.columns[mappedFieldKeysForeignToOriginal[header]]"
            :values="getUniqueValues(header)"
            :label-key="getLabelKey(header)"
            :selected-filters="filters.find((f) => f.header == header)"
            @set-filter="(values) => setFilter(header, values)"
          />
        </tr>
      </thead>
      <tbody v-if="loading">
        <tr>
          <td :colspan="includedFields.length + 1" class="centered">
            <v-progress-circular indeterminate color="primary" />
          </td>
        </tr>
      </tbody>
      <tbody v-else-if="tableModelLoaded">
        <TableRow
          v-for="row in paginatedData"
          :key="row[primaryKey]"
          :row="row"
          :foreign-keys="tableModel.foreign_keys"
          :data-columns="includedFields"
          :primary-key="primaryKey"
          :id-publicatiestatus-bool="id_publicatiestatusBool"
          :versie-nr="row['versie_nr']"
          @row-selected="(id) => selectRow(id)"
          @relation-updated="getTableData"
        />
        <tr v-if="paginatedData.length == 0">
          <td :colspan="includedFields.length + 1" class="centered">
            Geen rijen gevonden voor de gekozen filters.
          </td>
        </tr>
      </tbody>
    </v-table>

    <v-dialog v-model="showErrorDialog" max-width="500">
      <v-card>
        <v-card-title>Foutmelding</v-card-title>
        <v-card-text>
          Het object kan niet worden verwerkt omdat de invoer incorrect of incompleet is.
        </v-card-text>
      </v-card>
    </v-dialog>
  </v-container>
  <router-view @record-updated=";[getTableData()]" />
</template>

<script lang="ts">
import axios from 'axios'
import { defineComponent } from 'vue'
import store from '@/store/index'
import { Table, TableModel } from '@/types/Tables'
import { tables } from '@/config/tables'
import { getPrimaryKey, getid_publicatiestatus, mapFieldKeys } from '@/util/misc'
import TableRow from '@/components/TableRow.vue'
import TableHeader from '@/components/TableHeader.vue'

export default defineComponent({
  name: 'TableCms',
  components: {
    TableRow,
    TableHeader
  },
  props: {
    resource: {
      type: String,
      required: true
    }
  },
  data() {
    const data: Array<object> = []
    const loading: boolean = true
    const showRow: boolean = false
    const selectedRowId: string | number | undefined = undefined
    const page: number = 1
    const pageLength: number = 10
    const dialog: boolean = false
    const filters: Array<{ header: string; values: Array<string> }> = []
    const showErrorDialog: boolean = false
    const error: string = ''
    const searchQuery: string = ''
    const searchFieldText: string = ''
    const initTableModel: TableModel = {
      primary_key: '',
      foreign_keys: [],
      fields: {},
      description_key: '',
      foreign_key_mapping: {},
      resource: ''
    }
    return {
      data,
      loading,
      showRow,
      selectedRowId,
      page,
      pageLength,
      dialog,
      filters,
      showErrorDialog,
      error,
      searchQuery,
      searchFieldText,
      initTableModel,
      tableModel: initTableModel,
      tableModelLoaded: false
    }
  },
  computed: {
    mappedFieldKeysOriginalToForeign() {
      return mapFieldKeys(this.tableModel, 'foreign')
    },
    mappedFieldKeysForeignToOriginal() {
      return mapFieldKeys(this.tableModel, 'original')
    },
    includedFields() {
      return Object.keys(this.table?.columns || [])
        .filter((header) => !this.table?.hiddenColumns.includes(header))
        .map((f) => this.mappedFieldKeysOriginalToForeign[f])
    },
    table() {
      const table: Table | undefined = tables.find((t) => t.resource == this.resource)
      return table
    },
    selectedRow() {
      const selectedRow = this.data.find((r) => r[this.primaryKey] == this.selectedRowId)
      return selectedRow
    },
    paginatedData() {
      if (this.searchFieldText) {
        if (this.nPages > 1) {
          return this.data.slice(this.pageLength * (this.page - 1), this.pageLength * this.page)
        } else {
          return this.data.slice(0, this.pageLength)
        }
      } else {
        return this.data.slice(this.pageLength * (this.page - 1), this.pageLength * this.page)
      }
    },
    paginatedEntityCodes() {
      return this.paginatedData.map((row) => row[this.primaryKey])
    },
    nPages() {
      return Math.ceil(this.data.length / this.pageLength)
    },
    primaryKey() {
      return getPrimaryKey(this.tableModel)
    },
    id_publicatiestatusBool() {
      return getid_publicatiestatus(this.tableModel)
    }
  },
  watch: {
    async searchQuery() {
      if (this.searchQuery) {
        this.loading = true
        this.page = 1
        const { data } = await axios.get(
          `${store.state.APIurl}/${this.resource}/filter/${this.searchFieldText}`
        )
        this.loading = false
        this.data = data
      } else {
        const { data } = await axios.get(`${store.state.APIurl}/${this.resource}/`)
        this.data = data
      }
    },
    resource: {
      handler() {
        this.init()
        this.resetSearchFieldText()
        this.resetPage()
      },
      immediate: true
    }
  },
  methods: {
    onSearchClick() {
      this.searchFieldText = this.searchFieldText
        .toString()
        .trim()
        /* eslint-disable no-useless-escape */
        .replace(/[@#$%^&*_+\=\[\]{};':"\\|,.<>\/]/g, '')

      this.searchQuery = this.searchFieldText
    },
    resetSearchFieldText() {
      this.searchFieldText = ''
      this.searchQuery = ''
    },
    resetPage() {
      this.page = 1
    },
    getLabelKey(column) {
      const foreignKey = this.tableModel.foreign_keys.find((fK) => fK.foreign_key == column)
      return foreignKey ? foreignKey.foreign_table.description_key : undefined
    },
    async getTableData() {
      const { data } = await axios.get(`${store.state.APIurl}/${this.resource}/`)
      this.data = data
    },
    async getTableModel() {
      try {
        this.tableModelLoaded = false
        const { data } = await axios.get(`${store.state.APIurl}/table/${this.resource}/model`)
        this.tableModel = data
        this.tableModelLoaded = true
      } catch (e) {
        console.error(e)
      }
    },
    selectRow(id) {
      this.selectedRowId = id
      this.showRow = true
    },
    addNewRow() {
      this.selectedRowId = undefined
      this.showRow = true
    },
    getUniqueValues(h) {
      const labelKey = this.getLabelKey(h)
      const uniqueLabels = [
        ...new Set(
          // get unique values based on the cell label to prevent duplicates
          this.data.map((row) => {
            const rowValue = row[h]
            return rowValue && labelKey ? rowValue[labelKey] : rowValue
          })
        )
      ]

      const uniqueValues = uniqueLabels.map((label) => {
        // retrieve original value based on the label
        if (labelKey) {
          const originalRow = this.data.find((row) => (row[h] ? row[h][labelKey] : row[h]) == label)
          return originalRow ? originalRow[h] : label
        } else {
          return label
        }
      })

      return uniqueValues
    },
    setFilter(header, values) {
      // Entering without values means the user likely wants to disable the filter instead.
      if (values.length == 0) {
        this.clearFilter(header)
        return
      }
      const existingFilter = this.filters.find((f) => f.header == header)
      if (existingFilter) {
        existingFilter.values = values
      } else {
        this.filters.push({
          header,
          values
        })
      }
      this.page = 1
    },
    clearFilter(header) {
      const existingFilter = this.filters.find((f) => f.header == header)
      if (existingFilter) {
        const existingFilterIndex = this.filters.indexOf(existingFilter)
        this.filters.splice(existingFilterIndex, 1)
      }
    },
    showError(e) {
      this.error = e
      this.showErrorDialog = true
    },
    async init() {
      this.loading = true
      this.tableModel = this.initTableModel
      this.data = []
      this.filters = []
      await Promise.all([this.getTableData(), this.getTableModel()])
      this.loading = false
    }
  }
})
</script>

<style>
@import '/src/styles/styles.scss';

.table-pagination .v-btn--disabled {
  visibility: visible !important;
}

.v-btn.table-button {
  padding-right: 10px !important;
  padding-left: 10px !important;
  min-width: 0 !important;
}
</style>
