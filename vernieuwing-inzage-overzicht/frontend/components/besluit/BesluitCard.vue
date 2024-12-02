<template>
  <div class="card-item">
    <div v-if="props.loading" class="skeleton-content">
      <div class="skeleton-header"></div>
      <div class="skeleton-description"></div>
      <div class="skeleton-content-items">
        <div v-for="i in 3" :key="i" class="skeleton-content-item">
          <div class="skeleton-content-title"></div>
          <div class="skeleton-white-box"></div>
        </div>
      </div>
    </div>

    <template v-else>
      <div ref="htmlLink" class="item-header">
        <NuxtLink :to="props.link" class="result--title focus-border">
          <h3 class="h3-margin-tile">{{ props.title }}</h3>
        </NuxtLink>
      </div>
      <p>
        <ParseUrl>
          {{ props.description }}
        </ParseUrl>
      </p>
      <div class="dl columns--data">
        <div v-for="item in props.content" :key="item.title" class="column--fullwidth">
          <h4 class="no-margin">{{ item.title }}</h4>
          <p class="white-card">
            <ParseUrl>
              {{ capitaliseFirstLetter(item.description) }}
            </ParseUrl>
          </p>
        </div>
      </div>
      <b v-if="$colorMode.value == 'concept'" class="versionNumber">
        {{ `${t(`versionNumber`)} ${props.version}` }}
      </b>
      <div class="card-footer">
        <div class="text-align-left chips-container">
          <ChipsOnderwerp :chips="props.chips"></ChipsOnderwerp>
        </div>

        <b class="text-align-right">
          <NuxtLink :to="props.link" :aria-label="`Lees meer over ${props.title}`"
            >{{ t('pages.besluiten.readMore') }}
          </NuxtLink>
        </b>
      </div>
    </template>
  </div>
</template>

<script setup lang="ts">
import { capitaliseFirstLetter } from '~/common/common-functions'
export interface Content {
  title: string
  description: string
}

interface Props {
  title: string
  description: string
  content: Content[]
  link: any
  version?: number
  chips: string[]
  setFocus: boolean
  loading: boolean
}

const props = withDefaults(defineProps<Props>(), {
  title: '',
  description: '',
  content: undefined,
  link: undefined,
  version: 0,
  chips: undefined,
  setFocus: true,
  loading: false
})

const { t } = useI18n()
const htmlLink = ref<HTMLAnchorElement>()

const focusCardLink = () => {
  if (props.setFocus) {
    setTimeout(() => {
      ;(htmlLink.value?.firstChild as HTMLElement)?.focus()
    }, 300) // Adjust delay as needed
  }
}

watch([() => props.loading, () => props.setFocus], ([newLoadingValue, newSetFocusValue]) => {
  if (!newLoadingValue && newSetFocusValue) {
    focusCardLink()
  }
})
</script>

<style scoped lang="scss">
.versionNumber {
  margin-bottom: 10px;
}
h2 {
  font-size: 1.1em;
  margin-bottom: 0;
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
}

.card-footer {
  height: 100%;
  display: flex;
  justify-content: space-between;
}
.text-align-right {
  text-align: right;
  margin-top: auto;
  min-width: 82px;
}
.text-align-left {
  text-align: left;
  margin-top: auto;
  min-width: 82px;
}
.h3-margin-tile {
  margin-bottom: 0.3em;
}
</style>
