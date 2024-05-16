<template>
  <a :href="fullURL" target="_blank" class="is-external-icon">
    <slot />
    <span class="visually-hidden">{{ t('externalLink') }}</span>
  </a>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useI18n } from 'vue-i18n'

const { t } = useI18n()

const props = defineProps<{ href: string }>()

const fullURL = computed(() => {
  if (props.href.startsWith('http://') || props.href.startsWith('https://')) {
    return props.href
  } else {
    return `https://${props.href}`
  }
})
</script>
