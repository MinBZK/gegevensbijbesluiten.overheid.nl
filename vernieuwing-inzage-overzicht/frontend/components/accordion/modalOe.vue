<template>
  <div class="white-card-list">
    <ul>
      <li
        v-for="item in oeListSorted.slice(0, maxListItemsInModal)"
        :key="item.oe_cd"
        class="white-card-list"
      >
        <NuxtLink
          :to="getLink(`/organisatie/${item.oe_upc}`).value"
          :aria-label="`Lees meer over ${item.naam_spraakgbr}`"
          class="linked-content"
        >
          <span class="underline">{{ capitaliseFirstLetter(item.naam_spraakgbr) }}</span>
        </NuxtLink>
      </li>
    </ul>
    <div
      v-if="oe.length > maxListItemsInModal"
      class="show-more capitalise-first underline"
      aria-haspopup="dialog"
      aria-expanded="false"
    >
      <img src="assets/images/icons/icon-hamburger.svg" alt="" height="12" />
      <a
        class="linked-content"
        href="#"
        role="button"
        @click.prevent="showModal()"
        @keydown.enter.prevent="showModal()"
        @keydown.space.prevent="showModal()"
      >
        {{ t('oeIndex.showMore') }}
      </a>
    </div>
  </div>
  <div>
    <ModalShell
      v-model="isModalVisible"
      width="500px"
      :height="isMobile ? '100%' : '80%'"
      :subject-title="props.title"
      modal-title="Organisaties"
      @click.stop
    >
      <h1 class="h1--small no-margin">{{ p('gegevens.h2Modal') }}</h1>
      <p>
        <ModalSearchBar
          :search-explanation="p('searchbar.OeSearchText')"
          @do-search="handleSearch"
        />
      </p>
      <p>
        <b>{{ p('searchbar.OeSelect') }}</b>
      </p>
      <div v-if="oeList.length == 0">
        <p v-if="searchPerformed">{{ p('searchbar.OeNoResults') }}</p>
      </div>
      <div aria-live="polite" aria-atomic="true" class="sr-only">
        <p v-if="oeList.length == 0 && searchPerformed">
          {{ p('searchbar.OeNoResults') }}
        </p>
      </div>
      <ul>
        <li v-for="item in oeListSorted" :key="item.oe_cd" class="card-sub-content">
          <NuxtLink :to="getLink(`/organisatie/${item.oe_upc}`).value" class="linked-content">
            <span class="underline">{{ capitaliseFirstLetter(item.naam_spraakgbr) }}</span>
          </NuxtLink>
        </li>
      </ul>
    </ModalShell>
  </div>
</template>

<script setup lang="ts">
import type { Oe } from '@/types/besluit'
import { getLink, capitaliseFirstLetter } from '~/common/common-functions'
import { getMaxListItems } from '@/config/config'

const isMobile = useMobileBreakpoint().medium
const { t } = useI18n()
const { p } = usePreditor()

const props = defineProps<{
  oe: Oe[]
  title: string
}>()

const oeList = ref(props.oe || [])
const oeListSorted = computed(() =>
  oeList.value.sort((a, b) => a.naam_spraakgbr.localeCompare(b.naam_spraakgbr))
)

const searchPerformed = ref<boolean>(false)
const handleSearch = (searchValue: string) => {
  searchPerformed.value = true
  oeList.value = (props.oe || []).filter((oeList) =>
    oeList.naam_spraakgbr.toLowerCase().includes(searchValue.toLowerCase().trim())
  )
}

const isModalVisible = ref<boolean>(false)
const lastFocus = ref<Element | null>(null)

const showModal = () => {
  lastFocus.value = document.activeElement
  isModalVisible.value = true
}

const oeListSortedSlice = ref(oeListSorted.value)
const { maxListItemsInModal } = getMaxListItems()
onMounted(() => {
  maxListItemsInModal.value = 3
  oeListSortedSlice.value = oeListSorted.value.slice(0, maxListItemsInModal.value)
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
