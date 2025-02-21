export default defineNuxtConfig({
  ssr: !(process.env.NUXT_DEV && process.env.NUXT_DEV !== ''), // Disable server-side rendering when in development
  app: {
    head: {
      link: [{ rel: 'icon', type: 'image/png', href: '/favicon.ico' }]
    }
  },
  devtools: {
    enabled: true
  },
  build: {
    transpile: ['vue-i18n']
  },
  modules: [
    '@nuxtjs/color-mode',
    'nuxt-icon',
    'nuxt-security',
    '@piwikpro/nuxt-piwik-pro',
    '@nuxtjs/i18n',
    'nuxt-simple-sitemap'
  ],
  piwikPro: {
    containerId: '262fdf7d-ae55-4632-8bee-31b4d1c306c1',
    containerUrl: 'https://statistiek.rijksoverheid.nl'
  },
  i18n: {
    locales: ['nl'],
    defaultLocale: 'nl',
    strategy: 'no_prefix',
    vueI18n: '@/config/i18.ts'
  },
  colorMode: {
    classSuffix: '-mode'
  },
  vite: {
    css: {
      preprocessorOptions: {
        scss: {
          additionalData: `@import "@/assets/styles/global.scss";`
        }
      }
    }
  },
  css: ['@/assets/styles/main.scss'],
  runtimeConfig: {
    public: {
      apiBaseUrl: process.env.NUXT_PUBLIC_API_BASE_URL,
      colorMode: process.env.NUXT_PUBLIC_COLOR_MODE
    }
  },
  typescript: {
    typeCheck: true,
    tsConfig: {
      compilerOptions: {
        // baseUrl: "./",
        module: 'ESNext',
        paths: {
          '@/*': ['./*.ts'],
          '~/*': ['./*.ts'],
          '~~/*': ['./*.ts']
        }
      }
    }
  },
  security:
    process.env.NUXT_DEV && process.env.NUXT_DEV !== ''
      ? {
          headers: {}
        }
      : {
          headers: {
            xXSSProtection: false,
            strictTransportSecurity: {
              maxAge: 31536000,
              includeSubdomains: true,
              preload: true
            },
            crossOriginEmbedderPolicy: false,
            contentSecurityPolicy: {
              'default-src': ["'self'"],
              'base-uri': ["'self'"],
              'font-src': ["'self'"],
              'connect-src': [
                "'self'",
                'https://statistiek.rijksoverheid.nl',
                'https://api.iconify.design'
              ],
              'form-action': ["'self'"],
              'frame-ancestors': ["'self'"],
              'img-src': ["'self'", 'https://statistiek.rijksoverheid.nl', 'data:'],
              'object-src': ["'none'"],
              'script-src-attr': ["'none'"],
              'script-src-elem': [
                "'self'",
                "'nonce-{{nonce}}'",
                'https://statistiek.rijksoverheid.nl',
                "'sha256-qWmdE4JQLIb9NMuTXQ3incKVGl6Hq0DR/WnvPBKK3Gw='"
              ],
              'script-src': ["'nonce-{{nonce}}'", 'https://statistiek.rijksoverheid.nl'],
              'style-src': ["'self'", "'nonce-{{nonce}}'", "'http://w3.org'"],
              'upgrade-insecure-requests': true
            },
            referrerPolicy: 'strict-origin-when-cross-origin',
            xContentTypeOptions: 'nosniff',
            xDNSPrefetchControl: 'off',
            xFrameOptions: 'SAMEORIGIN',
            permissionsPolicy: {
              camera: ['()'],
              'display-capture': ['()'],
              fullscreen: ['()'],
              geolocation: ['()'],
              microphone: ['()']
            }
          },
          csrf: true,
          nonce: true
        }
})
