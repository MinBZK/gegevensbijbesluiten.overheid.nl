<template>
  <v-row>
    <v-col>
      <v-autocomplete
        v-if="foreignResourceModel"
        v-model="selectedForeignRecord"
        :items="recordsList"
        :loading="loading"
        :label="`Selecteer: ${label || fieldKey}` + (required ? ' (verplicht)' : '')"
        :disabled="disableEvtp"
        density="comfortable"
        variant="outlined"
        return-object
        clearable
        hide-no-data
      />
      <v-select
        v-else-if="fieldKey === 'koepel'"
        v-model="selectedKoepel"
        :items="koepelOptions"
        :disabled="disableEvtp"
        :label="(label || fieldKey) + (required ? ' (verplicht)' : '')"
        density="comfortable"
        variant="outlined"
      />
      <v-textarea
        v-else-if="fieldKey == 'versie_nr'"
        :model-value="getModelValue()"
        :label="(label || fieldKey) + (required ? '' : '')"
        density="compact"
        persistent-hint
        variant="outlined"
        persistent-placeholder
        disabled
        rows="1"
      />
      <v-select
        v-else-if="fieldKey === 'id_publicatiestatus'"
        v-model="selectedIdPublicatiestatus"
        :label="(label || fieldKey) + (required ? ' (verplicht)' : '')"
        density="comfortable"
        variant="outlined"
        disabled
      />
      <v-textarea
        v-else
        :key="fieldKey"
        :counter="maximumValueLength"
        :rules="rules"
        :label="(label || fieldKey) + (required ? ' (verplicht)' : '')"
        :model-value="getModelValue()"
        :disabled="readonly || disableEvtp"
        density="compact"
        persistent-hint
        filled
        variant="outlined"
        persistent-placeholder
        rows="1"
        auto-grow
        @update:model-value="
          (v) => [(value = v), !v && isIntegerKey ? $emit('update', null) : $emit('update', v)]
        "
      />
    </v-col>
    <v-col cols="3" class="mt-1">
      <v-btn
        v-if="foreignResourceModel && value && foreignKey && foreignResourceInClient"
        size="small"
        icon="mdi-link"
        variant="outlined"
        color="primary"
        class="px-0"
        :to="{
          name: 'entityRecord',
          params: {
            tab: 'data',
            recordResource: foreignResourceModel.resource,
            id: value[foreignKey.foreign_table.primary_key]
          },
          query: {
            redirect: $route.fullPath
          }
        }"
      />
    </v-col>
  </v-row>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import type { PropType } from 'vue'
import axios from 'axios'
import { TableModelColumn, TableModelForeignKey } from '@/types/Tables'
import store from '@/store/index'
import { getTableValue, getTableKey, formatDateToLocale } from '@/util/misc'
import { getPublicatieStatus } from '@/types/PublicatieStatus'
import { tables } from '@/config/tables'

export default defineComponent({
  name: 'EntityRecordDataField',
  props: {
    label: {
      type: undefined,
      required: true
    },
    fieldKey: {
      type: String,
      required: true
    },
    originalKey: {
      type: String,
      required: true
    },
    initialValue: {
      type: [String, Number, Array, Object, Boolean],
      default: null,
      required: false
    },
    tableName: {
      type: String,
      required: true
    },
    modelColumns: {
      type: Object as PropType<TableModelColumn>,
      default: () => {},
      required: false
    },
    readonly: {
      type: Boolean,
      required: true
    },
    fieldProperties: {
      type: Object,
      default: () => {},
      required: false
    },
    foreignKey: {
      type: Object as PropType<TableModelForeignKey>,
      default: () => {},
      required: false
    },
    required: {
      type: Boolean,
      required: true
    },
    dataType: {
      type: String,
      required: true
    },
    disableEvtp: {
      type: Boolean,
      required: true
    },
    ggCdParent: {
      type: String,
      default: null,
      required: false
    }
  },
  emits: ['update'],
  data() {
    return {
      value: '' as string,
      rules: [
        (v) => (this.required && !v ? 'Verplicht veld' : true),
        (v) => (this.isIntegerKey && !/^\d*$/.test(v) && v ? 'Voer een geldig getal in' : true),
        (v) =>
          v && v.length >= (this.fieldProperties?.max_length || 1000)
            ? 'Maximum aan karakters is bereikt'
            : true,
        (v) =>
          [
            're_link',
            'link',
            'uri',
            'overige_informatie_link',
            'ext_lnk_aut',
            'internet_domein'
          ].includes(this.fieldKey) && !/^(ftp|http|https):\/\/[^ "]+$/.test(v.trim())
            ? 'Voer een geldige URL in de vorm van https://...'
            : true
      ],
      fieldValueOptions: [] as Array<object>,
      loading: true as boolean,
      records: [] as Array<object>,
      selectedForeignRecord: '' as string,
      koepelOptions: ['Ja', 'Nee'],
      selectedKoepel: '' as string,
      selectedIdPublicatiestatus: '' as string
    }
  },
  computed: {
    store() {
      return store
    },
    isIntegerKey() {
      return !!(
        this.dataType == 'integer' ||
        this.dataType == 'bigint' ||
        this.dataType == 'smallint'
      )
    },
    foreignResource() {
      return this.foreignKey ? this.foreignKey.foreign_resource : null
    },
    maximumValueLength() {
      return this.fieldProperties ? this.fieldProperties.max_length || 1000 : null
    },
    foreignResourceModel() {
      return this.foreignKey?.foreign_table
    },
    foreignResourceInClient() {
      const resources = tables.map((t) => t.resource)
      return this.foreignResource ? resources.includes(this.foreignResource) : false
    },
    primaryKey() {
      return this.foreignKey?.foreign_table.primary_key || ''
    },
    descriptionKey() {
      return this.foreignKey?.foreign_table.description_key || ''
    },
    recordsList() {
      if (this.records.some((r) => 'versie_nr' in r)) {
        return this.records.map(
          (r) => `${r[this.descriptionKey]} (${r[this.primaryKey]}) versie: ${r['versie_nr']}`
        )
      } else {
        return this.records.map((r) => `${r[this.descriptionKey]} (${r[this.primaryKey]})`)
      }
    }
  },
  watch: {
    selectedKoepel() {
      if (this.selectedKoepel === 'Ja') {
        this.$emit('update', true)
      } else if (this.selectedKoepel === 'Nee') {
        this.$emit('update', false)
      }
    },
    selectedForeignRecord() {
      const selectedForeignRecordObject = Object.assign(
        {},
        this.records.some((r) => 'versie_nr' in r)
          ? this.records.filter(
              (r) =>
                `${r[this.descriptionKey]} (${r[this.primaryKey]}) versie: ${r['versie_nr']}` ===
                this.selectedForeignRecord
            )
          : this.records.filter(
              (r) =>
                `${r[this.descriptionKey]} (${r[this.primaryKey]})` === this.selectedForeignRecord
            )
      )[0]
      selectedForeignRecordObject
        ? this.$emit('update', selectedForeignRecordObject)
        : this.$emit(
            'update',
            this.records.filter((r) => r[this.descriptionKey] == this.selectedForeignRecord)[0]
          )
    },
    value() {
      const maxLength = this.maximumValueLength
      if (this.value && this.value.length >= maxLength) {
        this.value = this.value.substring(0, maxLength)
      }
    },
    initialValue: {
      handler() {
        // @ts-ignore
        this.value = this.initialValue
        // @ts-ignore
        this.selectedValue = this.value
        this.setSelectedKoepel()
        this.setSelectedidPublicationStatus()
      },
      immediate: true
    },
    selectedValue(v) {
      this.$emit('update', v)
    }
  },
  async created() {
    await this.updateForeignRecord()
  },
  methods: {
    setSelectedKoepel() {
      if (this.fieldKey === 'koepel') {
        this.selectedKoepel = this.initialValue == null ? '' : this.initialValue ? 'Ja' : 'Nee'
      }
    },
    setSelectedidPublicationStatus() {
      if (this.fieldKey === 'id_publicatiestatus') {
        const statusNumber = this.initialValue as number
        this.selectedIdPublicatiestatus = getPublicatieStatus(statusNumber)
      }
    },
    async updateForeignRecord() {
      if (this.foreignResource) {
        await this.getData()
      }
      if (this.records.length > 0) {
        const modelValue = this.getModelValue()
        if (modelValue) {
          const version = this.initialValue['versie_nr']
            ? ` versie: ${this.initialValue['versie_nr']}`
            : ''
          this.selectedForeignRecord = `${modelValue} (${this.getModelKey()})${version}`
        } else {
          this.selectedForeignRecord = ''
        }
      }
    },
    async getFieldValueOptions() {
      if (this.foreignKey) {
        const { data } = await axios.get(
          `${store.state.APIurl}/table/${this.foreignKey.foreign_table.resource}/field/${this.fieldKey}`
        )
        this.fieldValueOptions = data.data
      }
    },
    getModelValue() {
      const recordDataFormatted = formatDateToLocale(this.fieldKey, this.value)
      return getTableValue(this.foreignKey, recordDataFormatted)
    },
    getModelKey() {
      return getTableKey(this.foreignKey, this.value)
    },
    async getData() {
      let target = this.foreignResource
      if (this.originalKey == 'gg_cd_sup') {
        target = 'gg/gg-sup'
      } else if (this.originalKey == 'gg_cd_sub') {
        target = 'gg-koepel/gg-sub'
      }
      if (this.ggCdParent) {
        target = `gg/gg-sub-filtered-${this.ggCdParent}`
      }
      const { data } = await axios.get(`${store.state.APIurl}/${target}-list/`)
      this.records = data
      this.loading = false
    }
  }
})
</script>

<style lang="scss">
@import '/src/styles/styles.scss';

.required-text-field {
  font-weight: bold;
}
</style>
