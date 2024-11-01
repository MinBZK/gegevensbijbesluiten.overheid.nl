import type { OeQuery, OeQueryResult } from '~~/types/organisatie'

const getOeFiltered = (query: OeQuery) =>
  useFetch<OeQueryResult>('/oe/filter', {
    baseURL: useRuntimeConfig().public.apiBaseUrl,
    method: 'POST',
    body: query
  })

const getOneOe = (oeUpc: string) =>
  useFetch<any>(`/oe/${oeUpc}`, {
    baseURL: useRuntimeConfig().public.apiBaseUrl
  })

export default {
  getOeFiltered,
  getOneOe
}
