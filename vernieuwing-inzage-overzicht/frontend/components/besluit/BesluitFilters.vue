<template>
  <div v-if="filterData && selectedFilters">
    <template v-if="!isMobile || showFilterForArchive">
      <FilterSelectedFilters
        v-if="selectedFilters.length"
        :selected-filters="selectedFilters"
        class="selected-filter"
      />
      <FilterSingleSelect
        v-if="!orgFilterActive"
        :options="filterData.organisation"
        enable-read-more
        enable-read-less
        :max-size="7"
      />
    </template>
    <template v-else>
      <div class="mobile-filters">
        <FilterMobileFilter>
          <h1 id="filter-title">{{ t('filters') }}</h1>
          <FilterSelectedFilters
            v-if="selectedFilters.length"
            :selected-filters="selectedFilters"
            class="selected-filter"
          />
          <FilterSingleSelect
            v-if="!orgFilterActive"
            :options="filterData.organisation"
            enable-read-more
            enable-read-less
            :max-size="7"
          />
        </FilterMobileFilter>
        <FilterMobileSelectedFilters :selected-filters="selectedFilters" />
      </div>
    </template>
  </div>
</template>

<script setup lang="ts">
import type { BesluitFilterData, SelectedFilter } from '@/types/filter'
import { useMobileBreakpoint } from '~~/composables/mobile'

const { t } = useI18n()

const props = defineProps<{
  selectedFilters?: SelectedFilter[]
  filterData?: BesluitFilterData
}>()

const isMobile = useMobileBreakpoint().small
const showFilterForArchive = ref(true as boolean)

const orgFilterActive = computed(() => {
  return !!props.selectedFilters?.find((filter) => filter.key === 'organisation')
})

onMounted(() => {
  showFilterForArchive.value = false
})
</script>

<style scoped lang="scss">
.selected-filter {
  margin-bottom: 0.5em;
}

.mobile-filters {
  margin-bottom: 1.25em;
}
</style>
