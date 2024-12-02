<template>
  <div class="white-card-list">
    <ul>
      <li v-for="item in ggListSortedSlice" :key="item.gg_cd" class="white-card-list">
        <NuxtLink
          :to="getLink(`/gegeven/${item.gg_upc}`).value"
          :aria-label="`Lees meer over ${item.omschrijving}`"
          class="linked-content"
        >
          <span class="underline">
            {{ capitaliseFirstLetter(item.omschrijving) }}
          </span>
        </NuxtLink>
      </li>
    </ul>
    <div v-if="ggList.length > maxListItemsInModal" class="show-more capitalise-first underline">
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
        {{ t('ggIndex.showMore') }}
      </a>
    </div>
  </div>
  <div>
    <ModalShell
      v-model="isModalVisible"
      width="500px"
      :height="isMobile ? '100%' : '80%'"
      aria-labelledby="gegevens-h3-modal"
      @click.stop
    >
      <h1 id="gegevens-h3-modal" class="h1--small no-margin">
        {{ t('pages.organisaties.relatedOe') }}
      </h1>
      <p>
        <ModalSearchBar
          :search-explanation="t('pages.gegevens.searchSingleText')"
          @do-search="handleSearch"
        />
      </p>
      <p>
        <b>{{ t('gegevens.select') }}</b>
      </p>
      <div v-if="ggList.length == 0">
        <p v-if="searchPerformed">{{ t('gegevens.noResults') }}</p>
      </div>
      <div aria-live="polite" aria-atomic="true" class="sr-only">
        <p v-if="ggList.length == 0 && searchPerformed">
          {{ t('gegevens.GgNoResults') }}
        </p>
      </div>
      <ul>
        <li v-for="item in ggListSorted" :key="item.gg_cd" class="card-sub-content">
          <NuxtLink :to="getLink(`/gegeven/${item.gg_upc}`).value" class="linked-content">
            <span class="underline">
              {{ capitaliseFirstLetter(item.omschrijving) }}
            </span>
          </NuxtLink>
        </li>
      </ul>
    </ModalShell>
  </div>
</template>

<script setup lang="ts">
import type { Gg } from '@/types/gegeven'
import { getLink, capitaliseFirstLetter } from '~/common/common-functions'
import { getMaxListItems } from '@/config/config'

const isMobile = useMobileBreakpoint().medium
const { t } = useI18n()

const props = defineProps<{
  gg: Gg[]
  title: string
}>()

const ggList = ref(props.gg || [])
const ggListSorted = computed(() =>
  ggList.value.sort((a, b) => a.omschrijving.localeCompare(b.omschrijving))
)

const searchPerformed = ref<boolean>(false)
const handleSearch = (searchValue: string) => {
  searchPerformed.value = true
  ggList.value = (props.gg || []).filter((ggList) =>
    ggList.omschrijving.toLowerCase().includes(searchValue.toLowerCase().trim())
  )
}

const isModalVisible = ref<boolean>(false)
const lastFocus = ref<Element | null>(null)

const showModal = () => {
  lastFocus.value = document.activeElement
  isModalVisible.value = true
}

const ggListSortedSlice = ref(ggListSorted.value)
const { maxListItemsInModal } = getMaxListItems()
onMounted(() => {
  maxListItemsInModal.value = 3
  ggListSortedSlice.value = ggListSorted.value.slice(0, maxListItemsInModal.value)
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
