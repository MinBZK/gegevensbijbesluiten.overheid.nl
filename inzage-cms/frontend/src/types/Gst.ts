export type Gst = {
  gst_cd: number
  gst_upc: number
  omschrijving: string
  oe_bron: number
  oe_best: number
  ibron: number
  ext_lnk_auth: string
  conditie: string
}

export type GstTypeTree = {
  gstt_cd: number
  gst_gstt_cd: number
  gstt_naam: string
  gstt_oms: string
  gstt_pp: string
}
