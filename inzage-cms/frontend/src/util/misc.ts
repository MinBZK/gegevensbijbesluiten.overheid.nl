import { toRaw } from 'vue'
import moment from 'moment-timezone'
import { TableModel, TableModelForeignKey } from '@/types/Tables'

const getPrimaryKey = (tableModel: TableModel) => {
  return tableModel.primary_key || ''
}

const getid_publicatiestatus = (tableModel: TableModel) => {
  return !!tableModel.fields['id_publicatiestatus']
}

const getTableValue = (foreignKey: TableModelForeignKey | undefined, value: string) => {
  if (typeof value === 'function') {
    return ''
  }
  if (foreignKey) {
    return value ? value[foreignKey.foreign_table.description_key] : value
  } else {
    return value
  }
}

const getTableKey = (foreignKey: TableModelForeignKey | undefined, value) => {
  if (foreignKey) {
    return value ? value[foreignKey.foreign_table.primary_key] : value
  } else {
    return value
  }
}

const mapFieldKeys = (tableModel: TableModel, mapFrom: string) => {
  const allColumns = Object.keys(tableModel.fields)
  return allColumns.reduce((obj, originalHeader) => {
    const mappedHeader = tableModel.foreign_key_mapping[originalHeader] || originalHeader
    if (mapFrom == 'original') {
      obj[mappedHeader] = originalHeader
    } else if (mapFrom == 'foreign') {
      obj[originalHeader] = mappedHeader
    }

    return obj
  }, {})
}

const getEnvironment = (envObj: Array<object>, variable: string) => {
  if (envObj.filter((record) => record[variable]).length > 0) {
    return Object.values(toRaw(envObj)?.filter((record) => record[variable])[0])[0]
  } else return 'Lokaal'
}

const formatDateToLocale = (fieldKey: string, recordData: string) => {
  if ((fieldKey === 'ts_mut' || fieldKey === 'ts_publ') && recordData) {
    const dateString = recordData.toString()
    const date = moment(dateString).tz('Europe/Amsterdam')
    return date.locale('nl').format('DD-MM-YYYY HH:mm')
  }
  return recordData || ''
}

export {
  formatDateToLocale,
  getPrimaryKey,
  getTableValue,
  mapFieldKeys,
  getEnvironment,
  getid_publicatiestatus,
  getTableKey
}
