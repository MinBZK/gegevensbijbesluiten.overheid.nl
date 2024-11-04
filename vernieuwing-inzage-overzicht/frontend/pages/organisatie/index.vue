<template>
  <div class="container">
    <SearchBar
      ref="searchbar"
      :search-explanation="p('pages: organisaties.searchText')"
      :suggestions-hidden="`pages.organisaties.suggestionsHidden`"
      @do-search="(searchtext) => doSearch(searchtext)"
    />
    <div class="row container columns no-padding">
      <div class="column-d-9">
        <h2 role="status">
          {{ t(`organisaties.foundResults`, { n: totalCountUnderlying }) }}
        </h2>
        <div v-if="oeResults.length != 0" class="row no-padding">
          <div class="column-d-6">
            <TablePagination
              v-if="nPages > 1"
              :current-page="page"
              :page-length="nPages"
              @set-page="(p) => setPage(p)"
            />
          </div>
        </div>
        <div v-if="oeResults.length != 0" class="result--list__data">
          <ul class="card-container ul-padding">
            <li v-for="(Koepel, index) in oeResults" :key="index" class="li-padding">
              <OrganisatieCard
                :set-focus="index == 0 && newFocusIsRequested"
                :title="Koepel.titel"
                :description="Koepel.omschrijving"
                :content="extractContent(Koepel)"
                :loading="loading"
                :chips="[]"
                @focus-has-been-set="() => (newFocusIsRequested = false)"
              >
              </OrganisatieCard>
            </li>
          </ul>
        </div>
        <div v-if="oeResults.length != 0" class="row no-padding">
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
          <p>{{ t('oeIndex.noResults.p1') }}</p>
          <ul class="no-results">
            <li>
              {{ t('oeIndex.noResults.l1') }}
            </li>
            <li>
              {{ t('oeIndex.noResults.l2') }}
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
import oeService from '@/services/organisatie'
import type { OeKoepel } from '~~/types/organisatie'

import type { UrlQuery } from '~/types/filter'
import type { OeContent } from '@/components/organisatie/OrganisatieCard.vue'

const { t } = useI18n()
const { p } = usePreditor()
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

let { data } = await oeService.getOeFiltered(query.value)

// Refresh data based on the URL query
const loading = ref(false)

watch(query, async () => {
  loading.value = true
  const response = await oeService.getOeFiltered(query.value)
  loading.value = false
  data = response.data
})

const page = computed(() => query.value.page)
const totalCountUnderlying = computed(() => data.value?.total_count_underlying || 0)
const totalCountKoepel = computed(() => data.value?.total_count_koepel || 0)
const oeResults = computed(() => data.value?.result_oe || [])
const nPages = computed(() => Math.ceil(totalCountKoepel.value / query.value.limit))
const scrollToCards = () => {
  searchbar.value.$el.scrollIntoView({ behavior: 'smooth' })
}

const searchbar = ref()
const setPage = (newPage: number) => {
  router.push({ query: { ...query.value, page: newPage } })
  scrollToCards()
}

// default value is true, so that when we search from the homepage the focus is always placed correctly.
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

const extractContent = (data: OeKoepel) => {
  const content = data.child_oe_struct.map((item) => ({
    link: getLink(`/organisatie/${item.child_entity.oe_upc}`).value,
    description: item.child_entity.naam_officieel || t('ontbreekt')
  }))
  content.sort((a, b) => a.description.localeCompare(b.description)) // Sort alphabetically
  return content as OeContent[]
}

const searchPageTitle = computed(() => t(`oeIndex.pageTitle`))

useHead({ title: searchPageTitle })
providePageTitle({
  title: 'oeIndex.pageTitle',
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
