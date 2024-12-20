<template>
  <div class="white-card-list">
    <ul>
      <li v-for="item in evtpListSortedSlice" :key="item.evtp_nm" class="white-card-list">
        <NuxtLink
          :to="getLink(`/besluit/${item.evtp_upc}`, item.versie_nr).value"
          :aria-label="`${item.evtp_nm}`"
          class="linked-content"
        >
          <span class="underline"> {{ item.evtp_nm }} </span>
        </NuxtLink>
      </li>
    </ul>
    <div v-if="evtp.length > maxListItemsInModal" class="show-more capitalise-first underline">
      <img src="assets/images/icons/icon-hamburger.svg" alt="" height="12" />
      <a
        class="linked-content"
        href="#"
        role="button"
        aria-haspopup="dialog"
        @click.prevent="showModal()"
        @keydown.enter.prevent="showModal()"
        @keydown.space.prevent="showModal()"
      >
        {{ t('evtpIndex.showMore') }}
      </a>
    </div>
  </div>
  <div>
    <ModalShell
      v-model="isModalVisible"
      width="500px"
      :height="isMobile ? '100%' : '80%'"
      :subject-title="props.title"
      aria-labelledby="gegevens-h1-modal"
    >
      <h1 id="gegevens-h1-modal" class="h1--small no-margin">
        {{ t('pages.besluiten.relatedEvtp') }}
      </h1>
      <p>
        <ModalSearchBar
          :search-explanation="t('pages.besluiten.searchSingleText')"
          @do-search="handleSearch"
        />
      </p>
      <p>
        <b>{{ t('besluiten.foundEvtp') }}</b>
      </p>
      <div v-if="evtpList.length == 0">
        <p v-if="searchPerformed">{{ t('besluiten.noResults') }}</p>
      </div>
      <div aria-live="polite" aria-atomic="true" class="sr-only">
        <p v-if="evtpList.length == 0 && searchPerformed">
          {{ t('besluiten.noResults') }}
        </p>
      </div>
      <ul>
        <li v-for="item in evtpListSorted" :key="item.evtp_nm" class="card-sub-content">
          <NuxtLink
            :to="getLink(`/besluit/${item.evtp_upc}`, item.versie_nr).value"
            class="linked-content"
          >
            <span class="underline"> {{ item.evtp_nm }} </span>
          </NuxtLink>
        </li>
      </ul>
    </ModalShell>
  </div>
</template>

<script setup lang="ts">
import type { Evtp } from '@/types/besluit'
import { getLink } from '~/common/common-functions'
import { getMaxListItems } from '@/config/config'

const isMobile = useMobileBreakpoint().medium
const { t } = useI18n()

const props = defineProps<{
  evtp: Evtp[]
  title: string
}>()

const evtpList = ref(props.evtp || [])
const evtpListSorted = computed(() => {
  return evtpList.value.sort((a, b) => a.evtp_nm.localeCompare(b.evtp_nm))
})

const searchPerformed = ref<boolean>(false)
const handleSearch = (searchValue: string) => {
  searchPerformed.value = true
  evtpList.value = (props.evtp || []).filter((evtpList) =>
    evtpList.evtp_nm.toLowerCase().includes(searchValue.toLowerCase().trim())
  )
}

const isModalVisible = ref<boolean>(false)
const lastFocus = ref<Element | null>(null)

const showModal = () => {
  lastFocus.value = document.activeElement
  isModalVisible.value = true
}

const evtpListSortedSlice = ref(evtpListSorted.value)
const { maxListItemsInModal } = getMaxListItems()
onMounted(() => {
  maxListItemsInModal.value = 3
  evtpListSortedSlice.value = evtpListSorted.value.slice(0, maxListItemsInModal.value)
})

watch(isModalVisible, (newValue) => {
  if (!newValue) {
    if (lastFocus.value instanceof HTMLElement) {
      lastFocus.value.focus()
    }
  }
})
</script>

<style scoped lang="scss">
ul {
  padding-left: 0;
}

p:first-letter {
  text-transform: capitalize;
}

.lowercase:first-letter {
  text-transform: lowercase;
}

a {
  text-decoration: none;
}
</style>
