export interface LinkStatus {
  url: string
  is_alive: boolean
  primary_key: string | number
  description: string
}

export interface ResourceLinkStatus {
  resource: string
  links: {
    [key: string]: LinkStatus[]
  }
}
