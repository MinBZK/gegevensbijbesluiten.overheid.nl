export enum PublicatieStatus {
  NIEUW = 'Nieuw',
  GEREEDVOORCONTROLE = 'Gereed voor controle',
  GEPUBLICEERD = 'Gepubliceerd',
  GEARCHIVEERD = 'Gearchiveerd'
}

export const getPublicatieStatus = (status: number): string => {
  return Object.values(PublicatieStatus)[status - 1]
}

export type StatusOe = {
  index: string
  columns: string
  data: number
}
