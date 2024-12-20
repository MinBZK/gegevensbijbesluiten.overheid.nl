<template>
  <div>
    <div class="card-header">
      <h1 id="organisaties-card-title" class="h1--small no-margin modal-title-padding">
        {{ props.title }}
      </h1>
    </div>
    <p>
      <ModalSearchBar
        :search-explanation="t('pages.organisaties.searchText')"
        @do-search="handleSearch"
      />
    </p>
    <p>
      <b>{{ t('organisaties.select') }}</b>
    </p>
    <template v-if="contentList.length !== 0">
      <div>
        <ul>
          <li v-for="(item, index) in contentList" :key="index" class="card-sub-content">
            <NuxtLink :to="item.link" :aria-label="`${item.description}`">
              {{ capitaliseFirstLetter(item.description) }}
            </NuxtLink>
          </li>
        </ul>
      </div>
    </template>
    <template v-else>
      <p v-if="searchPerformed">{{ t('organisaties.noResults') }}</p>
    </template>
  </div>
</template>

<script setup lang="ts">
import type { OeContent } from '@/components/organisatie/OrganisatieCard.vue'
import { capitaliseFirstLetter } from '@/common/common-functions'

const { t } = useI18n()

const props = defineProps<{
  content: OeContent[]
  title: string
  description: string
}>()
const emit = defineEmits(['update:overlay'])

const data = props.content
const contentList = ref(data || [])

const closeOverlayCard = () => {
  emit('update:overlay', false)
}

const searchPerformed = ref<boolean>(false)
const handleSearch = (searchValue: string) => {
  searchPerformed.value = true
  contentList.value = (props.content || []).filter((contentList) =>
    contentList.description.toLowerCase().includes(searchValue.toLowerCase().trim())
  )
}

const isMobile = useMobileBreakpoint().medium

onMounted(() => {
  const escListener = (event: any) => {
    if (event.key === 'Escape') {
      closeOverlayCard()
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
ul {
  padding-left: 0;
}

.card-header {
  display: inline-flex;
  align-items: center;

  h1 {
    margin-bottom: 1em;
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
