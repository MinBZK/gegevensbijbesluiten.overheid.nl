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
  result_oe: OeKoepel[]
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
