import { createVuetify } from 'vuetify'
import { nl, en } from 'vuetify/locale'

export default defineNuxtPlugin((nuxtApp) => {
  const vuetify = createVuetify({
    locale: {
      locale: 'nl',
      messages: { nl, en }
    },
    ssr: true,
    display: {
      mobileBreakpoint: 'sm',
      thresholds: {
        sm: 1040 // this equals 65em
      }
    }
  })

  nuxtApp.vueApp.use(vuetify)
})
