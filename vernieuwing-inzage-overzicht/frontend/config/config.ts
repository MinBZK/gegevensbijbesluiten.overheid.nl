const summaryTiles: Array<string> = ['aanleiding', 'gebr_dl', 'naam_spraakgbr']

const navigationItems = [
  {
    localeName: 'navigation.home',
    routeName: 'index'
  },
  {
    localeName: 'navigation.onderwerp',
    routeName: 'onderwerp'
  },
  {
    localeName: 'navigation.besluitRegister',
    routeName: 'besluit'
  },
  {
    localeName: 'navigation.gegevens',
    routeName: 'gegeven'
  },
  {
    localeName: 'navigation.organisaties',
    routeName: 'organisatie'
  },
  {
    localeName: 'navigation.uitleg',
    routeName: 'uitleg'
  },
  {
    localeName: 'navigation.footer',
    routeName: 'footer'
  },
  {
    localeName: 'navigation.over',
    routeName: 'over'
  },
  {
    localeName: 'navigation.contact',
    routeName: 'contact'
  },
  {
    localeName: 'navigation.privacyverklaring',
    routeName: 'privacyverklaring'
  },
  {
    localeName: 'navigation.toegankelijkheid',
    routeName: 'toegankelijkheid'
  },
  {
    localeName: 'navigation.db',
    routeName: 'dashboard'
  },
  {
    localeName: 'navigation.archief',
    routeName: 'archief'
  },
  {
    localeName: 'navigation.kwetsbaarheid',
    routeName: 'kwetsbaarheid-melden'
  },
  {
    localeName: 'navigation.cookies',
    routeName: 'cookies'
  },
  {
    localeName: 'navigation.copyright',
    routeName: 'copyright'
  }
]

const backendContentLanguage = 'nl'

const getMaxListItems = () => {
  const maxListItemsInModal = ref(Infinity as number)

  return {
    maxListItemsInModal
  }
}

export { summaryTiles, navigationItems, backendContentLanguage, getMaxListItems }
