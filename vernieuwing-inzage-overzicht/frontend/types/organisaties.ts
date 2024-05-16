import type { SelectedFilter } from './filter'

interface OeStruct {
  child_entity: {
    naam_officieel: string
    naam_spraakgbr: string
    oe_cd: number
    oe_upc: number
  }
}

export interface Oe {
  oe_cd: number
  oe_upc: number
  naam_officieel: string
  naam_spraakgbr: string
  child_oe_struct: OeStruct[]
}

export interface OeQueryResult {
  results: Oe[]
  total_count: number
  selected_filters: SelectedFilter[]
  // filter_data: BesluitFilterData
}

export interface OeQuery {
  page: number
  limit: number
  searchtext?: string
  organisation?: string
}

export interface Ibron {
  ibron_cd: number
  omschrijving: string
  // eslint-disable-next-line no-use-before-define
  entity_oe: OeRelations
}

interface OeRelations {
  naam_spraakgbr: string
  naam_officieel: string
  lidw_sgebr?: string
  e_contact?: string
  internet_domein?: string
  entity_ibron?: Ibron
}
