<template>
  <div class="container">
    <div>
      <h1 class="h1 margin-top">{{ t(`footer.paths.cookiesPage.h1`) }}</h1>
      <p>
        {{ t(`footer.paths.cookiesPage.p1`) }}
      </p>
      <h2>
        {{ t(`footer.paths.cookiesPage.h2`) }}
      </h2>
      <p>
        {{ t(`footer.paths.cookiesPage.p2_1`) }}
      </p>
      <ul class="bullet ml-4">
        <li>{{ t(`footer.paths.cookiesPage.li1_1`) }}</li>
        <li>
          {{ t(`footer.paths.cookiesPage.li1_2`) }}
        </li>
      </ul>
      <p>
        {{ t(`footer.paths.cookiesPage.p2_2`) }}
      </p>
      <ul class="bullet ml-4">
        <li>{{ t(`footer.paths.cookiesPage.li2_1`) }}</li>
        <li>
          {{ t(`footer.paths.cookiesPage.li2_2`) }}
        </li>
        <li>
          {{ t(`footer.paths.cookiesPage.li2_3`) }}
        </li>
        <li>
          {{ t(`footer.paths.cookiesPage.li2_4`) }}
        </li>
      </ul>
      <h2>
        {{ t(`footer.paths.cookiesPage.h3`) }}
      </h2>
      <p>
        {{ t(`footer.paths.cookiesPage.p3`) }}
      </p>
      <h2>
        {{ t(`footer.paths.cookiesPage.h4`) }}
      </h2>
      <p>
        {{ t(`footer.paths.cookiesPage.p4_1`) }}
        <ExternalLink :href="t(`footer.paths.cookiesPage.link_1_url`)">
          {{ t(`footer.paths.cookiesPage.link_1_text`) }}
        </ExternalLink>
        {{ t(`footer.paths.cookiesPage.p4_2`) }}
        <ExternalLink :href="t(`footer.paths.cookiesPage.link_2_url`)">
          {{ t(`footer.paths.cookiesPage.link_2_text`) }} </ExternalLink
        >.
      </p>
      <p class="p-margin-bottom-footer extra-margin-bottom">
        {{ t(`footer.paths.cookiesPage.p5`) }}
        <a href="mailto:algemeneinzage@ictu.nl"> algemeneinzage@ictu.nl</a>.
      </p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'

const { t } = useI18n()

definePageMeta({
  title: 'Cookies'
})

const pageTitle = computed(() => t('footer.paths.cookies'))
useHead({ title: pageTitle })
providePageTitle({ title: 'footer.paths.cookies', labelType: 'locale-index' })
</script>

<style lang="scss">
@media (max-width: 65em) {
  .extra-margin-bottom {
    margin-bottom: 35%;
  }
}

.green-color {
  background-color: #f0f8e8;
  margin-bottom: 0px !important;
}

.no-bottom-padding {
  padding-bottom: 0px !important;
  margin-bottom: 100px !important;
}
</style>
