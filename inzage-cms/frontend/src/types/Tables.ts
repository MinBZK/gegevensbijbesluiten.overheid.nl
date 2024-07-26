export type Table = {
  label: string
  group: string
  resource: string
  nameKey: string
  primaryKey: string
  maxWidthDialog: number
  columns: { [key: string]: string }
  hiddenColumns: Array<string>
  fieldOrder: Array<string>
  visible: boolean
}

export type TableRow = {
  id_publicatiestatus: string
}

export type TableModelColumn = {
  COLUMN_NAME: string
  DATA_TYPE: string
  CHARACTER_MAXIMUM_LENGTH: number
  COLUMN_TYPE: string
  COLUMN_KEY: string
  IS_NULLABLE: boolean
}

export type TableModelForeignKey = {
  foreign_key: string
  direction: string
  foreign_resource: string
  foreign_table: TableModel
}

export type TableModel = {
  resource: string
  primary_key: string
  description_key: string
  foreign_keys: TableModelForeignKey[]
  foreign_key_mapping: object
  fields: { [key: string]: Fields[] }
}

export type Fields = {
  required: boolean
  optional: boolean
  readonly: boolean
  max_length: string
  data_type: string
}
