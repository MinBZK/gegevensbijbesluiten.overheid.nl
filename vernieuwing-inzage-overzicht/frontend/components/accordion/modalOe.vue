<template>
  <div>
    <ul class="white-card-list">
      <li
        v-for="item in oeListSorted.slice(0, 3)"
        :key="item.oe_cd"
        class="white-card-list"
      >
        <NuxtLink
          :to="getLink(`/organisaties/${item.oe_upc}`).value"
          class="linked-content"
        >
          <span class="underline">{{
            capitaliseFirstLetter(item.naam_spraakgbr)
          }}</span>
        </NuxtLink>
      </li>

      <div v-if="oe.length > 3" class="show-more capitalise-first underline">
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
      <ul>
        <li
          v-for="item in oeListSorted"
          :key="item.oe_cd"
          class="card-sub-content"
        >
          <NuxtLink
            :to="getLink(`/organisaties/${item.oe_upc}`).value"
            class="linked-content"
          >
            <span class="underline">{{
              capitaliseFirstLetter(item.naam_spraakgbr)
            }}</span>
          </NuxtLink>
        </li>
      </ul>
    </ModalShell>
  </div>
</template>

<script setup lang="ts">
import type { Oe } from '@/types/besluit'
import { getLink, capitaliseFirstLetter } from '~/common/common-functions'

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
const isModalVisible = ref<boolean>(false)

const searchPerformed = ref<boolean>(false)
const handleSearch = (searchValue: string) => {
  searchPerformed.value = true
  oeList.value = (props.oe || []).filter((oeList) =>
    oeList.naam_spraakgbr.toLowerCase().includes(searchValue.toLowerCase())
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
