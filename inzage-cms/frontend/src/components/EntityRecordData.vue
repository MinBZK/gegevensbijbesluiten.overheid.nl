<template>
  <v-card-text class="form-container">
    <entity-record-data-field
      v-for="fieldKey in includedFields"
      :key="fieldKey"
      :field-key="fieldKey"
      :original-key="originalFieldKeys[fieldKey]"
      :label="table.columns[originalFieldKeys[fieldKey]]"
      :initial-value="inputValue[fieldKey]"
      :table-name="table.label"
      :field-properties="tableModel.fields[fieldKey]"
      :foreign-key="getForeignKey(fieldKey)"
      :resource="table.resource"
      :required="isRequired(originalFieldKeys[fieldKey])"
      :readonly="isReadonly(originalFieldKeys[fieldKey])"
      :new-relationevtp="evtpTree"
      :data-type="getDataType(originalFieldKeys[fieldKey])"
      :disable-evtp="disableEvtp"
      :gg-cd-parent="ggCdParent"
      @update="(foreignKeyObject) => updateRecord(fieldKey, foreignKeyObject)"
    />
    <template v-if="table.resource == 'evtp-acc'">
      <v-row>
        <v-divider />
        <v-card-title> Bijlage </v-card-title>
      </v-row>
      <v-row>
        <v-col>
          <v-form v-model="isFormValid">
            <v-file-input
              v-model="files"
              counter
              multiple
              show-size
              small-chips
              density="compact"
              accept=".pdf"
              label="Voer bestand(en) in"
              :rules="fileInputRules"
            />
          </v-form>
        </v-col>
      </v-row>
      <v-row v-for="(file, index) in list_files" :key="index">
        <v-col>
          <table>
            <tr style="color: #01689b; text-decoration: underline" @click="() => getFiles(file)">
              {{
                file
              }}
            </tr>
          </table>
        </v-col>
        <v-col cols="3">
          <v-btn
            size="small"
            icon="mdi-download"
            variant="outlined"
            color="primary"
            class="px-0 mr-2"
            @click="() => getFiles(file)"
          />
          <v-btn
            size="small"
            icon="mdi-delete"
            variant="outlined"
            color="red"
            class="px-0 mr-2"
            @click="() => removeFiles(file)"
          />
        </v-col>
      </v-row>
    </template>
  </v-card-text>
  <v-divider />
  <v-card-actions>
    <v-spacer />
    <v-btn color="primary" @click="() => $emit('close')"> Annuleren </v-btn>
    <v-btn
      color="primary"
      :disabled="invalidFields.length > 0"
      @click="() => $emit('confirm', adjustedRecord, files)"
    >
      {{ evtpTree ? 'Toevoegen nieuwe relatie' : isNewRow ? 'Toevoegen' : 'Opslaan' }}
    </v-btn>
  </v-card-actions>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import type { PropType } from 'vue'
import axios from 'axios'
import EntityRecordDataField from '@/components/EntityRecordDataField.vue'
import { Table, TableModel } from '@/types/Tables'
import { mapFieldKeys } from '@/util/misc'
import store from '@/store/index'

export default defineComponent({
  name: 'EntityRecordData',
  components: { EntityRecordDataField },
  props: {
    table: {
      type: Object as PropType<Table>,
      required: true
    },
    record: {
      type: Object,
      default: () => {}
    },
    tableModel: {
      type: Object as PropType<TableModel>,
      required: true,
      default: () => {
        return {
          foreign_keys: [],
          primary_key: undefined,
          columns: []
        }
      }
    },
    primaryKey: {
      type: String,
      required: true
    },
    isNewRow: {
      type: Boolean,
      required: true
    },
    evtpCd: {
      type: String,
      default: null,
      required: false
    },
    gstCd: {
      type: String,
      default: null,
      required: false
    },
    structCd: {
      type: String,
      default: null,
      required: false
    },
    structRelation: {
      type: String,
      default: null,
      required: false
    },
    versieNr: {
      type: String,
      default: null,
      required: false
    },
    oeBestCd: {
      type: String,
      default: null,
      required: false
    },
    ggCdParent: {
      type: String,
      default: null,
      required: false
    },
    disableEvtp: {
      type: Boolean,
      default: false,
      required: false
    }
  },
  emits: ['close', 'confirm'],
  data() {
    return {
      adjustedRecord: {} as object,
      evtpTree: false as boolean,
      inputValue: this.evtpCd || this.gstCd ? {} : (this.record as {}),
      isFormValid: false,
      files: [],
      list_files: [],
      fileInputRules: [
        (files: any) =>
          files.reduce((sum: number, current: any) => sum + current.size, 0) < 20000000 ||
          'Upload maximaal 20 MB aan bestanden per keer.'
      ],
      tableModelUpdated: this.tableModel
    }
  },
  computed: {
    includedFields() {
      return this.getFieldOrder()
    },
    allFields() {
      return Object.keys(this.tableModelUpdated.fields)
    },
    inputFields() {
      return this.allFields.filter((h) => !this.tableModelUpdated.fields[h]['readonly'])
    },
    originalFieldKeys() {
      return mapFieldKeys(this.tableModelUpdated, 'original')
    },
    invalidFields() {
      return this.includedFields.filter((f) => {
        const originalFieldKey = this.originalFieldKeys[f]
        const fieldValue = this.adjustedRecord[originalFieldKey]
        const hasValue = fieldValue !== undefined && fieldValue !== null && fieldValue !== ''
        const validValue = this.isRequired(originalFieldKey) ? hasValue : true
        return !validValue
      })
    }
  },
  watch: {
    record: {
      handler() {
        this.inputValue = this.record
        // prefill evtp in evtp-ond
        if (
          this.evtpCd &&
          (this.table.resource == 'evtp-ond' || this.table.resource == 'evtp-oe-com-type')
        ) {
          this.inputValue = {}
          this.inputValue['evtp_cd'] = this.evtpCd
          this.inputValue['versie_nr'] = this.versieNr
          this.tableModelUpdated.fields['evtp_cd']['readonly'] = true
          this.tableModelUpdated.foreign_key_mapping['evtp_cd'] = ''
          this.tableModelUpdated.foreign_key_mapping['versie_nr'] = ''
          this.adjustedRecord['evtp_cd'] = this.evtpCd
          this.adjustedRecord['versie_nr'] = this.versieNr
        } else if (this.evtpCd && this.oeBestCd) {
          this.inputValue = {}
          this.inputValue['oe_best'] = this.oeBestCd
          this.tableModelUpdated.fields['oe_best']['readonly'] = true
          this.tableModelUpdated.foreign_key_mapping['oe_best'] = ''
          this.adjustedRecord['oe_best'] = this.oeBestCd
        } else if (this.evtpCd) {
          this.inputValue = ''
          this.evtpTree = true
        } else if (this.gstCd) {
          this.evtpTree = true
          this.inputValue = {}
          this.inputValue['gst_cd'] = this.gstCd
          this.inputValue['versie_nr'] = this.versieNr
          this.tableModelUpdated.fields['gst_cd']['readonly'] = true
          this.tableModelUpdated.foreign_key_mapping['gst_cd'] = ''
          this.tableModelUpdated.foreign_key_mapping['versie_nr'] = ''
          this.adjustedRecord['gst_cd'] = this.gstCd
          this.adjustedRecord['versie_nr'] = this.versieNr
        } else if (this.structCd) {
          const inputField = {
            OE: { parent: 'oe_koepel_cd', child: 'oe_cd' },
            GG: { parent: 'gg_cd_sup', child: 'gg_cd_sub' }
          }
          const inputObject = this.tableModelUpdated.resource == 'gg-struct' ? 'GG' : 'OE'
          this.inputValue = {}
          const childField = inputField[inputObject]['child']
          if (this.structRelation == 'parents') {
            this.inputValue[childField] = this.structCd
            this.tableModelUpdated.fields[childField]['readonly'] = true
            this.tableModelUpdated.foreign_key_mapping[childField] = ''
            this.adjustedRecord[childField] = this.structCd
          } else if (this.structRelation == 'oe-koepel') {
            this.inputValue[childField] = this.structCd
            this.tableModelUpdated.fields[childField]['readonly'] = true
            this.tableModelUpdated.foreign_key_mapping[childField] = ''
            this.adjustedRecord[childField] = this.structCd
          } else if (this.structRelation == 'oe-koepel-oe') {
            const parentField = inputField[inputObject]['parent']
            this.inputValue[parentField] = this.structCd
            this.tableModelUpdated.fields[parentField]['readonly'] = true
            this.tableModelUpdated.foreign_key_mapping[parentField] = ''
            this.adjustedRecord[parentField] = this.structCd
          } else {
            const parentField = inputField[inputObject]['parent']
            this.inputValue[parentField] = this.structCd
            this.tableModelUpdated.fields[parentField]['readonly'] = true
            this.tableModelUpdated.foreign_key_mapping[parentField] = ''
            this.adjustedRecord[parentField] = this.structCd
          }
        } else {
          this.adjustedRecord = {}
          this.inputFields.forEach((f) => {
            this.adjustedRecord[f] = this.inputValue[f] || null
          })
          if (this.table.resource == 'evtp-acc') {
            this.tableModelUpdated.fields['oe_cd']['readonly'] = true
            this.tableModelUpdated.foreign_key_mapping['oe_cd'] = ''
          }
        }
      },
      immediate: true
    }
  },
  created() {
    if (this.table.resource === 'evtp-acc' && Object.values(this.record).length > 0) {
      this.getFileNames()
    }
  },
  methods: {
    async getFileNames() {
      await axios({
        url: `${store.state.APIurl}/evtp-acc/get-filenames/${this.record[this.primaryKey]}`,
        method: 'GET'
      })
        .then((response) => {
          this.list_files = response.data
        })
        .catch((error) => {
          console.log(error)
        })
    },
    async getFiles(file: string) {
      await axios({
        url: `${store.state.APIurl}/evtp-acc/get-files/${file}`,
        method: 'GET',
        responseType: 'blob'
      })
        .then((response) => {
          const fileURL = window.URL.createObjectURL(new Blob([response.data]))
          const fURL = document.createElement('a')

          fURL.href = fileURL
          fURL.setAttribute('download', `${file}.pdf`)
          document.body.appendChild(fURL)

          fURL.click()
        })
        .catch((error) => {
          console.log(error)
        })
    },
    async removeFiles(file: string) {
      await axios({
        url: `${store.state.APIurl}/evtp-acc/delete-files/${file}`,
        method: 'DELETE'
      }).catch((error) => {
        console.log(error)
      })
      this.getFileNames()
    },
    getFieldOrder() {
      let orderedHeaders: string[]
      if (this.table.fieldOrder.length === 0) {
        orderedHeaders = Object.keys(this.originalFieldKeys)
      } else {
        orderedHeaders = this.table.fieldOrder.map(
          (originalKey) => this.tableModelUpdated.foreign_key_mapping[originalKey] || originalKey
        )
      }
      return orderedHeaders
    },
    getForeignKey(fieldKey: string) {
      return this.tableModelUpdated.foreign_keys.find((fK) => fK.foreign_key == fieldKey)
    },
    mapForeignKeyToOriginalKey(foreignKey: string) {
      const mappedFields = Object.keys(this.tableModelUpdated.foreign_key_mapping).filter(
        (mappedKey) => this.tableModelUpdated.foreign_key_mapping[mappedKey] == foreignKey
      )
      return mappedFields[0]
    },
    updateRecord(fieldKey: string, foreignKeyObject: any) {
      // update foreign key column if the key is a related column
      const mappedFields = Object.values(this.tableModelUpdated.foreign_key_mapping)
      const isMappedField = mappedFields.includes(fieldKey)
      if (isMappedField) {
        const originalKey = this.mapForeignKeyToOriginalKey(fieldKey)
        const foreignKey = this.getForeignKey(fieldKey)
        if (foreignKey?.foreign_resource == 'omg' && !foreignKeyObject) {
          // field omg may have null values
          this.adjustedRecord[originalKey] = null
        }
        if (foreignKey && foreignKeyObject) {
          const foreignId = foreignKeyObject
            ? foreignKeyObject[foreignKey.foreign_table.primary_key]
            : null
          this.adjustedRecord[originalKey] = foreignId
          if (
            foreignKey.foreign_resource == 'evtp-version' ||
            (foreignKey.foreign_resource == 'gst' && this.tableModel.resource != 'evtp-gst')
          ) {
            this.adjustedRecord['versie_nr'] = foreignKeyObject.versie_nr
          }
          if (
            foreignKey.foreign_resource == 'evtp-version' &&
            this.tableModel.resource == 'evtp-acc'
          ) {
            this.adjustedRecord['oe_cd'] = foreignKeyObject.verantwoordelijke_oe.oe_cd
          }
        } else if (foreignKey && !foreignKeyObject) {
          this.adjustedRecord[originalKey] = null
        }
      } else {
        this.adjustedRecord[fieldKey] = foreignKeyObject
      }
    },
    getDataType(fieldKey: string) {
      return this.tableModelUpdated.fields[fieldKey]['data_type']
    },
    isRequired(fieldKey: string) {
      return this.tableModelUpdated.fields[fieldKey]['required']
    },
    isReadonly(fieldKey: string) {
      return this.tableModelUpdated.fields[fieldKey]['readonly']
    }
  }
})
</script>

<style lang="scss">
tr {
  border: 1px solid blue;
}
</style>
