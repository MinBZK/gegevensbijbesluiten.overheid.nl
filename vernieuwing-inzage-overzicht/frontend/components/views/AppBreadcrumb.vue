<template>
  <div
    v-if="breadcrumbs.length != 0 && !error"
    :class="{
      'row row--page-opener': breadcrumbs.length < 3,
      'row row--page-opener margin': breadcrumbs.length >= 3,
    }"
  >
    <div class="container">
      <div class="breadcrumb">
        <p>{{ t('you-are-here') }}:</p>
        <ClientOnly>
          <ol>
            <li v-for="crumb in breadcrumbsWithLinks" :key="crumb.routeName">
              <NuxtLink
                v-if="
                  crumb.routeName == 'besluit' ||
                  crumb.routeName == 'index' ||
                  crumb.routeName == 'gegevens' ||
                  crumb.routeName == 'organisaties'
                "
                :to="{ name: `${crumb.routeName}` }"
                >{{ crumb.label }}</NuxtLink
              >
              <NuxtLink
                v-else
                :to="
                  getLink(
                    `/besluit/${crumb.routeName}`,
                    crumb.versionNr as number
                  ).value
                "
                >{{ crumb.label }}</NuxtLink
              >
              <span v-if="crumb.routeName == null">{{ crumb.label }}</span>
            </li>
            <li>{{ pathTail.label }}</li>
          </ol>
        </ClientOnly>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { navigationItems } from '@/config/config'
import { evtpNm, ggNm, oeNm } from '@/utils/index'
import { getLink } from '~/common/common-functions'

const error = useError()

const { t } = useI18n()
const { p } = usePreditor()

const currentRoute = useRoute()

const navigationItemsTranslated = computed(() =>
  navigationItems.map((item) => {
    return { label: p(item.localeName), routeName: item.routeName }
  })
)

onMounted(() => {})

const ignoredNavigationItems = ['footer']

type Crumb = {
  label: string
  routeName: string
  versionNr: number | null
}

const breadcrumbs = computed<Crumb[]>(() => {
  const path = currentRoute.path
  // the added '/ ' is interpreted in the mapping as the link to Home
  const crumbStrings: string[] =
    path !== '/' ? ('/' + path).split('/').slice(1) : []

  const filteredCrumbStrings = crumbStrings.filter(
    (crumb) => crumb && !ignoredNavigationItems.includes(crumb)
  )

  const crumbs: Crumb[] = filteredCrumbStrings.map((crumb: any) => {
    const item = navigationItemsTranslated.value.find(
      (item) => item.routeName === crumb
    )

    const label = item?.label
    let name = crumb === evtpNm.value.upc ? evtpNm.value.name : ggNm.value.name
    name = crumb === oeNm.value.upc ? oeNm.value.name : name

    return {
      label: label ?? name,
      routeName: crumb,
      versionNr: evtpNm.value.versionNr,
    }
  })

  return crumbs.length > 0
    ? [
        {
          label: 'Home',
          routeName: 'index',
          versionNr: null,
        },
        ...crumbs,
      ]
    : []
})

const breadcrumbsWithLinks = computed(() => breadcrumbs.value.slice(0, -1))
const pathTail = computed(() => breadcrumbs.value.slice(-1)[0])
</script>

<style scoped lang="scss">
.container {
  // width: $page-width;
  padding-top: 38px;
}
</style>
