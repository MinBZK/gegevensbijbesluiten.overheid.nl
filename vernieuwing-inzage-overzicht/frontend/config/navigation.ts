interface navigationHeader {
  label: string
  routeName: string
  highlightOnRoutes: string[]
  banner: string
  pageTitle: string
  pageDescriptionParagraph_1: string
  pageDescriptionParagraph_2: string
  pageDescriptionParagraph_2_2: string
  pageDescriptionParagraph_3: string
  pageDescriptionItalic: string
  pageLink_1: string
}

export const navigationHeaders: navigationHeader[] = [
  {
    label: 'navigation.home',
    routeName: 'index',
    highlightOnRoutes: ['index'],
    banner: 'heroes/landing-hero.svg',
    pageTitle: 'pages: home.title',
    pageDescriptionParagraph_1: 'pages: home.description_1',
    pageDescriptionParagraph_2: 'pages: home.description_2_1',
    pageDescriptionParagraph_2_2: 'pages: home.description_2_2',
    pageDescriptionParagraph_3: '',
    pageDescriptionItalic: '',
    pageLink_1: 'pages: onderwerpen.title'
  },
  {
    label: 'navigation.onderwerp',
    routeName: 'onderwerp',
    highlightOnRoutes: ['onderwerp'],
    banner: 'heroes/onderwerp-hero.svg',
    pageTitle: 'pages: onderwerpen.title',
    pageDescriptionParagraph_1: 'pages: onderwerpen.description_1',
    pageDescriptionParagraph_2: 'pages: onderwerpen.description_2',
    pageDescriptionParagraph_2_2: '',
    pageDescriptionParagraph_3: '',
    pageDescriptionItalic: '',
    pageLink_1: ''
  },
  {
    label: 'navigation.besluitRegister',
    routeName: 'besluit',
    highlightOnRoutes: ['besluit', 'besluit-evtp_upc', 'besluit-evtp_upc-gst_upc'],
    banner: 'heroes/besluit-hero-young.svg',
    pageTitle: 'pages: besluiten.title',
    pageDescriptionParagraph_1: 'pages: besluiten.description_1',
    pageDescriptionParagraph_2: 'pages: besluiten.description_2',
    pageDescriptionParagraph_2_2: '',
    pageDescriptionParagraph_3: 'pages: besluiten.description_3',
    pageDescriptionItalic: '',
    pageLink_1: ''
  },
  {
    label: 'navigation.gegevens',
    routeName: 'gegeven',
    highlightOnRoutes: ['gegeven', 'gegeven-gg_upc'],
    banner: 'heroes/gegevens-hero.svg',
    pageTitle: 'pages: gegevens.title',
    pageDescriptionParagraph_1: 'pages: gegevens.description_1',
    pageDescriptionParagraph_2_2: '',
    pageDescriptionParagraph_2: 'pages: gegevens.description_2',
    pageDescriptionParagraph_3: '',
    pageDescriptionItalic: '',
    pageLink_1: ''
  },
  {
    label: 'navigation.organisaties',
    routeName: 'organisatie',
    highlightOnRoutes: ['organisatie', 'organisatie-oe_upc'],
    banner: 'heroes/organisaties-hero.svg',
    pageTitle: 'pages: organisaties.title',
    pageDescriptionParagraph_1: 'pages: organisaties.description_1',
    pageDescriptionParagraph_2: '',
    pageDescriptionParagraph_2_2: '',
    pageDescriptionParagraph_3: '',
    pageDescriptionItalic: 'pages: organisaties.description_italics',
    pageLink_1: ''
  }
  // {
  //   label: 'navigation.dashboard',
  //   routeName: 'dashboard',
  //   highlightOnRoutes: ['dashboard'],
  // },
]
