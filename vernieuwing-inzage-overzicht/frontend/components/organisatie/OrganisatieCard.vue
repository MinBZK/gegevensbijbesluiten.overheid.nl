<template>
  <div class="card-item-override-oe-gg card-hover" @click="showModal()">
    <div v-if="props.loading" class="skeleton-content">
      <div class="skeleton-header"></div>
      <div class="skeleton-description"></div>
      <div class="skeleton-white-box">
        <div v-for="i in 3" :key="i" class="skeleton-list-item"></div>
      </div>
    </div>

    <template v-else>
      <div class="item-header">
        <div class="result--title focus-border">
          <h3>{{ props.title }}</h3>
        </div>
      </div>
      <p>
        {{ props.description }}
      </p>

      <div class="white-box">
        <ul id="link-list" class="no-padding">
          <li
            v-for="item in props.content.slice(0, maxListItemsInModal)"
            :key="item.link"
            class="card-sub-content"
            @click.stop
          >
            <NuxtLink
              :to="item.link"
              class="linked-content"
              :aria-label="`Lees meer over ${item.description}`"
            >
              {{ capitaliseFirstLetter(item.description) }}
            </NuxtLink>
          </li>
        </ul>
        <div
          v-if="props.content.length > maxListItemsInModal"
          class="card-sub-content"
          aria-haspopup="dialog"
          aria-expanded="false"
        >
          <img
            src="assets/images/icons/icon-hamburger.svg"
            aria-hidden
            class="mobile-description"
            alt=""
          />
          <a
            class="linked-content"
            href="#"
            role="button"
            aria-haspopup="dialog"
            @click.prevent="showModal()"
            @keydown.enter.prevent="showModal()"
            @keydown.space.prevent="showModal()"
          >
            {{ t('oeIndex.showMore') }}
          </a>
        </div>
      </div>
      <div class="card-footer">
        <div class="text-align-left">
          <ChipsOnderwerp :chips="props.chips"></ChipsOnderwerp>
        </div>
      </div>
    </template>

    <ModalShell
      v-model="isModalVisible"
      width="500px"
      :height="isMobile ? '100%' : '80%'"
      :subject-title="props.title"
      modal-title="Organisaties"
      @click.stop
    >
      <OrganisatieModal
        v-if="!!props.content"
        :content="props.content"
        :description="props.description"
        :title="props.title"
      />
    </ModalShell>
  </div>
</template>

<script setup lang="ts">
import OrganisatieModal from './OrganisatieModal.vue'
import { capitaliseFirstLetter } from '@/common/common-functions'
import { getMaxListItems } from '@/config/config'

// const { t } = useI18n()
const isMobile = useMobileBreakpoint().medium

export interface OeContent {
  link: any
  description: string
}

interface Props {
  title: string
  description: string
  content: OeContent[]
  chips: string[]
  setFocus: boolean
  loading: boolean
}

const props = withDefaults(defineProps<Props>(), {
  title: '',
  description: '',
  content: undefined,
  chips: undefined,
  setFocus: false,
  loading: false
})

const { t } = useI18n()

const isModalVisible = ref<boolean>(false)
const lastFocus = ref<Element | null>(null)

const focusCardLink = () => {
  nextTick(() => {
    const firstLink = document.querySelector(
      '#link-list > li:first-of-type > a'
    ) as HTMLAnchorElement
    if (firstLink) {
      setTimeout(() => {
        firstLink.focus()
      }, 300) // Adjust delay as needed
    }
  })
}

watch(
  // focus on first item after searching query
  [() => props.loading, () => props.setFocus],
  ([newLoadingValue, newSetFocusValue]) => {
    if (!newLoadingValue && newSetFocusValue) {
      focusCardLink()
    }
  }
)

const showModal = () => {
  lastFocus.value = document.activeElement
  isModalVisible.value = true
}

watch(isModalVisible, (newValue) => {
  if (!newValue) {
    if (lastFocus.value instanceof HTMLElement) {
      lastFocus.value.focus()
    }
  }
})

const { maxListItemsInModal } = getMaxListItems()

onMounted(() => {
  maxListItemsInModal.value = 3
})
</script>

<style scoped lang="scss">
.item-header {
  margin-bottom: 0em;
  margin-top: 1em;
  display: flex;
}

.dl.columns--data div {
  padding: 0.5em 0em 0.5em 0em;
}

.column--fullwidth {
  width: 100% !important;
  margin-bottom: 0.8em;
}

.card-footer {
  height: 100%;
  display: flex;
  justify-content: space-between;
}

img {
  width: 20px;
  height: auto;
  padding-right: 3px;
}
</style>
