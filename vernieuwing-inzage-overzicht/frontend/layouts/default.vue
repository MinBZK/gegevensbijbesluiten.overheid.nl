<template>
  <div>
    <div class="skiplinks container">
      <a href="#content" class="no-margin" tabindex="1">Direct naar content</a>
    </div>
    <AppHeader />
    <AppBreadcrumb />
    <AppPageBanner />
    <div>
      <slot />
    </div>
    <AppFooter>
      <template #after-footer>
        <div class="container"></div>
      </template>
    </AppFooter>
  </div>
</template>

<script setup lang="ts">
import AppHeader from '@/components/views/AppHeader.vue'
import AppBreadcrumb from '@/components/views/AppBreadcrumb.vue'
import AppFooter from '@/components/views/AppFooter.vue'
import AppPageBanner from '@/components/views/AppPageBanner.vue'

const { t, locale } = useI18n()
const siteTitle = computed(() => t('homepageTitle'))

useHead({
  htmlAttrs: { lang: locale },
  titleTemplate: (pageTitle) => {
    return pageTitle ? `${pageTitle} - ${siteTitle.value}` : siteTitle.value
  }
})
</script>
