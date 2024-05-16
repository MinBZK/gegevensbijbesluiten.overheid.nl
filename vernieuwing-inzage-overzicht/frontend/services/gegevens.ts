import type { GgQuery, GgQueryResult } from '~~/types/gegevens'

const getGgFiltered = (query: GgQuery) =>
  useFetch<GgQueryResult>('/gg/filter', {
    baseURL: useRuntimeConfig().public.apiBaseUrl,
    method: 'POST',
    body: query,
  })

const getOneGg = (ggUpc: string) =>
  useFetch<any>(`/gg/${ggUpc}`, {
    baseURL: useRuntimeConfig().public.apiBaseUrl,
  })

export default {
  getGgFiltered,
  getOneGg,
}
