import type { SupportingText } from '@/types/preditor'

const getAllContent = async () =>
  await useFetch<SupportingText>(`/static-content`, {
    baseURL: useRuntimeConfig().public.apiBaseUrl,
    method: 'GET',
  })

export { getAllContent }
