<template>
  <div class="container">
    <SearchBar
      ref="searchbar"
      :search-explanation="p('pages: gegevens.searchText')"
      @do-search="doSearch"
    />
    <div class="row container columns no-padding">
      <div class="column-d-9">
        <h2 role="status">
          {{ t(`gegevens.foundResults`, { n: totalCount }) }}
          {{ readTitle ? '&nbsp;' : null }}
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
          <div class="card-container ul-padding">
            <div v-for="(gg, index) in ggResults" :key="index">
              <GegevensCard
                :set-focus="index == 0 && newFocusIsRequested"
                :title="gg.omschrijving"
                :description="gg.omschrijving_uitgebreid || t('ontbreekt')"
                :content="extractContent(gg)"
                :loading="loading"
                :chips="[]"
                @focus-has-been-set="() => (newFocusIsRequested = false)"
              >
              </GegevensCard>
            </div>
          </div>
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
        <div v-if="totalCount == 0">
          <p>{{ t('ggIndex.noResults.p1') }}</p>
          <ul class="no-results">
            <li>
              {{ t('ggIndex.noResults.l1') }}
            </li>
            <li>
              {{ t('ggIndex.noResults.l2') }}
            </li>
            <li>
              {{ t('ggIndex.noResults.l3') }}
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
import ggService from '~~/services/gegevens'
import type { Gg } from '~~/types/gegevens'

import type { UrlQuery } from '~/types/filter'
import type { GgContent } from '@/components/gegevens/GegevensCard.vue'

const { t } = useI18n()
const { p } = usePreditor()
const router = useRouter()

const query = computed(() => {
  const pageLength = 6
  const urlQuery = useRoute().query as UrlQuery
  return {
    ...urlQuery,
    page: +(urlQuery.page || 1),
    limit: +(urlQuery.limit || pageLength),
  }
})

let { data } = await ggService.getGgFiltered(query.value)

// Refresh data based on the URL query
const loading = ref(false)

watch(query, async () => {
  loading.value = true
  const response = await ggService.getGgFiltered(query.value)
  loading.value = false
  data = response.data
})

const page = computed(() => query.value.page)
const totalCount = computed(() => data.value?.total_count || 0)
const ggResults = computed(() => data.value?.results || [])
const nPages = computed(() => Math.ceil(totalCount.value / query.value.limit))
const scrollToCards = () => {
  searchbar.value.$el.scrollIntoView({ behavior: 'smooth' })
}

const searchbar = ref()
const setPage = (newPage: number) => {
  router.push({ query: { ...query.value, page: newPage } })
  scrollToCards()
}

const readTitle = ref<boolean>(false)
// default value is true, so that when we search from the homepage the focus is always placed correctly.
const newFocusIsRequested = ref<boolean>(false)

const doSearch = (searchtext: string) => {
  const newQuery = {
    ...query.value,
    searchtext: searchtext || undefined,
    page: 1,
  }
  router.push({ query: newQuery })
  newFocusIsRequested.value = true
  scrollToCards()

  // In some situations, say the page title again. Everytime state changes, the title is updated and read.
  readTitle.value = !readTitle.value
}

const extractContent = (data: Gg) => {
  const content = data.child_gg_struct.map((item) => ({
    link: getLink(`/gegevens/${item.child_entity.gg_upc}`, 0).value,
    description: item.child_entity.omschrijving || t('ontbreekt'),
  }))

  content.sort((a, b) => a.description.localeCompare(b.description)) // Sort alphabetically

  return content as GgContent[]
}

const searchPageTitle = computed(() => t(`ggIndex.pageTitle`))

useHead({ title: searchPageTitle })

providePageTitle({
  title: 'ggIndex.pageTitle',
  labelType: 'locale-index',
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
