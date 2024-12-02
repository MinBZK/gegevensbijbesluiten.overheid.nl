import type { SelectedFilter, BesluitFilterData } from './filter'
import type { GgChild } from './gegeven'

export interface Oe {
  oe_cd: number
  oe_upc: number
  afko: string
  huisnummer: string
  huisnummer_toev: string
  ibron_cd: number
  internet_domein: string
  lidw_sgebr: string
  naam_officieel: string
  naam_spraakgbr: string
  notitie: string
  plaats: string
  postcode: string
  provincie: string
  straat: string
  telefoon: string
  ts_mut: Date
  user_nm: string
}
export interface Ond {
  ond_cd: number
  titel: string
  omschrijving: string
  sort_key: number
}

type entities_evtp_ond = {
  entity_ond: Ond
}

type EvtpOeComType = {
  omschrijving: string
  link: string
}

type EvtpCommunication = {
  evtp_oe_com_type: EvtpOeComType[]
  oe_best_internetdomein: string
  evtp_oebest: string
  overige_informatie: string
  overige_informatie_link: string
}

export interface Evtp {
  evtp_cd: number
  evtp_upc: string
  versie_nr: number
  evtp_nm: string
  omschrijving: string
  aanleiding: string
  gebr_dl: string
  sort_key: number
  lidw_soort_besluit: string
  soort_besluit: string
  entity_oe_best: Oe
  entities_evtp_ond: entities_evtp_ond[]
}

export interface EvtpGg {
  besluit_communicatie: EvtpCommunication
  besluit: {
    evtp_cd: number
    evtp_upc: string
    evtp_nm: string
    omschrijving: string
    aanleiding: string
    gebr_dl: string
    soort_besluit: string
    lidw_soort_besluit: string
    oe_lidw_sgebr: string
    oe_naam_spraakgbr: string
    oe_naam_officieel: string
    ond: string[]
    entity_omg: {
      titel: string
      lidw: string
      link: string
      entity_oe: {
        naam_spraakgbr: string
        lidw_sgebr: string
      }
    }
  }
  gegevensgroep: {
    ggParentObject: object[]
    ggParent: any
    index: number
  }
}

type BronOrganisatie = {
  header_oe_bron_naamofficieel: string
  oe_bron_naampraakgebr: string
  oe_bron_lidwsgebr: string
  oe_bron_internetdomein: string
  ibron_oe_naam_officieel: string
  ibron_oe_lidw: string
  ibron_titel: string
  ibron_link: string
  ibron_lidw: string
  gsttype_gsttoms: string[]
  gst_extlnkaut: string
}

type Rge = {
  titel: string
  re_link: string
}

type GegevensgroepGrondslag = {
  header_oe_best_naamofficieel: string
  gg_child: GgChild[]
  gg_parent: string
  gg_omschrijvinguitgebreid: string[]
  evtp_aanleiding: string
  gst_conditie: string
  oe_best_lidwsgebr: string
  oe_best_naampraakgebr: string
  evtp_gebrdl: string
  rge: Rge[]
}

export interface EvtpGst {
  besluit: Evtp
  bron_organisatie: BronOrganisatie
  gegevensgroep_grondslag: GegevensgroepGrondslag
}

export const EvtpGstHeader = {
  besluit: 'besluit',
  bron_organisatie: 'bron_organisatie',
  gegevensgroep_grondslag: 'gegevensgroep_grondslag'
}

type OeStatistics = {
  naam_officieel: string
  count: number
}

export interface OeStatisticsList {
  oe_by_evtp_total: OeStatistics[]
}

export interface EvtpQuery {
  page: number
  limit: number
  searchtext?: string
  organisation?: string
}

export interface EvtpQueryResult {
  result_evtp: Evtp[]
  total_count: number
  filter_data: BesluitFilterData
  selected_filters: SelectedFilter[]
}

export type SearchSuggestion = {
  title: string
  version: number | undefined
  upc: string
}

export type SearchSuggestionsAllEntities = {
  evtp: SearchSuggestion[] | []
  gg: SearchSuggestion[] | []
  oe: SearchSuggestion[] | []
  [key: string]: SearchSuggestion[]
}
