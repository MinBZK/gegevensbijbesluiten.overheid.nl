<template>
  <div class="container">
    <SearchBar
      ref="searchbar"
      :search-explanation="p('pages: organisaties.searchText')"
      @do-search="doSearch"
    />
    <div class="row container columns no-padding">
      <div class="column-d-9">
        <h2 role="status">
          {{ t(`organisaties.foundResults`, { n: totalCount }) }}
          {{ readTitle ? '&nbsp;' : null }}
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
          <div class="card-container ul-padding">
            <div v-for="(oe, index) in oeResults" :key="index">
              <OrganisatiesCard
                :set-focus="index == 0 && newFocusIsRequested"
                :title="oe.naam_officieel"
                :content="extractContent(oe)"
                :loading="loading"
                :chips="[]"
                @focus-has-been-set="() => (newFocusIsRequested = false)"
              >
              </OrganisatiesCard>
            </div>
          </div>
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
        <div v-if="totalCount == 0">
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
import oeService from '~~/services/organisaties'
import type { Oe } from '~~/types/organisaties'

import type { UrlQuery } from '~/types/filter'
import type { OeContent } from '@/components/organisaties/OrganisatiesCard.vue'

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
const totalCount = computed(() => data.value?.total_count || 0)
const oeResults = computed(() => data.value?.results || [])
const nPages = computed(() => Math.ceil(totalCount.value / query.value.limit))

const searchbar = ref()
const setPage = (newPage: number) => {
  router.push({ query: { ...query.value, page: newPage } })
  searchbar.value.$el.scrollIntoView({ behavior: 'smooth' })
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

  // In some situations, say the page title again. Everytime state changes, the title is updated and read.
  readTitle.value = !readTitle.value
}

// TODO implement me
const extractContent = (data: Oe) => {
  const content = data.child_oe_struct.map((item) => ({
    link: getLink(`/organisaties/${item.child_entity.oe_upc}`, 0).value,
    description: item.child_entity.naam_officieel || t('ontbreekt'),
  }))
  content.sort((a, b) => a.description.localeCompare(b.description)) // Sort alphabetically
  return content as OeContent[]
}

// const extractContent = (data: Oe) => {
//   // placeholder until proper backend
//   const content = [
//     {
//       link: getLink(`/organisaties/${data.oe_upc}`, 0).value,
//       description: data.naam_officieel || t('ontbreekt'),
//     },
//   ]
//   return content as OeContent[]
// }

const searchPageTitle = computed(() => t(`oeIndex.pageTitle`))

useHead({ title: searchPageTitle })
providePageTitle({
  title: 'oeIndex.pageTitle',
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
