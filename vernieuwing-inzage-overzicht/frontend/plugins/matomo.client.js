import VueMatomo from 'vue-matomo'

export default defineNuxtPlugin((nuxtApp) => {
  nuxtApp.vueApp.use(VueMatomo, {
    host: 'https://statistiek.rijksoverheid.nl',
    siteId: '262fdf7d-ae55-4632-8bee-31b4d1c306c1',
    trackerFileName: 'matomo',
    router: nuxtApp.$router,
    enableLinkTracking: true,
    requireConsent: false,
    trackInitialView: true,
    disableCookies: false,
    requireCookieConsent: false,
    enableHeartBeatTimer: false,
    heartBeatTimerInterval: 15,
    debug: false,
    userId: undefined,
    cookieDomain: undefined,
    domains: undefined,
    preInitActions: [],
    trackSiteSearch: false,
  })
})
