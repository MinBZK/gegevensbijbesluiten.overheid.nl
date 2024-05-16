import type { OeStatisticsList } from '@/types/besluit'

const getTotalCount = () =>
  useFetch<number>(`/evtp/count`, {
    baseURL: useRuntimeConfig().public.apiBaseUrl,
  })

const getOeStatistics = () =>
  useFetch<OeStatisticsList>(`/evtp/statistics-per-oe`, {
    baseURL: useRuntimeConfig().public.apiBaseUrl,
  })

export default {
  getTotalCount,
  getOeStatistics,
}
