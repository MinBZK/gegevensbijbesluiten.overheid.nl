<template>
  <NuxtLayout>
    <!-- using http for configs is bodgy, but the useColorMode() method causes hydration issues -->
    <div class="display-none">
      {{ ($colorMode.preference = useRuntimeConfig().public.colorMode) }}
    </div>
    <NuxtPage />
  </NuxtLayout>
</template>

<script setup lang="ts">
import type { SupportingText } from './types/preditor'
import { getAllContent } from './services/preditor'
const supportingText = useState<SupportingText | null>(
  'supportingText',
  () => null
)

const { data } = await getAllContent()
supportingText.value = data.value
</script>

<style>
.display-none {
  display: none;
}
</style>
