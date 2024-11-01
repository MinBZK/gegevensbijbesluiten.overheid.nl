const changeHash = (hash: string | undefined) => {
  const router = useRouter()
  if (typeof hash === 'string') {
    router.replace({
      hash: '#' + hash
    })
  } else {
    router.replace({
      hash: ''
    })
  }
}

interface pageTitleInfo {
  title: string
  labelType: 'locale-index' | 'page-title'
}
const pageTitleInfo = ref<pageTitleInfo>({
  title: '',
  labelType: 'page-title'
})
const providePageTitle = (input: pageTitleInfo = { title: '', labelType: 'page-title' }) => {
  pageTitleInfo.value = input
}

interface mappingUpc {
  name: string
  upc: string
  versionNr: number | null
}

const evtpNm = ref<mappingUpc>({
  name: '',
  upc: '',
  versionNr: null
})

const ggNm = ref<mappingUpc>({
  name: '',
  upc: '',
  versionNr: null
})

const oeNm = ref<mappingUpc>({
  name: '',
  upc: '',
  versionNr: null
})

// (un)collapse accordion
const activeItem = ref(
  [] as Array<{
    header: string
    active: boolean
    iconAccordion: string
    index: number
  }>
)
const hideUnhideAccordion = ref<boolean>(true)
const textCollapseAllAccordions = ref<string>('Overzicht uitklappen')

const hideUnhideAccordionAllAccordions = (inputHidden: boolean) => {
  if (inputHidden) {
    activeItem.value.map((item) => (item.active = true))
    activeItem.value.map((item) => (item.iconAccordion = 'fa-chevron-up'))
    textCollapseAllAccordions.value = 'Overzicht inklappen'
    hideUnhideAccordion.value = false
  } else {
    activeItem.value.map((item) => (item.active = false))
    activeItem.value.map((item) => (item.iconAccordion = 'fa-chevron-down'))
    textCollapseAllAccordions.value = 'Overzicht uitklappen'
    hideUnhideAccordion.value = true
  }
}

const openCloseAccordion = (header: string, accordionHeader: HTMLElement | null) => {
  hideUnhideAccordion.value = false
  textCollapseAllAccordions.value = 'Overzicht inklappen'
  const showSection = !activeItem.value
    .filter((item) => item.header === header)
    .map((item) => item.active)[0]
  activeItem.value
    .filter((item) => item.header === header)
    .map((item) => (item.active = showSection))
  const icon = showSection ? 'fa-chevron-up' : 'fa-chevron-down'
  activeItem.value
    .filter((item) => item.header === header)
    .map((item) => (item.iconAccordion = icon))

  if (accordionHeader) {
    accordionHeader.scrollIntoView({ behavior: 'smooth' })
  }
  return activeItem.value.filter((item) => item.header === header)
}

const openCloseAccordionMutuallyExclusive = (header: string) => {
  activeItem.value.map((item) => {
    if (item.header === header) {
      item.active = !item.active
      item.iconAccordion = item.active ? 'fa-chevron-up' : 'fa-chevron-down'
    } else {
      item.active = false
      item.iconAccordion = 'fa-chevron-down'
    }
    return activeItem.value.filter((item) => item.header === header)
  })
}

const isAccordionActive = (header: string) => {
  if (activeItem) {
    return activeItem.value.filter((item) => item.header === header).map((item) => item.active)[0]
  } else return false
}

const getIconAccordion = (header: string) => {
  return (
    activeItem.value
      .filter((item) => item.header === header)
      .map((item) => item.iconAccordion)[0] ?? 'fa-chevron-down'
  )
}

const resetAccordion = () => {
  activeItem.value.map((item) => (item.active = false))
  activeItem.value.map((item) => (item.iconAccordion = 'fa-chevron-down'))
  textCollapseAllAccordions.value = 'Overzicht uitklappen'
  hideUnhideAccordion.value = true
}

export {
  changeHash,
  providePageTitle,
  pageTitleInfo,
  evtpNm,
  ggNm,
  oeNm,
  isAccordionActive,
  openCloseAccordion,
  openCloseAccordionMutuallyExclusive,
  hideUnhideAccordionAllAccordions,
  activeItem,
  hideUnhideAccordion,
  textCollapseAllAccordions,
  getIconAccordion,
  resetAccordion
}
