<template>
  <div>
    <span v-for="(chip, index) in props.chips" :key="index" class="chip">
      <span class="chip-text">{{ chip }}</span>
    </span>
  </div>
</template>

<script setup lang="ts">
const props = defineProps({
  chips: {
    type: Array,
    required: true,
  },
})
</script>

<style scoped lang="scss">
.chip {
  border: 1px solid $primary-dark;
  border-radius: 30px;
  margin: 4px;
  margin-left: 0;
  padding: 8px 12px;
}

.chip-text {
  font-style: italic;
  color: $primary-dark;
}
</style>
