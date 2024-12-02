export type Ond = {
  ond_cd: number
  titel: string
  omschrijving: string
  sort_key: number
}

export type EvtpOnd = {
  evtp_ond_cd: number
  evtp_cd: number
  ond: number
}

export type OndTree = {
  evtp_ond_cd: number
  ond_cd: number
  titel: string
}
