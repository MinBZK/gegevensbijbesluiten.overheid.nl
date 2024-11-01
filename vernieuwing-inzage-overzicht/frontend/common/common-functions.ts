export const getLink = (path: string, versieNr?: number): Ref<string> => {
  const runtimeConfig = useRuntimeConfig()
  const link =
    runtimeConfig.public.colorMode === 'concept' && path.split('/')[1] === 'besluit'
      ? `${path}?versionNr=${versieNr}`
      : path

  return ref(link)
}

export const channelIfConcept = computed(() => {
  const condition = useRuntimeConfig().public.colorMode === 'concept'
  return condition
})

export const capitaliseFirstLetter = (string: string): string => {
  return string.charAt(0).toUpperCase() + string.slice(1)
}
