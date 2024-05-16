<template>
  <div ref="htmlLink" class="card-item card-hover" @click="showModal()">
    <div></div>
    <!-- add at least one child to focus on in case the search resulted in nothing -->
    <div v-if="!props.loading" class="item-header">
      <div class="result--title focus-border">
        <h3>{{ props.title }}</h3>
      </div>
    </div>
    <p v-if="!props.loading">
      {{ props.description }}
    </p>

    <div v-if="!props.loading" class="white-box">
      <div
        v-for="item in props.content.slice(0, 3)"
        :key="item.link"
        class="card-sub-content"
        @click.stop
      >
        <NuxtLink :to="item.link" class="linked-content">
          {{ item.description }}
        </NuxtLink>
      </div>
      <div class="card-sub-content">
        <img
          src="assets/images/icons/icon-hamburger.svg"
          aria-hidden
          class="mobile-description"
          alt=""
        />
        <a
          class="linked-content"
          href="#"
          @click.prevent="showModal()"
          @keydown.enter.prevent="showModal()"
          @keydown.space.prevent="showModal()"
        >
          {{ t('ggIndex.showMore') }}
        </a>
      </div>
    </div>
    <div v-if="!props.loading" class="card-footer">
      <div class="text-align-left">
        <ChipsOnderwerp :chips="props.chips"></ChipsOnderwerp>
      </div>
    </div>
    <ModalShell
      v-model="isModalVisible"
      width="500px"
      :height="isMobile ? '100%' : '80%'"
      :subject-title="props.title"
      @click.stop
    >
      <GegevensModal
        v-if="!!props.content"
        :content="props.content"
        :description="props.description"
        :title="props.title"
      />
    </ModalShell>
  </div>
</template>

<script setup lang="ts">
import GegevensModal from './GegevensModal.vue'

// const { t } = useI18n()
const isMobile = useMobileBreakpoint().medium

export interface GgContent {
  link: any
  description: string
}

interface Props {
  title: string
  description: string
  content: GgContent[]
  chips: string[]
  setFocus?: boolean
  loading: boolean
}

const props = withDefaults(defineProps<Props>(), {
  title: '',
  description: '',
  content: undefined,
  chips: undefined,
  setFocus: false,
  loading: false,
})

const emit = defineEmits<{
  (e: 'focusHasBeenSet'): void
}>()

const { t } = useI18n()

onMounted(() => {
  focusCardLink()
})

const htmlLink = ref<HTMLAnchorElement>()
const isModalVisible = ref<boolean>(false)

const showModal = () => {
  isModalVisible.value = true
}

const focusCardLink = () => {
  if (htmlLink.value && htmlLink.value.firstChild && props.setFocus) {
    ;(htmlLink.value.firstChild as HTMLElement)?.focus()
    emit('focusHasBeenSet')
  }
}

const setFocusWatcher = computed(() => props.setFocus)
watch(setFocusWatcher, (newValue) => {
  if (newValue) {
    focusCardLink()
  }
})
</script>

<style scoped lang="scss">
.card-item {
  min-height: 25em;
}

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
