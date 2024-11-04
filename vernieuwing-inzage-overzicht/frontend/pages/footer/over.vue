<template>
  <div class="container">
    <h1 class="h1 margin-top">{{ t(`footer.paths.overPage.title`) }}</h1>
    <p>
      {{ t(`footer.paths.overPage.p0_1`) }}
    </p>
    <p>
      {{ t(`footer.paths.overPage.p0_2`) }}
      <a href="mailto:test@test.nl"> test@test.nl</a>.
    </p>
    <h2>{{ t(`footer.paths.overPage.h1`) }}</h2>
    <p>
      {{ t(`footer.paths.overPage.p1_1`) }}
    </p>
    <p>
      {{ t(`footer.paths.overPage.p1_2`) }}
    </p>
    <ul class="bullet ml-4">
      <li>{{ t(`footer.paths.overPage.li1_1`) }}</li>
      <li>
        {{ t(`footer.paths.overPage.li1_2`) }}
      </li>
      <li>
        {{ t(`footer.paths.overPage.li1_3`) }}
      </li>
      <li>
        {{ t(`footer.paths.overPage.li1_4`) }}
      </li>
    </ul>
    <h2>{{ t(`footer.paths.overPage.h2`) }}</h2>
    <p>
      {{ t(`footer.paths.overPage.p2_1`) }}
    </p>
    <p>
      {{ t(`footer.paths.overPage.p2_2`) }}
    </p>
    <ul class="bullet ml-4">
      <li>{{ t(`footer.paths.overPage.li2_1`) }}</li>
      <li>{{ t(`footer.paths.overPage.li2_2`) }}</li>
      <li>{{ t(`footer.paths.overPage.li2_3`) }}</li>
      <li>{{ t(`footer.paths.overPage.li2_4`) }}</li>
      <li>{{ t(`footer.paths.overPage.li2_5`) }}</li>
    </ul>

    <p>
      {{ t(`footer.paths.overPage.p2_3`) }}
      <a href="mailto:test@test.nl"> test@test.nl</a>.
    </p>
    <h2>{{ t(`footer.paths.overPage.h3`) }}</h2>
    <p>
      {{ t(`footer.paths.overPage.p3_1`) }}
    </p>
    <h2>{{ t(`footer.paths.overPage.h4`) }}</h2>
    <p>
      {{ t(`footer.paths.overPage.p4_1`) }}
    </p>
    <p>
      {{ t(`footer.paths.overPage.p4_2`) }}
    </p>
    <p class="p-margin-bottom-footer">
      {{ t(`footer.paths.overPage.p4_3`) }}
    </p>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'

const { t } = useI18n()

const pageTitle = computed(() => t('footer.paths.overPage.title'))
useHead({ title: pageTitle })
providePageTitle({
  title: 'footer.paths.overPage.title',
  labelType: 'locale-index'
})
</script>
