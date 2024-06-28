import type { SelectedFilter } from './filter'

export interface Oe {
  oe_cd: number
  oe_upc: number
  naam_officieel: string
  naam_spraakgbr: string
}

interface OeKoepelOe {
  child_entity: Oe
}

export interface OeKoepel {
  titel: string
  omschrijving: string
  child_oe_struct: OeKoepelOe[]
}

export interface OeQueryResult {
  results: OeKoepel[]
  total_count_koepel: number
  total_count_underlying: number
  selected_filters: SelectedFilter[]
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
