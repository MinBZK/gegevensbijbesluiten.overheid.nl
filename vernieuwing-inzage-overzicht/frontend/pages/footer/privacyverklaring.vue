<template>
  <div class="container">
    <h1 class="h1 margin-top">
      {{ t('footer.paths.privacyverklaringPage.h1') }}
    </h1>

    <p>{{ t('footer.paths.privacyverklaringPage.p1') }}</p>

    <h2>{{ t('footer.paths.privacyverklaringPage.h2') }}</h2>
    <p>{{ t('footer.paths.privacyverklaringPage.p2') }}</p>

    <h2>{{ t('footer.paths.privacyverklaringPage.h3') }}</h2>
    <p>{{ t('footer.paths.privacyverklaringPage.p3') }}</p>

    <p class="p-margin-bottom-footer">
      {{ t('footer.paths.privacyverklaringPage.p4') }}
      <a href="mailto:algemeneinzage@ictu.nl"> algemeneinzage@ictu.nl</a>.
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
