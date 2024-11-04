import { filename } from 'pathe/utils'
import type { Ond } from '@/types/besluit'

const getPopulatedOnd = (params: { limit: number }) =>
  useFetch<Ond[]>('/ond/populated', {
    baseURL: useRuntimeConfig().public.apiBaseUrl,
    params
  })

const getIcon = (title: string) => {
  // a roundabout way because nuxt cannot dynamically import assets
  const paths = import.meta.glob('@/assets/images/icons/onderwerp/icon-*.svg', {
    eager: true
  })
  const images = Object.fromEntries(
    Object.entries(paths).map(([key, value]) => [filename(key), (value as any).default])
  )
  switch (title) {
    case 'Gezondheid':
      return images['icon-health']
    case 'Identiteit':
      return images['icon-identity']
    case 'Inkomen':
      return images['icon-income']
    case 'Onderwijs':
      return images['icon-education']
    case 'Recht':
      return images['icon-law']
    case 'Schulden':
      return images['icon-liabilities']
    case 'Vervoer':
      return images['icon-transport']
    case 'Werk':
      return images['icon-career']
    case 'Wonen':
      return images['icon-living']
    case 'Familie':
      return images['icon-family']
    case 'Belastingen':
      return images['icon-tax']
    case 'Ondernemen':
      return images['icon-undertaking']
  }
  return ''
}

export { getIcon }

export default {
  getPopulatedOnd
}
