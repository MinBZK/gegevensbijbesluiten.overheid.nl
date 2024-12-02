<template>
  <div>
    <div class="card-header">
      <img class="card-icon" :alt="ond.titel" :src="`${getIcon(ond.titel)}`" />
      <h1 id="ond-title">{{ ond.titel }}</h1>
    </div>
    <p v-if="isMobile">{{ ond.omschrijving }}</p>
    <p>
      <ModalSearchBar
        :search-explanation="t('pages.onderwerpen.searchText')"
        @do-search="handleSearch"
      />
    </p>
    <p>
      <b> {{ t('besluitLinkList') }}</b>
    </p>
    <template v-if="evtps.length !== 0">
      <ul>
        <li v-for="(evtp, index) in evtps" :key="index">
          <NuxtLink
            :to="getLink(`/besluit/${evtp.evtp_upc}`, evtp.versie_nr).value"
            :aria-label="`Lees meer over ${evtp.evtp_nm}`"
            >{{ evtp.evtp_nm }}
            <span v-if="channelIfConcept"> {{ `${t(`versionNumber`)} ${evtp.versie_nr}` }}</span>
          </NuxtLink>
        </li>
      </ul>
    </template>
    <template v-else>
      <p v-if="searchPerformed">{{ t('besluiten.noResults') }}</p>
      <p v-else>{{ t('besluiten.empty') }}</p>
    </template>
  </div>
</template>

<script setup lang="ts">
import evtpService from '~~/services/besluit'
import { getIcon } from '~~/services/onderwerp'
import type { Ond } from '~~/types/besluit'
import { getLink, channelIfConcept } from '~/common/common-functions'

const props = defineProps<{
  ond: Ond
}>()

const { t } = useI18n()
const emit = defineEmits(['update:modal'])

const { data } = await evtpService.getEvtpByOnd(props.ond.ond_cd)
const evtps = ref(data.value || [])
const searchPerformed = ref<boolean>(false)

const closeModal = () => {
  emit('update:modal', false)
}

const handleSearch = (searchValue: string) => {
  searchPerformed.value = true
  evtps.value = (data.value || []).filter((evtp) =>
    evtp.evtp_nm.toLowerCase().includes(searchValue.toLowerCase().trim())
  )
}

const isMobile = useMobileBreakpoint().medium

onMounted(() => {
  const escListener = (event: any) => {
    if (event.key === 'Escape') {
      closeModal()
    }
  }
  window.addEventListener('keydown', escListener)
  onBeforeUnmount(() => {
    window.removeEventListener('keydown', escListener)
  })

  const handleResize = () => {
    isMobile.value = window.innerWidth <= 800
  }

  window.addEventListener('resize', handleResize)
  handleResize()
})
</script>

<style scoped lang="scss">
li {
  padding-bottom: 1em;
}

ul {
  padding-left: 0;
}

.card-header {
  display: inline-flex;
  align-items: center;

  h1 {
    margin-bottom: 0;
  }

  .card-icon {
    width: 3em;
    height: 3em;
    background-size: cover;
    background-position: right center;
    margin-left: auto;
    margin-right: 1em;
  }
}
</style>
