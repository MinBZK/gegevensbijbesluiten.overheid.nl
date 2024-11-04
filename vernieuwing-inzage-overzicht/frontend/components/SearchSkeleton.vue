<template>
  <div class="search-skeleton">
    <div v-for="i in props.skeletonItem" :key="i" class="skeleton-item">
      <div class="skeleton-line"></div>
    </div>
  </div>
</template>

<script setup lang="ts">
const props = defineProps<{
  skeletonItem: number
}>()
</script>

<style scoped lang="scss">
.search-skeleton {
  padding: 0.5em;
}

.skeleton-item {
  margin-bottom: 0.5em;
}

.skeleton-line {
  height: 2em;
  background-color: #f0f0f0;
  border-radius: 4px;
}

@keyframes shimmer {
  0% {
    background-position: -468px 0;
  }
  100% {
    background-position: 468px 0;
  }
}

.skeleton-line {
  animation-duration: 1.5s;
  animation-fill-mode: forwards;
  animation-iteration-count: infinite;
  animation-name: shimmer;
  animation-timing-function: linear;
  background: linear-gradient(to right, #f6f6f6 8%, #f0f0f0 18%, #f6f6f6 33%);
  background-size: 800px 104px;
}
</style>
