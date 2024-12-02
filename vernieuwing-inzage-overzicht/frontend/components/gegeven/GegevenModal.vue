<template>
  <div>
    <div class="card-header">
      <h1 id="gegevens-card-title" class="h1--small no-margin modal-title-padding">
        {{ props.title }}
      </h1>
    </div>
    <p>
      <ModalSearchBar
        :search-explanation="t('pages.gegevens.searchText')"
        @do-search="handleSearch"
      />
    </p>
    <p>
      <b>{{ t('gegevens.select') }}</b>
    </p>
    <template v-if="contentList.length !== 0">
      <div>
        <ul class="white-box-list">
          <li v-for="(item, index) in contentList" :key="index" class="card-sub-content">
            <NuxtLink :to="item.link" :aria-label="`Lees meer over ${item.description}`"
              >{{ item.description }}
            </NuxtLink>
          </li>
        </ul>
      </div>
    </template>
    <template v-else>
      <p v-if="searchPerformed">{{ t('gegevens.noResults') }}</p>
    </template>
  </div>
</template>

<script setup lang="ts">
import type { GgContent } from '@/components/gegeven/GegevenCard.vue'
const { t } = useI18n()

const props = defineProps<{
  content: GgContent[]
  title: string
  description: string
}>()

const emit = defineEmits(['update:modal'])

const data = props.content
const contentList = ref(data || [])

const closeOverlayCard = () => {
  emit('update:modal', false)
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
