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

export interface GgChild {
  gg_cd: number
  gg_upc: number
  omschrijving: string
}

export interface GgQueryResult {
  result_gg: Gg[]
  total_count_koepel: number
  total_count_underlying: number
  selected_filters: SelectedFilter[]
}

export interface GgQuery {
  page: number
  limit: number
  searchtext?: string
  organisation?: string
}
