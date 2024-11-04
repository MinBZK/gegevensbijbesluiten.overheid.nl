<template>
  <div ref="blockSearch" class="block-search">
    <div class="columns">
      <div class="column column-d-5">
        <div class="form__row">
          <label id="search-label" class="form__label form__label--accent">{{
            searchExplanation
          }}</label>

          <div class="wrapper-searchbar">
            <input
              id="input-text-98789"
              ref="searchInput"
              v-model="searchValue"
              type="text"
              name="98789"
              class="input input-text"
              aria-invalid="false"
              aria-labelledby="search-label"
              autocomplete="off"
              :placeholder="searchHint"
              :aria-expanded="showSuggestions"
              @keyup.enter="getPage !== 'index' && doSearch()"
              @keydown.esc="hideSuggestions"
              @focus="handleInputFocus"
            />
          </div>
          <div v-if="showSuggestions" class="suggestions-wrapper">
            <div v-if="getPage === 'index'" class="suggestions-index">
              <template v-for="entityType in ['evtp', 'gg', 'oe']" :key="entityType">
                <b class="entity-title">{{
                  `${getEntityTitle(entityType)} (${getTotalSuggestions(entityType)})`
                }}</b>
                <div v-if="getTotalSuggestions(entityType) > 0" class="entity-suggestions">
                  <ul class="suggestion-list">
                    <li
                      v-for="suggestion in getLimitedSuggestions(entityType)"
                      :key="suggestion.upc"
                      class="suggestion-item"
                    >
                      <NuxtLink
                        :to="
                          getLink(
                            `/${getEntityPath(entityType)}/${suggestion.upc}`,
                            suggestion.version
                          ).value
                        "
                        class="suggestion-link"
                      >
                        {{ capitaliseFirstLetter(suggestion.title) }}
                      </NuxtLink>
                    </li>
                  </ul>
                  <div
                    v-if="getSuggestionsHiddenCount(entityType) > 0"
                    class="suggestion-footer"
                    @click="showAllSuggestions(entityType)"
                  >
                    {{ getSuggestionHiddenText(entityType) }}
                  </div>
                </div>
                <div
                  v-else-if="entitiesWithNoResults.has(entityType)"
                  class="suggestion-item-notfound"
                >
                  {{ t('noResultsSuggestionsList') }}
                </div>
                <SearchSkeleton v-else :skeleton-item="3" />
              </template>
            </div>
            <div v-else class="suggestions-single-entity">
              <div v-if="getTotalSuggestions(entity) > 0">
                <ul class="suggestion-list">
                  <li
                    v-for="suggestion in getLimitedSuggestions(entity)"
                    :key="suggestion.upc"
                    class="suggestion-item"
                  >
                    <NuxtLink
                      :to="
                        getLink(`/${getEntityPath(entity)}/${suggestion.upc}`, suggestion.version)
                          .value
                      "
                      class="suggestion-link"
                    >
                      {{ capitaliseFirstLetter(suggestion.title) }}
                    </NuxtLink>
                  </li>
                </ul>
                <div
                  v-if="getSuggestionsHiddenCount(entity) > 0"
                  class="suggestion-footer"
                  @click="showAllSuggestions(entity)"
                >
                  {{ getSuggestionHiddenText(entity) }}
                </div>
              </div>
              <div v-else>
                <SearchSkeleton :skeleton-item="3" />
              </div>
            </div>
          </div>
          <div
            v-else-if="showNoResultsMessage"
            class="suggestions-wrapper suggestion-item-notfound-single-entity"
          >
            {{ t('noResultsSuggestionsListAll') }}
          </div>
        </div>
      </div>
      <div v-if="getPage !== 'index'" class="column column-d-0.5">
        <div class="form__row">
          <FormOverheidButton
            class="button--align-to-search-field"
            :label="search"
            icon="ic:round-search"
            :full-width="true"
            @click="() => doSearch()"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { watchDebounced } from '@vueuse/core'
import SearchSkeleton from './SearchSkeleton.vue'
import evtpService from '~~/services/besluit'
import type { SearchSuggestionsAllEntities, SearchSuggestion } from '~~/types/besluit'
import { getLink, capitaliseFirstLetter } from '~/common/common-functions'

const { t } = useI18n()

const emit = defineEmits<{
  (e: 'doSearch', searchValue: string): void
}>()

const props = defineProps<{
  searchExplanation: string
  suggestionsHidden: string
}>()

const searchValue = ref(useRoute().query.searchtext || '')
const searchInput = ref<HTMLInputElement | null>(null)
const maxSuggestions = ref<number>(3)
const showingAllSuggestions = ref<boolean>(false)
const suggestionsContainer = ref<HTMLElement | null>(null)
const blockSearch = ref<HTMLElement | null>(null)
const showSuggestions = ref(false)
const getPage = useRouter().currentRoute.value.name as
  | 'index'
  | 'besluit'
  | 'gegeven'
  | 'organisatie'
const search = computed(() => t('search'))
const searchHint = computed(() => t('searchHint'))
const searchExplanation = props.searchExplanation
const suggestionsResultsAllEntities = ref<SearchSuggestionsAllEntities>()
const suggestionsResultsEntity = ref<SearchSuggestion[]>([])
const isLoading = ref(false)
const shouldShowNoResults = ref(false)
const entitiesWithNoResults = ref<Set<string>>(new Set())

const startNoResultsTimeout = () => {
  shouldShowNoResults.value = false
  setTimeout(() => {
    shouldShowNoResults.value = true
  }, 100)
}

const startNoResultsTimeoutForEntity = (entityType: string) => {
  setTimeout(() => {
    if (getTotalSuggestions(entityType) === 0) {
      entitiesWithNoResults.value.add(entityType)
    }
  }, 100)
}

const maxSuggestionsPerEntity = ref<{ [key: string]: number }>({
  evtp: maxSuggestions.value,
  gg: maxSuggestions.value,
  oe: maxSuggestions.value
})

const showingAllSuggestionsPerEntity = ref<{ [key: string]: boolean }>({
  evtp: showSuggestions.value,
  gg: showSuggestions.value,
  oe: showSuggestions.value
})

const getSuggestionHiddenText = (entityType: string) => {
  switch (entityType) {
    case 'evtp':
      return t('pages.besluiten.suggestionsHidden', { n: getSuggestionsHiddenCount(entityType) })
    case 'gg':
      return t('pages.gegevens.suggestionsHidden', { n: getSuggestionsHiddenCount(entityType) })
    case 'oe':
      return t('pages.organisaties.suggestionsHidden', { n: getSuggestionsHiddenCount(entityType) })
    default:
      return ''
  }
}

const getEntityTitle = (entityType: string) => {
  switch (entityType) {
    case 'evtp':
      return t('pages.besluiten.title')
    case 'gg':
      return t('pages.gegevens.title')
    case 'oe':
      return t('pages.organisaties.title')
    default:
      return ''
  }
}
const getEntityPath = (entityType: string) => {
  switch (entityType) {
    case 'evtp':
      return 'besluit'
    case 'gg':
      return 'gegeven'
    case 'oe':
      return 'organisatie'
    default:
      return ''
  }
}

const getLimitedSuggestions = (entityType: string) => {
  if (getPage === 'index') {
    return (
      suggestionsResultsAllEntities.value?.[entityType]?.slice(
        0,
        maxSuggestionsPerEntity.value[entityType]
      ) || []
    )
  } else {
    return suggestionsResultsEntity.value.slice(0, maxSuggestions.value)
  }
}

const getSuggestionsHiddenCount = (entityType: string) => {
  if (getPage === 'index') {
    return Math.max(
      0,
      (suggestionsResultsAllEntities.value?.[entityType]?.length || 0) -
        maxSuggestionsPerEntity.value[entityType]
    )
  } else {
    return Math.max(0, suggestionsResultsEntity.value.length - maxSuggestions.value)
  }
}

const getTotalSuggestions = (entityType: string) => {
  if (getPage === 'index') {
    return suggestionsResultsAllEntities.value?.[entityType]?.length || 0
  } else {
    return suggestionsResultsEntity.value.length
  }
}
const hideSuggestions = () => {
  showSuggestions.value = false
  resetContainerPadding()
}

const showSuggestionsAndAdjustPadding = () => {
  showSuggestions.value = true
  nextTick(() => {
    adjustContainerPadding()
  })
}

const handleClickOutside = (event: MouseEvent) => {
  const target = event.target as HTMLElement
  if (blockSearch.value && !blockSearch.value.contains(target)) {
    hideSuggestions()
    showTopSuggestions()
  }
}

const doSearch = () => {
  const router = useRouter()
  router.push({
    name: 'besluit',
    query: {
      searchtext: searchValue.value,
      scrollTo: 'searchbar'
    }
  })
  emit('doSearch', searchValue.value as string)
  hideSuggestions()
}

const entity = computed(() => {
  switch (getPage) {
    case 'besluit':
      return 'evtp'
    case 'gegeven':
      return 'gg'
    case 'organisatie':
      return 'oe'
    case 'index':
      return 'common'
    default:
      return 'evtp'
  }
})

const fetchSearchSuggestions = async () => {
  isLoading.value = true
  shouldShowNoResults.value = false
  entitiesWithNoResults.value.clear()
  // await new Promise(resolve => setTimeout(resolve, 100)); // 500ms delay
  const response = await evtpService.getSearchSuggestion(entity.value, searchValue.value.toString())
  isLoading.value = false
  suggestionsResultsAllEntities.value = response.data.value || { evtp: [], gg: [], oe: [] }
  if (entity.value !== 'common') {
    suggestionsResultsEntity.value = suggestionsResultsAllEntities.value[entity.value]
  }

  const hasSuggestions = Object.values(suggestionsResultsAllEntities.value).some(
    (arr) => arr.length > 0
  )

  if (hasSuggestions) {
    showSuggestionsAndAdjustPadding()
    if (getPage === 'index') {
      ;['evtp', 'gg', 'oe'].forEach((entityType) => {
        if (getTotalSuggestions(entityType) === 0) {
          startNoResultsTimeoutForEntity(entityType)
        }
      })
    } else if (suggestionsResultsEntity.value.length === 0) {
      startNoResultsTimeout()
    }
  } else {
    hideSuggestions()
    startNoResultsTimeout()
  }
}

const showAllSuggestions = (entityType: string) => {
  if (getPage === 'index') {
    maxSuggestionsPerEntity.value[entityType] =
      suggestionsResultsAllEntities.value?.[entityType]?.length || 0
    showingAllSuggestionsPerEntity.value[entityType] = true
  } else {
    maxSuggestions.value = suggestionsResultsEntity.value.length
    showingAllSuggestions.value = true
  }
  nextTick(() => {
    adjustContainerPadding()
  })
}
const checkIfSuggestionsAreNull = computed((): boolean => {
  const suggestions = suggestionsResultsAllEntities.value

  if (!suggestions) {
    return false
  }

  const { evtp, gg, oe, ...otherKeys } = suggestions

  const areSpecificKeysEmpty = evtp.length === 0 && gg.length === 0 && oe.length === 0

  const areOtherKeysEmpty = Object.values(otherKeys).every((arr) => arr.length === 0)

  return areSpecificKeysEmpty && areOtherKeysEmpty
})

const showNoResultsMessage = computed(() => {
  return (
    !isLoading.value &&
    shouldShowNoResults.value &&
    checkIfSuggestionsAreNull.value &&
    searchValue.value.length > 2
  )
})

const showTopSuggestions = () => {
  if (getPage === 'index') {
    Object.keys(maxSuggestionsPerEntity.value).forEach((key) => {
      maxSuggestionsPerEntity.value[key] = 3
      showingAllSuggestionsPerEntity.value[key] = false
    })
  } else {
    maxSuggestions.value = 3
    showingAllSuggestions.value = false
  }
  nextTick(() => {
    resetContainerPadding()
  })
}

const adjustContainerPadding = () => {
  if (blockSearch.value && suggestionsContainer.value) {
    const suggestionsHeight = suggestionsContainer.value.offsetHeight
    blockSearch.value.style.paddingBottom = `${suggestionsHeight}px`
  }
}

const resetContainerPadding = () => {
  if (blockSearch.value) {
    blockSearch.value.style.paddingBottom = '27px'
  }
}

const handleInputFocus = () => {
  if (
    searchValue.value.length > 2 &&
    (suggestionsResultsEntity.value.length > 0 ||
      Object.values(suggestionsResultsAllEntities.value || {}).some((arr) => arr.length > 0))
  ) {
    showSuggestionsAndAdjustPadding()
  }
}

watchDebounced(
  searchValue,
  async () => {
    if (searchValue.value.length > 2) {
      showSuggestionsAndAdjustPadding()
      await fetchSearchSuggestions()
    } else {
      suggestionsResultsEntity.value = []
      suggestionsResultsAllEntities.value = { evtp: [], gg: [], oe: [] }
      hideSuggestions()
    }
  }
  // { debounce: 300 }
)

onMounted(() => {
  document.addEventListener('mousedown', handleClickOutside)
  window.addEventListener('resize', adjustContainerPadding)
})

onUnmounted(() => {
  document.removeEventListener('mousedown', handleClickOutside)
  window.removeEventListener('resize', adjustContainerPadding)
})
</script>

<style scoped lang="scss">
.wrapper-searchbar {
  display: flex;
}

.dropdown {
  background-color: $primary;
  color: white;
  border-radius: 0.25em;
  border-top-right-radius: 0px;
  border-bottom-right-radius: 0px;
  width: 200px;
}

.dropdown-item {
  background-color: $secondary;
  color: black;
}

.button--align-to-search-field {
  margin-top: 1.75em;
}

@media (max-width: 65em) {
  .button--align-to-search-field {
    margin-top: 0.6em;
  }
}

.form__label {
  margin-bottom: 0.5em !important;
}

.block-search {
  scroll-margin-top: 1em;
  position: relative;
  padding-bottom: 27px;
  transition: padding-bottom 0.3s ease;
}

.suggestions {
  border: 1px solid #ccc;
  max-height: none;
  overflow-y: hidden;
  background-color: white;
  width: 100%;
  position: absolute;
  z-index: 1;
  border-radius: 0.25em;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);

  &.show-all {
    max-height: 200px;
    overflow-y: auto;
  }
}

.suggestion-footer {
  padding: 0.6em;
  background-color: #f5f5f5;
  border-top: 1px solid #eee;
  font-size: 0.9em;
  color: #666;
  text-align: center;
  cursor: pointer;

  &:hover {
    background-color: #e6e6e6;
  }
}

.clickable {
  user-select: none;
}

.suggestion-item {
  padding: 0.6em;
  border-bottom: 1px solid #eee;
  transition: background-color 0.2s ease;

  &:last-child {
    border-bottom: none;
  }

  &:hover {
    background-color: $tertiary;
  }

  a {
    display: block;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    transform: underline;
  }
}

.suggestion-item-notfound {
  padding: 0.5em;
}
.suggestion-item-notfound-single-entity {
  padding: 1.2em;
}
.no-margin-bottom {
  margin-bottom: 0;
}

.suggestions-wrapper {
  border: 1px solid #ccc;
  background-color: white;
  width: 100%;
  z-index: 10;
  border-radius: 0.25em;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  max-height: 400px;
  overflow-y: auto;
}

.suggestions-index,
.suggestions-single-entity {
  padding: 0.5em;
}

.entity-suggestions {
  margin-bottom: 1em;
  border-bottom: 1px solid #eee;

  &:last-child {
    margin-bottom: 0;
  }
}

.entity-title {
  font-size: 1em;
  font-weight: bold;
  margin-bottom: 0.5em;
  padding-left: 0.1em;
}

.suggestion-list {
  list-style-type: none;
  padding: 0;
  margin: 0;
}

.suggestion-link {
  display: block;
  text-decoration: none;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;

  &:hover {
    text-decoration: underline;
  }
}

.suggestion-footer {
  padding: 0.6em;
  background-color: #f5f5f5;
  font-size: 0.9em;
  color: $primary;
  text-align: center;
  cursor: pointer;
  transition: background-color 0.2s ease;

  &:hover {
    background-color: darken(#f5f5f5, 5%);
  }
}
</style>
