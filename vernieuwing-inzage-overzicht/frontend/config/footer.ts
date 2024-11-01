import type { FooterColumn } from '~~/types/footer'

const footer: FooterColumn = {
  internal: [
    {
      key: 'over',
      path: '/over'
    },
    {
      key: 'contact',
      path: '/contact'
    },
    {
      key: 'privacyverklaring',
      path: '/privacyverklaring'
    },
    {
      key: 'toegankelijkheid',
      path: '/toegankelijkheid'
    },
    {
      key: 'archief',
      path: '/archief'
    },
    {
      key: 'kwetsbaarheid',
      path: '/kwetsbaarheid-melden'
    }
  ],
  external: [
    {
      key: 'ext_werkagenda_nl',
      path: 'https://www.digitaleoverheid.nl/kabinetsbeleid-digitalisering/werkagenda/iedereen-heeft-regie-op-het-digitale-leven/acties-prioriteit-3-1/'
    },
    {
      key: 'ext_overheid_nl',
      path: 'https://overheid.nl'
    },
    {
      key: 'ext_rijksoverheid_nl',
      path: 'https://rijksoverheid.nl'
    },
    {
      key: 'ext_digitaleoverheid_nl',
      path: 'https://digitaleoverheid.nl/overzicht-van-alle-onderwerpen/regie-op-gegevens/'
    },
    {
      key: 'ext_algoritmes_nl',
      path: 'https://algoritmes.overheid.nl'
    },
    {
      key: 'ext_pleio_nl',
      path: 'https://rog.pleio.nl'
    }
  ]
}

export default footer
