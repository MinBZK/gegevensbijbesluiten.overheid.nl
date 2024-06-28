const summaryTiles: Array<string> = ['aanleiding', 'gebr_dl', 'naam_spraakgbr']

const navigationItems = [
  {
    localeName: 'navigation.home',
    routeName: 'index',
  },
  {
    localeName: 'navigation.onderwerp',
    routeName: 'onderwerp',
  },
  {
    localeName: 'navigation.besluitRegister',
    routeName: 'besluit',
  },
  {
    localeName: 'navigation.gegevens',
    routeName: 'gegevens',
  },
  {
    localeName: 'navigation.organisaties',
    routeName: 'organisaties',
  },
  {
    localeName: 'navigation.uitleg',
    routeName: 'uitleg',
  },
  {
    localeName: 'navigation.footer',
    routeName: 'footer',
  },
  {
    localeName: 'navigation.over',
    routeName: 'over',
  },
  {
    localeName: 'navigation.contact',
    routeName: 'contact',
  },
  {
    localeName: 'navigation.privacyverklaring',
    routeName: 'privacyverklaring',
  },
  {
    localeName: 'navigation.toegankelijkheid',
    routeName: 'toegankelijkheid',
  },
  {
    localeName: 'navigation.db',
    routeName: 'dashboard',
  },
]

const backendContentLanguage = 'nl'

export { summaryTiles, navigationItems, backendContentLanguage }
