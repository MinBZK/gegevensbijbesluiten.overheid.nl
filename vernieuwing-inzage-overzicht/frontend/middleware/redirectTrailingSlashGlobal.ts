export default defineNuxtRouteMiddleware((to, _from) => {
  if (to.path === '/besluit/') {
    const { path, query, hash } = to
    const nextPath = path.replace(/\/+$/, '') || '/'
    const nextRoute = { path: nextPath, query, hash }
    return navigateTo(nextRoute, { redirectCode: 301 })
  }
})
