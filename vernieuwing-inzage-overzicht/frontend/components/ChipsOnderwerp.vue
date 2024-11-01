<template>
  <div class="chips-container">
    <span v-for="(chip, index) in props.chips" :key="index" class="chip">
      <span class="chip-text">{{ chip }}</span>
    </span>
  </div>
</template>

<script setup lang="ts">
const props = defineProps({
  chips: {
    type: Array,
    required: true
  }
})
</script>

<style scoped lang="scss">
.chips-container {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}
.chip {
  border: 1px solid $primary-dark;
  border-radius: 30px;
  margin-left: 0;
  padding: 8px 12px;
}

.chip-text {
  font-style: italic;
  color: $primary-dark;
}
</style>
