<template>
  <FilterBlock
    v-if="props.options.length > 0"
    v-model:readMore="readMore"
    :title="t('filter.filters.pickOrg')"
    disable-dropdown
    :enable-read-more="shownOptions.length != options.length"
    :enable-read-less="enableReadLess"
    :more-options-button="props.options.length > props.maxSize ? true : false"
  >
    <ul class="no-padding-left">
      <li v-for="option in shownOptions" :key="option.key">
        <a
          ref="filterListItems"
          :tabindex="0"
          class="filter-options capitalize"
          :aria-label="$t('filter.aria/add', { what: option.label })"
          @click="addNewQueryToRoute(option)"
          @keydown.enter="addNewQueryToRoute(option)"
          @keydown.space.prevent="addNewQueryToRoute(option)"
        >
          <span>
            {{ option.label }}
          </span>
          <span class="filter-option-count">
            {{ option.count }}
          </span>
        </a>
      </li>
    </ul>
  </FilterBlock>
</template>

<script setup lang="ts">
import type { UrlQuery, FilterData } from '@/types/filter'

const props = withDefaults(
  defineProps<{
    options: FilterData[]
    queryKey?: keyof UrlQuery | 'organisation'
    enableReadMore?: boolean
    enableReadLess?: boolean
    maxSize?: number
  }>(),
  {
    maxSize: 7,
    queryKey: 'organisation'
  }
)

const { t } = useI18n()

const query = computed(() => useRoute().query as UrlQuery)
const filterListItems = ref<HTMLElement[]>([])
const addNewQueryToRoute = (option: FilterData): void => {
  const newQuery = { ...query.value, page: '1' }
  newQuery[props.queryKey] = option.key
  useRouter().push({ query: newQuery })
}

const readMore = ref<boolean>(true)

const shownOptions = computed(() => {
  if ((props.options.length || 0) > props.maxSize && props.enableReadMore && readMore.value) {
    return props.options.slice(0, props.maxSize)
  } else {
    return props.options
  }
})

watch(
  () => shownOptions.value.length,
  (newLength) => {
    if (newLength === props.options.length && props.options.length > props.maxSize) {
      nextTick(() => {
        filterListItems.value[props.maxSize].focus()
      })
    } else if (filterListItems.value.length > 0 && props.options.length > props.maxSize) {
      filterListItems.value[0].focus()
    }
  }
)
</script>

<style scoped lang="scss">
.filter-options {
  width: 100%;
  display: inline-flex;
  flex-wrap: nowrap;
  justify-content: space-between;
  align-items: center;
  cursor: pointer;
}

.filter-option-count {
  margin-left: 0.5em;
  white-space: nowrap;
}
</style>
