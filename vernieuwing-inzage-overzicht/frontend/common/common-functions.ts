export const getLink = (path: string, versieNr?: number): Ref<object> => {
  const query = { versionNr: versieNr }
  const condition = useRuntimeConfig().public.colorMode === 'concept'
  const link = condition ? { path, query } : { path }
  return computed(() => link)
}

export const channelIfConcept = computed(() => {
  const condition = useRuntimeConfig().public.colorMode === 'concept'
  return condition
})

export const capitaliseFirstLetter = (string: string): string => {
  return string.charAt(0).toUpperCase() + string.slice(1)
}
