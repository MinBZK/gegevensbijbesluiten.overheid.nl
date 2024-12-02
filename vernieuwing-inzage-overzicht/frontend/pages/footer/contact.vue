<template>
  <div class="container">
    <h1 class="h1 margin-top">{{ t('footer.paths.contactPage.h1') }}</h1>
    <p>{{ t('footer.paths.contactPage.p1') }}</p>

    <h2>{{ t('footer.paths.contactPage.h2') }}</h2>
    <p>
      {{ t('footer.paths.contactPage.p2') }}
      <a href="mailto:test@test.nl"> test@test.nl</a>.
    </p>

    <p>
      {{ t('footer.paths.contactPage.p3_1') }}
      <NuxtLink :to="'/footer/privacyverklaring'">
        {{ t('footer.paths.contactPage.p3_2') }} </NuxtLink
      >.
    </p>

    <p class="p-margin-bottom-footer extra-margin-bottom">{{ t('footer.paths.contactPage.p4') }}</p>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'

const { t } = useI18n()

definePageMeta({
  title: 'Contact'
})

const pageTitle = computed(() => t('footer.paths.contact'))
useHead({ title: pageTitle })
providePageTitle({ title: 'footer.paths.contact', labelType: 'locale-index' })
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
