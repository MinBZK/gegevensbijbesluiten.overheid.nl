<template>
  <div>
    <ul class="white-card-list">
      <li
        v-for="item in evtp.slice(0, 3)"
        :key="item.evtp_nm"
        class="white-card-list"
      >
        <NuxtLink
          :to="getLink(`/besluit/${item.evtp_upc}`, item.versie_nr).value"
          class="linked-content"
        >
          {{ item.aanleiding }}:
          <span class="underline"> {{ item.evtp_nm }} </span>
        </NuxtLink>
      </li>
      <div v-if="evtp.length > 3" class="show-more capitalise-first underline">
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
      <h1 class="h1--small no-margin">{{ p('gegevens.h1Modal') }}</h1>
      <p>
        <ModalSearchBar
          :search-explanation="p('searchbar.EvtpSearchText')"
          @do-search="handleSearch"
        />
      </p>
      <p>
        <b>{{ p('searchbar.EvtpSelect') }}</b>
      </p>
      <div v-if="evtpList.length == 0">
        <p v-if="searchPerformed">{{ p('searchbar.EvtpNoResults') }}</p>
      </div>
      <ul>
        <li
          v-for="item in evtpListSorted"
          :key="item.evtp_nm"
          class="card-sub-content"
        >
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

const isMobile = useMobileBreakpoint().medium
const { t } = useI18n()
const { p } = usePreditor()

const props = defineProps<{
  evtp: Evtp[]
  title: string
}>()

const evtpList = ref(props.evtp || [])
const evtpListSorted = computed(() => {
  return evtpList.value.sort((a, b) => a.evtp_nm.localeCompare(b.evtp_nm))
})
const isModalVisible = ref<boolean>(false)

const searchPerformed = ref<boolean>(false)
const handleSearch = (searchValue: string) => {
  searchPerformed.value = true
  evtpList.value = (props.evtp || []).filter((evtpList) =>
    evtpList.omschrijving.toLowerCase().includes(searchValue.toLowerCase())
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
