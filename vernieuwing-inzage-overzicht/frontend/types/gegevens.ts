import type { SelectedFilter } from './filter'

interface GgStruct {
  child_entity: {
    omschrijving: string
    gg_cd: number
    gg_upc: number
  }
}

export interface Gg {
  gg_cd: number
  gg_upc: number
  omschrijving: string
  omschrijving_uitgebreid: string
  child_gg_struct: GgStruct[]
}

export interface GgQueryResult {
  results: Gg[]
  total_count: number
  selected_filters: SelectedFilter[]
  // filter_data: BesluitFilterData
}

export interface GgQuery {
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
