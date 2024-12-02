<template>
  <div class="container">
    <SearchBar
      ref="searchbar"
      :search-explanation="t('pages.gegevens.searchText')"
      :suggestions-hidden="`pages.gegevens.suggestionsHidden`"
      @do-search="(searchtext) => doSearch(searchtext)"
    />
    <div class="row container columns no-padding">
      <div class="column-d-9">
        <h2>
          <span role="status">
            {{ t(`gegevens.foundResults`, { n: totalCountUnderlying }) }}
          </span>
        </h2>
        <div v-if="ggResults.length != 0" class="row no-padding">
          <div class="column-d-6">
            <TablePagination
              v-if="nPages > 1"
              :current-page="page"
              :page-length="nPages"
              @set-page="(p) => setPage(p)"
            />
          </div>
        </div>
        <div v-if="ggResults.length != 0" class="result--list__data">
          <ul class="card-container ul-padding">
            <li v-for="(gg, index) in ggResults" :key="index" class="li-padding">
              <GegevenCard
                :set-focus="index == 0 && newFocusIsRequested"
                :title="gg.omschrijving"
                :description="gg.omschrijving_uitgebreid || t('ontbreekt')"
                :content="extractContent(gg)"
                :loading="loading"
                @focus-has-been-set="() => (newFocusIsRequested = false)"
              >
              </GegevenCard>
            </li>
          </ul>
        </div>
        <div v-if="ggResults.length != 0" class="row no-padding">
          <div class="column-d-6">
            <TablePagination
              v-if="nPages > 1"
              class="u-margin-top-24"
              :current-page="page"
              :page-length="nPages"
              @set-page="(p) => setPage(p)"
            />
          </div>
        </div>
        <div v-if="totalCountUnderlying == 0">
          <p>{{ t('ggIndex.noResults.p1') }}</p>
          <ul class="no-results">
            <li>
              {{ t('ggIndex.noResults.l1') }}
            </li>
            <li>
              {{ t('ggIndex.noResults.l2') }}
            </li>
          </ul>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { getLink } from '~/common/common-functions'
import ggService from '@/services/gegeven'
import type { Gg } from '~~/types/gegeven'

import type { UrlQuery } from '~/types/filter'
import type { GgContent } from '@/components/gegeven/GegevenCard.vue'

const { t } = useI18n()
const router = useRouter()

const query = computed(() => {
  const pageLength = 6
  const urlQuery = useRoute().query as UrlQuery
  return {
    ...urlQuery,
    page: +(urlQuery.page || 1),
    limit: +(urlQuery.limit || pageLength)
  }
})

let { data } = await ggService.getGgFiltered(query.value)

// Refresh data based on the URL query
const loading = ref(false)

watch(query, async () => {
  if (window.location.hash !== '#content') {
    loading.value = true
    const response = await ggService.getGgFiltered(query.value)
    loading.value = false
    data = response.data
  }
})

const page = computed(() => query.value.page)
const totalCountUnderlying = computed(() => data.value?.total_count_underlying || 0)
const totalCountKoepel = computed(() => data.value?.total_count_koepel || 0)
const ggResults = computed(() => data.value?.result_gg || [])
const nPages = computed(() => Math.ceil(totalCountKoepel.value / query.value.limit))
const scrollToCards = () => {
  searchbar.value.$el.scrollIntoView({ behavior: 'smooth' })
}

const searchbar = ref()
const setPage = (newPage: number) => {
  router.push({ query: { ...query.value, page: newPage } })
  scrollToCards()
}

// default value is false, so that when we search from the homepage the focus is always placed correctly.
const newFocusIsRequested = ref<boolean>(false)

const doSearch = (searchtext: string) => {
  const newQuery = {
    ...query.value,
    searchtext: searchtext.trim() || undefined,
    page: 1
  }
  router.push({ query: newQuery })
  newFocusIsRequested.value = true
  scrollToCards()
}

const extractContent = (data: Gg) => {
  const content = data.child_gg_struct.map((item) => ({
    link: getLink(`/gegeven/${item.child_entity.gg_upc}`).value,
    description: item.child_entity.omschrijving || t('ontbreekt')
  }))

  content.sort((a, b) => a.description.localeCompare(b.description)) // Sort alphabetically

  return content as GgContent[]
}

const searchPageTitle = computed(() => t(`ggIndex.pageTitle`))

useHead({ title: searchPageTitle })

providePageTitle({
  title: 'ggIndex.pageTitle',
  labelType: 'locale-index'
})
</script>

<style scoped lang="scss">
ul.no-results {
  list-style-image: url(@/assets/images/icons/icon-dart-right-blue.svg);
  line-height: 2 !important;
  padding-left: 3em;
  margin-bottom: 20em;
}

li {
  padding-left: 1em;
}

.card-container {
  grid-template-columns: repeat(3, 1fr);
}

@media (max-width: 50em) {
  .card-container {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 35em) {
  .card-container {
    grid-template-columns: repeat(1, 1fr);
  }
}
</style>
