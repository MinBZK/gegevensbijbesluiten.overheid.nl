import type { Ond } from '@/types/besluit'

const getPopulatedOnd = (params: { limit: number }) =>
  useFetch<Ond[]>('/ond/populated', {
    baseURL: useRuntimeConfig().public.apiBaseUrl,
    params,
  })

export default {
  getPopulatedOnd,
}
