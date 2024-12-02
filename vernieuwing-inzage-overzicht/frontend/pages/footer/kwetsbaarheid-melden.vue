<template>
  <div class="container">
    <div>
      <h1 class="h1 margin-top">{{ t(`footer.paths.kwetsbaarheidPage.h1`) }}</h1>
      <p>
        {{ t(`footer.paths.kwetsbaarheidPage.p1_1`) }}
        <a href="">
          <a href="mailto:algemeneinzage@ictu.nl">algemeneinzage@ictu.nl</a>
        </a>
        {{ t(`footer.paths.kwetsbaarheidPage.p1_2`) }}
      </p>
      <p>
        <ExternalLink :href="t(`footer.paths.kwetsbaarheidPage.li1`)">
          {{ t(`footer.paths.kwetsbaarheidPage.p2`) }} </ExternalLink
        >.
      </p>
    </div>
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
