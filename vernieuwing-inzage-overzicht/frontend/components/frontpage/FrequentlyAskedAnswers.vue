<template>
  <div class="answers">
    <h3 v-if="isMobile" id="faqQuestionTitle">
      {{ props.question?.question && t(props.question.question) }}
    </h3>
    <div>
      <p>{{ answer1 }}</p>
      <p v-if="answer2">{{ answer2 }}</p>
      <p v-if="answer3">
        {{ answer3 }}
        <ExternalLink v-if="link3" :href="link3.url" :is-mobile="isMobile">
          {{ link3.text }}
        </ExternalLink>
      </p>
      <ul v-if="link4 && link5" class="bullet ml-4">
        <li>
          <ExternalLink :href="link4.url" :is-mobile="isMobile">
            <span aria-hidden="true">
              {{ link4.text }}
            </span>
            <span class="sr-only">
              {{ t('faq.7.link_4_5_information') }}
              {{ link4.text.toLowerCase() }}
            </span>
          </ExternalLink>
        </li>
        <li>
          <ExternalLink :href="link5.url" :is-mobile="isMobile">
            <span aria-hidden="true">
              {{ link5.text }}
            </span>
            <span class="sr-only">
              {{ t('faq.7.link_4_5_information') }}
              {{ link5.text.toLowerCase() }}
            </span>
          </ExternalLink>
        </li>
      </ul>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { Question } from '~/config/faq'

const props = defineProps<{
  question: Question | null
}>()

const { t } = useI18n()
const isMobile = useMobileBreakpoint().large

// Computed properties
const answer1 = computed(() => props.question?.answer_1 && t(props.question.answer_1))
const answer2 = computed(() => props.question?.answer_2 && t(props.question.answer_2))
const answer3 = computed(() => props.question?.answer_3 && t(props.question.answer_3))
const link3 = computed(() => {
  if (props.question?.link_3_url && props.question?.link_3_text) {
    return {
      url: t(props.question.link_3_url),
      text: t(props.question.link_3_text)
    }
  }
  return null
})
const link4 = computed(() => {
  if (props.question?.link_4_url && props.question?.link_4_text) {
    return {
      url: t(props.question.link_4_url),
      text: t(props.question.link_4_text)
    }
  }
  return null
})
const link5 = computed(() => {
  if (props.question?.link_5_url && props.question?.link_5_text) {
    return {
      url: t(props.question.link_5_url),
      text: t(props.question.link_5_text)
    }
  }
  return null
})
</script>

<style scoped lang="scss">
.answers {
  height: 100%;
  flex-direction: column;
  padding: 1em;

  h3 {
    font-size: 1.1em;
    margin-bottom: 0.85em;
  }
}
.no-margin {
  padding-left: 0px;
}
.sr-only {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  border: 0;
}
</style>
