<template>
  <div class="container">
    <div class="section">
      <OnderwerpenCards :number-of-tiles="12" :show-icons="true" />
    </div>
  </div>
</template>

<script setup lang="ts">
const { t } = useI18n()
useHead({ title: t('navigation.onderwerp') })
</script>

<style scoped lang="scss">
.section {
  display: flex;
  flex-direction: column;
  align-items: center;
  row-gap: 0.25em;
  margin: 7em 0em 4em 0em;
  @media (max-width: 50em) {
    margin: 6em 0em 3em 0em;
  }
}
</style>
