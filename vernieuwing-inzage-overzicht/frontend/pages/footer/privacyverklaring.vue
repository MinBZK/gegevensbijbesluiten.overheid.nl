<template>
  <div class="container">
    <h1 class="h1 margin-top">
      {{ t('footer.paths.privacyverklaringPage.h1') }}
    </h1>

    <p class="mb-2">
      {{ t('footer.paths.privacyverklaringPage.p1') }}
    </p>
    <ul class="bullet ml-4">
      <li>
        {{ t('footer.paths.privacyverklaringPage.li1_1') }}
      </li>
      <li>
        {{ t('footer.paths.privacyverklaringPage.li1_2') }}
      </li>
      <li>
        {{ t('footer.paths.privacyverklaringPage.li1_3') }}
      </li>
      <li>
        {{ t('footer.paths.privacyverklaringPage.li1_4') }}
      </li>
    </ul>

    <p class="mb-4 mt-4">
      {{ t('footer.paths.privacyverklaringPage.p2') }}
    </p>

    <h2>
      {{ t('footer.paths.privacyverklaringPage.h2') }}
    </h2>
    <p class="p-margin-bottom-footer">
      {{ t('footer.paths.privacyverklaringPage.p3') }}
    </p>

    <h2>
      {{ t('footer.paths.privacyverklaringPage.h3') }}
    </h2>
    <p class="p-margin-bottom-footer">
      {{ t('footer.paths.privacyverklaringPage.p4') }}
    </p>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'

const { t } = useI18n()

const pageTitle = computed(() => t('footer.paths.privacyverklaring'))
useHead({ title: pageTitle })
providePageTitle({
  title: 'footer.paths.privacyverklaring',
  labelType: 'locale-index'
})
</script>
