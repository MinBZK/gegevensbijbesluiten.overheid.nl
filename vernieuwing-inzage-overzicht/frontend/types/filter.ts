export interface UrlQuery {
  page?: string
  limit?: string
  searchtext?: string
  organisation?: string
}

export interface SelectedFilter {
  key: keyof UrlQuery
  value?: string
}

export interface FilterData {
  label: string
  key: string
  count: number
}

export interface BesluitFilterData {
  organisation: FilterData[]
  onderwerp: FilterData[]
}
