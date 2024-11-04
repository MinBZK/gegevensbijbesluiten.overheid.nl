<template>
  <div class="container">
    <SearchBar
      ref="searchbar"
      :search-explanation="t('pages.besluiten.searchText')"
      :suggestions-hidden="`pages.besluiten.suggestionsHidden`"
      @do-search="(searchtext) => doSearch(searchtext)"
    />
    <div class="row container columns no-padding">
      <div class="column-d-3">
        <BesluitFilters
          :selected-filters="data?.selected_filters"
          :filter-data="data?.filter_data"
        />
      </div>
      <div class="column-d-9">
        <h2 role="status">
          {{ t(`besluiten.foundResults`, { n: totalCount }) }}
        </h2>
        <div v-if="evtps.length != 0" class="row no-padding">
          <div class="column-d-6">
            <TablePagination
              v-if="nPages > 1"
              :current-page="page"
              :page-length="nPages"
              @set-page="(p) => setPage(p)"
            />
          </div>
        </div>
        <div v-if="evtps.length != 0" class="result--list__data">
          <ul class="card-container ul-padding">
            <li v-for="(evtp, index) in evtps" :key="index" class="li-padding">
              <BesluitCard
                :set-focus="index == 0 && newFocusIsRequested"
                :title="evtp.evtp_nm"
                :description="evtp.omschrijving"
                :content="extractContent(evtp)"
                :link="getLink(`/besluit/${evtp.evtp_upc}`, evtp.versie_nr).value"
                :version="evtp.versie_nr"
                :chips="evtp.entities_evtp_ond.map((item) => item.entity_ond.titel)"
                :loading="loading"
                @focus-has-been-set="() => (newFocusIsRequested = false)"
              >
              </BesluitCard>
            </li>
          </ul>
        </div>
        <TablePagination
          v-if="nPages > 1"
          class="u-margin-top-24"
          :current-page="page"
          :page-length="nPages"
          @set-page="(p) => setPage(p)"
        />
        <div v-if="totalCount == 0">
          <p>{{ t('evtpIndex.noResults.p1') }}</p>
          <ul class="no-results">
            <li>
              {{ t('evtpIndex.noResults.l1') }}
            </li>
            <li>
              {{ t('evtpIndex.noResults.l2') }}
            </li>
            <li>
              {{ t('evtpIndex.noResults.l3') }}
            </li>
          </ul>
        </div>
        <div v-if="totalCount != 0" class="column-d-6" :class="!isMobile && 'align-right'">
          <FormOverheidButton
            :label="t('downloadAllEvtps')"
            :action="evtpService.downloadUrl()"
            :style="'secondary'"
            icon="mdi:download"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { getLink } from '~/common/common-functions'
import evtpService from '~~/services/besluit'
import type { EvtpQuery, Evtp } from '~~/types/besluit'
import { summaryTiles } from '@/config/config'

import type { UrlQuery } from '~/types/filter'
import type { Content } from '@/components/besluit/BesluitCard.vue'

const { t } = useI18n()
const router = useRouter()
const isMobile = useMobileBreakpoint().medium

const query = computed(() => {
  const pageLength = 6
  const urlQuery = useRoute().query as UrlQuery
  return {
    ...urlQuery,
    page: +(urlQuery.page || 1),
    limit: +(urlQuery.limit || pageLength)
  } as EvtpQuery
})

let { data } = await evtpService.getEvtpFiltered(query.value)

// Refresh data based on the URL query
const loading = ref<boolean>(false)

watch(query, async () => {
  loading.value = true
  const response = await evtpService.getEvtpFiltered(query.value)
  loading.value = false
  data = response.data
  newFocusIsRequested.value = true
})

const page = computed(() => query.value.page)
const totalCount = computed(() => data.value?.total_count || 0)
const evtps = computed(() => data.value?.result_evtp || [])
const nPages = computed(() => Math.ceil(totalCount.value / query.value.limit))
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
  scrollToCards()
}

const extractContent = (evtp: Evtp) => {
  // turn the evtp into a list of content
  const content = summaryTiles.map((sT) => ({
    title: t(`evtpProperties.${sT}.label`),
    description: (evtp[sT as keyof Evtp] ||
      evtp.entity_oe_best.naam_spraakgbr ||
      t('ontbreekt')) as string
  }))
  return content as Content[]
}

const searchPageTitle = computed(() =>
  query.value.searchtext
    ? t(`besluiten.foundResults`, { n: totalCount.value }).concat(
        t(`forSearch`, { searchQuery: query.value.searchtext })
      )
    : t(`evtpIndex.pageTitle`)
)

useHead({ title: searchPageTitle })
providePageTitle({
  title: 'evtpIndex.pageTitle',
  labelType: 'locale-index'
})

onMounted(() => {
  const route = useRoute()
  const scrollTo = route.query.scrollTo
  if (scrollTo === 'searchbar') {
    setTimeout(() => {
      scrollToCards()
    }, 150) // Adjust delay as needed
    setTimeout(() => {
      newFocusIsRequested.value = true
    }, 150) // Adjust delay as needed
  }
})
</script>

<style scoped lang="scss">
.h2-size {
  font-size: 48.375px;

  @media (max-width: 51em) {
    font-size: 32px;
  }
}

ul.no-results {
  list-style-image: url(@/assets/images/icons/icon-dart-right-blue.svg);
  line-height: 2 !important;
  padding-left: 3em;
  margin-bottom: 20em;
}

li {
  padding-left: 1em;
}
</style>
