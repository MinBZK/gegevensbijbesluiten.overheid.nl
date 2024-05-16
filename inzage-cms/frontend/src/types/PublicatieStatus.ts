export enum PublicatieStatus {
    NIEUW = 'Nieuw',
    GEREEDVOORCONTROLE = 'Gereed voor controle',
    GEPUBLICEERD = 'Gepubliceerd',
    GEARCHIVEERD = 'Gearchiveerd',
  }
  
export type StatusOe = {
    index: string
    columns: string
    data: number
  }