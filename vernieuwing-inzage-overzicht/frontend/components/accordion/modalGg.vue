<template>
  <div>
    <ul class="white-card-list">
      <li
        v-for="item in ggList.slice(0, 3)"
        :key="item.gg_cd"
        class="white-card-list"
      >
        <NuxtLink
          :to="getLink(`/gegevens/${item.gg_upc}`, 0).value"
          class="linked-content"
        >
          <span class="underline"> {{ item.omschrijving }} </span>
        </NuxtLink>
      </li>
      <div
        v-if="ggList.length > 3"
        class="show-more capitalise-first underline"
      >
        <img src="assets/images/icons/icon-hamburger.svg" alt="" height="12" />
        <a
          class="linked-content"
          href="#"
          @click.prevent="showModal()"
          @keydown.enter="showModal()"
          @keydown.space.prevent="showModal()"
        >
          {{ t('showMore') }}
        </a>
      </div>
    </ul>
    <ModalShell
      v-model="isModalVisible"
      width="500px"
      :height="isMobile ? '100%' : '80%'"
      :subject-title="props.title"
      @click.stop
    >
      <h1 class="h1--small no-margin">{{ p('gegevens.h3Modal') }}</h1>
      <p>
        <ModalSearchBar
          :search-explanation="p('searchbar.GgSearchText')"
          @do-search="handleSearch"
        />
      </p>
      <p>
        <b>{{ p('searchbar.GgSelect') }}</b>
      </p>
      <div v-if="ggList.length == 0">
        <p v-if="searchPerformed">{{ p('searchbar.GgNoResults') }}</p>
      </div>
      <ul>
        <li
          v-for="item in ggListSorted"
          :key="item.gg_cd"
          class="card-sub-content capitalise-first"
        >
          <NuxtLink
            :to="getLink(`/gegevens/${item.gg_upc}`, 0).value"
            class="linked-content"
          >
            <span class="underline"> {{ item.omschrijving }} </span>
          </NuxtLink>
        </li>
      </ul>
    </ModalShell>
  </div>
</template>

<script setup lang="ts">
import type { Gg } from '@/types/gegevens'
import { getLink } from '~/common/common-functions'

const isMobile = useMobileBreakpoint().medium
const { t } = useI18n()
const { p } = usePreditor()

const props = defineProps<{
  gg: Gg[]
  title: string
}>()

const ggList = ref(props.gg || [])
const ggListSorted = computed(() =>
  ggList.value.sort((a, b) => a.omschrijving.localeCompare(b.omschrijving))
)
const isModalVisible = ref<boolean>(false)

const searchPerformed = ref<boolean>(false)
const handleSearch = (searchValue: string) => {
  searchPerformed.value = true
  ggList.value = (props.gg || []).filter((ggList) =>
    ggList.omschrijving.toLowerCase().includes(searchValue.toLowerCase())
  )
}
const showModal = () => {
  isModalVisible.value = true
}
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
