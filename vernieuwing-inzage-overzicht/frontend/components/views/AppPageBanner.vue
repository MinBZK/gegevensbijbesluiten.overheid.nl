<template>
  <div
    v-if="pageData[0].show && pageData.length === 1"
    :class="{ banner: true, 'no-padding-top': isMobile && !isHomepage }"
  >
    <div
      :class="{
        container: true,
        'banner-content': true,
        'homepage-height': isHomepage
      }"
    >
      <div class="introduction">
        <h1 id="content" class="page-title">
          {{ t(`${pageData[0].pageTitle}`) }}
        </h1>
        <p>
          {{ t(`${pageData[0].pageDescriptionParagraph_1}`) }}
        </p>
        <p v-if="pageData[0].pageDescriptionParagraph_2" class="no-margin">
          {{ t(`${pageData[0].pageDescriptionParagraph_2}`) }}
          <span v-if="pageData[0].pageLink_1" class="no-margin">
            <NuxtLink :to="{ name: 'onderwerp' }">
              {{ t(`${pageData[0].pageLink_1}`) }}
            </NuxtLink>
            {{ t(`${pageData[0].pageDescriptionParagraph_2_2}`) }}
          </span>
        </p>
        <p v-if="pageData[0].pageDescriptionParagraph_3" class="no-margin-description">
          {{ t(`${pageData[0].pageDescriptionParagraph_3}`) }}
        </p>
        <p v-if="pageData[0].pageDescriptionItalics">
          <i> {{ t(`${pageData[0].pageDescriptionItalics}`) }}</i>
        </p>
        <FormOverheidButton
          v-if="pageData[0].routeName === 'index'"
          :label="t('readMore')"
          to="/uitleg"
        />
      </div>
      <div :class="{ hero: true, 'is-homepage': isHomepage }">
        <img :src="pageData[0].bannerImage" alt="" />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { navigationItems } from '@/config/config'
import { navigationHeaders } from '@/config/navigation'

const { t } = useI18n()
const currentRoute = useRoute()
const isHomepage = computed(() => currentRoute.path === '/')
const isMobile = useMobileBreakpoint().small

const navigationItemsTranslated = computed(() =>
  navigationItems.map((item) => {
    const matchedHeader = navigationHeaders.find((header) => header.routeName === item.routeName)
    return {
      label: t(item.localeName),
      routeName: item.routeName,
      banner: matchedHeader ? matchedHeader.banner : '',
      pageTitle: matchedHeader ? matchedHeader.pageTitle : '',
      pageDescriptionParagraph_1: matchedHeader ? matchedHeader.pageDescriptionParagraph_1 : '',
      pageDescriptionParagraph_2: matchedHeader ? matchedHeader.pageDescriptionParagraph_2 : '',
      pageDescriptionParagraph_2_2: matchedHeader ? matchedHeader.pageDescriptionParagraph_2_2 : '',
      pageDescriptionParagraph_3: matchedHeader ? matchedHeader.pageDescriptionParagraph_3 : '',
      pageLink_1: matchedHeader ? matchedHeader.pageLink_1 : '',
      pageDescriptionItalic: matchedHeader ? matchedHeader.pageDescriptionItalic : ''
    }
  })
)

type pageMeta = {
  routeName: string
  bannerImage: string
  pageTitle: string
  pageDescriptionParagraph_1: string
  pageDescriptionParagraph_2: string
  pageDescriptionParagraph_2_2: string
  pageDescriptionParagraph_3: string
  pageDescriptionItalics: string
  pageLink_1: string
  show: boolean
}

const pageData = computed<pageMeta[]>(() => {
  const path = currentRoute.path
  const crumbStrings: string[] = path !== '/' ? ('/' + path).split('/').slice(1) : ['index']

  const filteredCrumbStrings = crumbStrings.filter((crumb) => crumb)

  const crumbs: pageMeta[] = filteredCrumbStrings.map((crumb: string) => {
    const item = navigationItemsTranslated.value.find((item) => item.routeName === crumb)

    return {
      routeName: crumb,
      bannerImage: item?.banner || '',
      pageTitle: item ? item.pageTitle : '',
      pageDescriptionParagraph_1: item ? item.pageDescriptionParagraph_1 : '',
      pageDescriptionParagraph_2: item ? item.pageDescriptionParagraph_2 : '',
      pageDescriptionParagraph_2_2: item ? item.pageDescriptionParagraph_2_2 : '',
      pageDescriptionParagraph_3: item ? item.pageDescriptionParagraph_3 : '',
      pageDescriptionItalics: item ? item.pageDescriptionItalic : '',
      pageLink_1: item ? item.pageLink_1 : '',
      show: !!item?.banner
    }
  })
  return crumbs
})
</script>

<style scoped lang="scss">
@media (max-width: 51em) {
  .page-title {
    margin-bottom: 0em;
  }
}

.banner {
  background-color: $tertiary;
  padding-top: 30px;
  margin-bottom: -50px;

  &.no-padding-top {
    padding-top: 0px;
  }
}

.banner-content {
  display: grid;
  grid-template-columns: 60fr 25fr;
  column-gap: 10px;
  height: calc(476px - 52px);

  @media (max-width: 90em) {
    grid-template-columns: auto;
    grid-template-rows: 50fr 20em;
    height: auto !important;
  }
  @media (max-width: 70em) {
    grid-template-rows: 50fr 10em;
  }
}

.homepage-height {
  height: calc(476px - 0px);
}

.hero {
  position: relative;
  display: flex;
  justify-content: right;

  @media (max-width: 90em) {
    justify-content: center;
  }

  img {
    position: absolute;
    max-height: 100%;
    bottom: 0;
  }
}
</style>
