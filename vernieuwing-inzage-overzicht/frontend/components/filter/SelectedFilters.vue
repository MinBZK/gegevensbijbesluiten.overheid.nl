<template>
  <FilterBlock
    disable-dropdown
    :title="t('filter.selectedFilter.selectedFilters')"
  >
    <div v-for="filter in selectedFilters" :key="filter.key">
      <strong>{{ t('filter.selectedFilter.' + filter.key) }}:</strong> <br />
      <RouterLink
        class="chosen-filter"
        :aria-label="$t('filter.aria/remove', { what: filter.value }) || ''"
        :to="filterRemoved(filter)"
      >
        {{ filter.value }}
        <img src="@/assets/images/icons/icon-close.svg" aria-hidden alt="" />
      </RouterLink>
    </div>
  </FilterBlock>
</template>

<script setup lang="ts">
import type { SelectedFilter, UrlQuery } from '@/types/filter'

const { t } = useI18n()

defineProps<{
  selectedFilters: SelectedFilter[]
}>()

const currentQuery = computed(() => useRoute().query as UrlQuery)

const filterRemoved = (filter: SelectedFilter) => {
  const query = { ...currentQuery.value }
  if (filter.key in query) {
    delete query[filter.key]
  }
  return { query }
}
</script>

<style scoped lang="scss">
.chosen-filter {
  width: 100%;
  display: inline-flex;
  flex-wrap: nowrap;
  justify-content: space-between;
  align-items: center;

  img {
    height: 0.75em;
  }
}
</style>
