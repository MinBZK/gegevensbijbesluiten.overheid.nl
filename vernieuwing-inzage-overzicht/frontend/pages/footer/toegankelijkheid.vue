<template>
  <div class="container">
    <div>
      <h1 class="h1 margin-top">{{ t('footer.paths.toegankelijkheid') }}</h1>

      <p>
        {{ t('footer.paths.toegankelijkheidPage.p1') }}
      </p>
      <p>
        {{ t('footer.paths.toegankelijkheidPage.p2') }}
      </p>
      <p>
        {{ t('footer.paths.toegankelijkheidPage.p3') }}
      </p>
      <p>{{ t('footer.paths.toegankelijkheidPage.p4') }}</p>
      <ul class="bullet ml-4 p-margin-bottom-footer">
        <li>
          <ExternalLink :href="t('footer.paths.toegankelijkheidPage.li1_link')">
            {{ t('footer.paths.toegankelijkheidPage.li1') }}
          </ExternalLink>
        </li>
        <!-- <li>
          <ExternalLink :href="t('footer.paths.toegankelijkheidPage.li2_link')">
            {{ t('footer.paths.toegankelijkheidPage.li2') }}</ExternalLink
          >
        </li> -->
      </ul>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'

const { t } = useI18n()

definePageMeta({
  title: 'Toegankelijkheid'
})
const pageTitle = computed(() => t('footer.paths.toegankelijkheid'))
useHead({ title: pageTitle })
providePageTitle({
  title: 'footer.paths.toegankelijkheid',
  labelType: 'locale-index'
})
</script>
