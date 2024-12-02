import type { RgeTree } from '@/types/Rge'
import type { Gg, GgTree } from '@/types/Gg'
import type { Ibron } from '@/types/Ibron'
import type { Gst, GstTypeTree } from '@/types/Gst'
import type { Oe } from '@/types/Oe'

export type EvtpVersion = {
  evtp_cd: number
  versie_nr: number
  evtp_nm: string
  omschrijving: string
  overige_informatie: string
  overige_informatie_link: string
  aanleiding: string
  gebr_dl: string
  oe_best: number
  lidw_soort_besluit: string
  soort_besluit: string
  uri: string
  huidige_versie: boolean
  id_publicatiestatus: number
  ts_publ: Date
  notitie: string
  user_nm: string
  ts_mut: Date
  ts_start: Date
}

export type Omg = {
  omg_cd: number
  titel: string
  oe_cd: number
  lidw: string
  link: string
}

export type EvtpTree = {
  evtp_cd: number
  versie_nr: number | string
  evtp_upc: number
  evtp_nm: string
  id_publicatiestatus: number
  verantwoordelijke_oe: Oe
}

export type EvtpGst = {
  evtp_gst_cd: number
  sort_key: number
}

export type EntityInDirectlyRelated = {
  evtpGst: EvtpGst[]
  gst: Gst[]
  gstType: GstTypeTree[][]
  oeBron: Oe[]
  ibron: Ibron[]
  ggChild: GgTree[][]
  ggParent: Gg[][]
  rge: RgeTree[][]
}
