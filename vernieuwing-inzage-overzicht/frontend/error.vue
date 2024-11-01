<template>
  <NuxtLayout>
    <div class="container">
      <h1 class="h1-error">{{ t('error.pageNotFound') }}</h1>
      <FormOverheidButton :label="t('error.goToHome')" @click="reloadHomePage" />
    </div>
  </NuxtLayout>
</template>

<script setup lang="ts">
// ensure preditor data is still applied
import type { SupportingText } from './types/preditor'
import { getAllContent } from './services/preditor'
const supportingText = useState<SupportingText | null>('supportingText', () => null)
const { data } = await getAllContent()
supportingText.value = data.value

const { t } = useI18n()

// render error page
defineProps<{ error: Error | Object }>()

const pageTitle = computed(() => t('error.pageNotFound'))

const reloadHomePage = () => {
  const router = useRouter()
  const homePagePath = router.resolve({ name: 'index' }).href
  window.location.href = homePagePath
}

useHead({ title: pageTitle })
</script>

<style>
.h1-error {
  padding-top: 1em;
}
</style>
