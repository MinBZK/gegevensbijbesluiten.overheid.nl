<template>
  <div class="container">
    <div>
      <h1 class="h1 margin-top">{{ t(`footer.paths.copyrightPage.h1`) }}</h1>
      <p>
        {{ t(`footer.paths.copyrightPage.p1`) }}
      </p>
      <h2>
        {{ t(`footer.paths.copyrightPage.h2`) }}
      </h2>
      <p>
        {{ t(`footer.paths.copyrightPage.p2`) }}
      </p>
      <ul class="bullet ml-4">
        <li>{{ t(`footer.paths.copyrightPage.li1`) }}</li>
        <li>{{ t(`footer.paths.copyrightPage.li2`) }}</li>
        <li>{{ t(`footer.paths.copyrightPage.li3`) }}</li>
      </ul>
      <h2>
        {{ t(`footer.paths.copyrightPage.h3`) }}
      </h2>
      <p>
        {{ t(`footer.paths.copyrightPage.p3`) }}
      </p>
      <h2>
        {{ t(`footer.paths.copyrightPage.h4`) }}
      </h2>
      <p class="p-margin-bottom-footer extra-margin-bottom">
        {{ t(`footer.paths.copyrightPage.p4`) }}
        <a href="mailto:algemeneinzage@ictu.nl"> algemeneinzage@ictu.nl</a>.
      </p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'

const { t } = useI18n()

definePageMeta({
  title: 'Copyright'
})

const pageTitle = computed(() => t('footer.paths.copyright'))
useHead({ title: pageTitle })
providePageTitle({ title: 'footer.paths.copyright', labelType: 'locale-index' })
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
