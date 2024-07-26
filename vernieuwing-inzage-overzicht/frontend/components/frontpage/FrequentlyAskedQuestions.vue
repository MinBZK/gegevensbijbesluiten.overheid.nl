<template>
  <ul class="no-padding faq-box">
    <li
      v-for="(question, index) in questions"
      :key="index"
      class="faq-component"
    >
      <div class="questions faq-card">
        <button
          ref="questionsItems"
          :key="index"
          :class="{ question: true, desktop: !isMobile }"
          :data-selected="question.question === selectedQuestion?.question"
          :aria-expanded="isAccordionActive(question.question)"
          @click="
            () => [
              selectQuestion(index),
              openCloseAccordionMutuallyExclusive(question.question),
            ]
          "
        >
          <p class="column left">{{ t(question.question) }}</p>
          <NuxtIcon
            :name="
              isMobile
                ? 'fa-chevron-right'
                : getIconAccordion(question.question)
            "
            class="column right chevron"
          />
        </button>
        <template v-if="!isMobile">
          <div v-if="isAccordionActive(question.question)">
            <FrequentlyAskedAnswers :question="questions[index]" />
          </div>
        </template>
      </div>
    </li>
  </ul>
  <template v-if="isMobile">
    <ModalShell
      v-model="isModalVisible"
      :width="isSmallScreen ? '100%' : '800px'"
      max-height="90%"
      height="350px"
      modal-title="faqQuestionTitle"
    >
      <FrequentlyAskedAnswers :question="selectedQuestion" />
    </ModalShell>
  </template>
</template>

<script setup lang="ts">
import { questions } from '~/config/faq'
import type { Question } from '~/config/faq'
import FrequentlyAskedAnswers from '~/components/frontpage/FrequentlyAskedAnswers.vue'
import {
  isAccordionActive,
  openCloseAccordionMutuallyExclusive,
  activeItem,
  resetAccordion,
  getIconAccordion,
} from '@/utils/index'

const { t } = useI18n()
const isModalVisible = ref<boolean>(false)
const selectedQuestion = ref<Question | null>(null)
const isMobile = useMobileBreakpoint().large
const isSmallScreen = useMobileBreakpoint().medium
const questionIndex = ref<number>(0)
const questionsItems = ref<HTMLElement[]>([])

const selectQuestion = (e: number) => {
  selectedQuestion.value = questions[e]
  questionIndex.value = e
  if (isMobile) {
    isModalVisible.value = true
  }
}

// (un)collapse accordion
resetAccordion()
activeItem.value = []

const active = false as boolean
const iconAccordion = 'fa-chevron-down' as string

Object.keys(questions).forEach((index: any) =>
  activeItem.value.push({
    header: questions[index].question,
    active,
    iconAccordion,
    index,
  })
)

watch(isModalVisible, (newValue) => {
  if (!newValue) {
    questionsItems.value[questionIndex.value as number].focus()
  }
})
</script>

<style scoped lang="scss">
.left {
  width: 95%;
}

.right {
  width: 5%;
}

.faq-component {
  column-gap: 0.85em;
  display: flex;
  justify-content: center;
  padding: 0 0em;
}

.faq-box {
  border-radius: 4px;
  box-shadow: 0 0 6px rgb(128, 157, 179);
}
.faq-card {
  display: flex;
  width: 50%;
  background-color: white;
  border-radius: 4px;
  box-shadow: 0 0 3px rgb(128, 157, 179);
}

.answers-desktop {
  display: none;
}

.chevron {
  padding: 0.1em;
  width: 1rem;
  height: 1rem;
  object-fit: contain;
}

.questions {
  display: grid;
  width: 25em;

  :first-child {
    border-top-left-radius: 4px;
    border-top-right-radius: 4px;
  }

  :last-child {
    border-bottom-left-radius: 4px;
    border-bottom-right-radius: 4px;
  }

  @media (max-width: 30em) {
    width: 100%;
  }
}

.question {
  // undo default button styling
  background-color: white;
  border: none;

  // Text, general positioning
  width: 100%;
  text-align: start;
  padding: 1.65em 1.2em;

  p {
    font-size: 1.4em;
    margin: 0;
    color: $primary-darker;
    font-weight: 700;
  }

  // Chevron positioning
  display: inline-flex;
  justify-content: space-between;
  align-items: center;

  cursor: pointer;

  &:hover {
    background-color: $tertiary;
  }

  &:focus {
    background-color: $tertiary;
    // fixes invisible border issues
    z-index: 1;
  }

  &[data-selected='true'].desktop {
    background-color: $secondary;
  }
}
</style>
