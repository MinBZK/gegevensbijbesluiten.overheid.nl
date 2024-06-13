<template>
  <div class="container">
    <OnderwerpenCards
      :number-of-tiles="12"
      :show-icons="true"
      class="tiles-container"
    />
  </div>
</template>

<script setup lang="ts">
const { t } = useI18n()
useHead({ title: t('navigation.onderwerp') })
</script>

<style scoped lang="scss">
.tiles-container {
  margin: 7em 0em 4em 0em;

  @media (max-width: 50em) {
    margin: 6em 0em 3em 0em;
  }
}
</style>
