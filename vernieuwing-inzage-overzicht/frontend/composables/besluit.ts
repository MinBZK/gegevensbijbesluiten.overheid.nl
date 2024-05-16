import type { Evtp } from '~~/types/besluit'

export const useEvtp = () => {
  const evtp = useState<Evtp | null>('besluit', () => null)
  const setEvtp = (a: Evtp | null) => (evtp.value = a)

  const route = useRoute()
  watch(route, () => {
    if (route.name !== 'besluit') setEvtp(null)
  })

  return {
    evtp,
    setEvtp,
  }
}
