<template>
  <div>
    <div class="container row">
      <NuxtLink class="link cta__backwards" :to="{ name: 'gegevens' }">
        {{ p('gegevens.goBack') }}
      </NuxtLink>
    </div>
    <div class="container row container--centered">
      <div class="md-padding">
        <div class="next-to-each-other">
          <h1 class="no-margin">{{ ggDetail.omschrijving }}</h1>
        </div>
        <p>
          <ParseUrl>
            {{ ggDetail.omschrijving_uitgebreid }}
          </ParseUrl>
        </p>

        <div class="formoverheid-padding">
          <FormOverheidButton
            class="button--align-to-search-field"
            :label="textCollapseAllAccordions"
            :style="'secondary'"
            :aria-expanded="!hideUnhideAccordion"
            @click="() => hideUnhideAccordionAllAccordions(hideUnhideAccordion)"
          />
        </div>
      </div>

      <div class="accordion">
        <div
          ref="accordionHeader1"
          class="accordion-header"
          role="button"
          tabindex="0"
          :aria-expanded="isAccordionActive(GgHeader.h1)"
          @click="() => openCloseAccordion(GgHeader.h1, accordionHeader1)"
          @keydown.enter="
            () => openCloseAccordion(GgHeader.h1, accordionHeader1)
          "
          @keydown.space.prevent="
            () => openCloseAccordion(GgHeader.h1, accordionHeader1)
          "
        >
          <h3 class="h3-sentence accordion-header-with-chevron">
            {{ p('gegevens.h1') }}
          </h3>
          <NuxtIcon :name="getIconAccordion(GgHeader.h1)" />
        </div>
        <div
          v-show="isAccordionActive(GgHeader.h1)"
          :id="GgHeader.h1"
          class="accordion-body"
        >
          <p>{{ p('gegevens.p1') }}</p>
          <AccordionModalEvtp :evtp="ggEvtp" :title="p('gegevens.p1')">
          </AccordionModalEvtp>
        </div>
      </div>

      <div class="accordion">
        <div
          ref="accordionHeader2"
          class="accordion-header"
          role="button"
          tabindex="0"
          :aria-expanded="isAccordionActive(GgHeader.h2)"
          @click="() => openCloseAccordion(GgHeader.h2, accordionHeader2)"
          @keydown.enter="
            () => openCloseAccordion(GgHeader.h2, accordionHeader2)
          "
          @keydown.space.prevent="
            () => openCloseAccordion(GgHeader.h2, accordionHeader2)
          "
        >
          <h3 class="h3-sentence accordion-header-with-chevron">
            {{ p('gegevens.h2') }}
          </h3>
          <NuxtIcon :name="getIconAccordion(GgHeader.h2)" />
        </div>
        <div
          v-show="isAccordionActive(GgHeader.h2)"
          :id="GgHeader.h2"
          class="accordion-body"
        >
          <div>
            <p>{{ p('gegevens.p2') }}</p>
            <AccordionModalOe :oe="oeBron" :title="p('gegevens.h1')">
            </AccordionModalOe>
          </div>
        </div>
      </div>

      <div class="accordion">
        <div
          ref="accordionHeader3"
          class="accordion-header"
          role="button"
          tabindex="0"
          :aria-expanded="isAccordionActive(GgHeader.h3)"
          @click="() => openCloseAccordion(GgHeader.h3, accordionHeader3)"
          @keydown.enter="
            () => openCloseAccordion(GgHeader.h3, accordionHeader3)
          "
          @keydown.space.prevent="
            () => openCloseAccordion(GgHeader.h3, accordionHeader3)
          "
        >
          <h3 class="h3-sentence accordion-header-with-chevron">
            {{ p('gegevens.h3') }}
          </h3>
          <NuxtIcon :name="getIconAccordion(GgHeader.h3)" />
        </div>
        <div
          v-show="isAccordionActive(GgHeader.h3)"
          :id="GgHeader.h3"
          class="accordion-body"
        >
          <p>{{ p('gegevens.p3') }}</p>
          <AccordionModalOe :oe="oeShared" :title="p('gegevens.h3')">
          </AccordionModalOe>
        </div>
      </div>
      <div class="formoverheid-padding">
        <FormOverheidButton
          class="button--align-to-search-field"
          :label="textCollapseAllAccordions"
          :style="'secondary'"
          :aria-expanded="!hideUnhideAccordion"
          @click="() => hideUnhideAccordionAllAccordions(hideUnhideAccordion)"
        />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import evtpService from '@/services/gegevens'
import type { Gg } from '@/types/gegevens'
import type { Oe, Evtp } from '@/types/besluit'

import {
  ggNm,
  isAccordionActive,
  openCloseAccordion,
  hideUnhideAccordionAllAccordions,
  getIconAccordion,
  resetAccordion,
  activeItem,
} from '@/utils/index'

const { p } = usePreditor()

resetAccordion()
const GgHeader = {
  h1: 'h1',
  h2: 'h2',
  h3: 'h3',
}

const route = useRoute()
const ggUpc = route.params.gg_upc as string

const response = await evtpService.getOneGg(ggUpc)
const data = response.data
const ggDetail = ref<Gg>(data.value.gg as Gg)
const oeShared = ref<Oe[]>(data.value.oe_best as Oe[])
const ggEvtp = ref<Evtp[]>(data.value.evtp as Evtp[])
const oeBron = ref<Oe[]>(data.value.oe_bron as Oe[])

const accordionHeader1 = ref<HTMLElement | null>(null)
const accordionHeader2 = ref<HTMLElement | null>(null)
const accordionHeader3 = ref<HTMLElement | null>(null)
// const ggIbron = ref<Ibron[]>(data.value.ibron as Ibron[])

const active = false as boolean
const iconAccordion = 'fa-chevron-down' as string

Object.keys(GgHeader).forEach((header, index) =>
  activeItem.value.push({ header, active, iconAccordion, index })
)

if (!ggDetail.value) {
  throw createError({
    statusCode: 404,
  })
}
ggNm.value.name = ggDetail.value.omschrijving
ggNm.value.upc = ggDetail.value.gg_upc.toString()
</script>
<style scoped lang="scss">
.word-break {
  word-break: break-word;
}

.img-question-mark {
  height: 1em;
  margin: 0em 0em -0.2em 0em;
  background-size: 1em !important;
  background-position: center 50%;
  background-repeat: no-repeat;
  padding-right: 1em;
  padding-left: 1em;
  cursor: pointer;
}

.question-highlight {
  color: white;
  padding: 0.1em;
  font-size: 0.8em;
  border-radius: 0.1em;
  background-color: $primary;
}

.timeline {
  position: relative;
  margin-left: 1em;
  counter-reset: section;
}

.timeline-dots::after {
  counter-increment: section;
  content: counter(section);
  font-size: 1.3em;
  text-align: center;
  color: $white;
  position: absolute;
  width: 1.3em;
  height: 1.3em;
  left: -2.35em;
  top: -0.5em;
  background-color: $primary-dark;
  border-radius: 50%;
  z-index: 9;
}

.collapse-all {
  text-decoration: underline;
  font-weight: bold;
  font-size: 1.35em;
  cursor: pointer;
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

.timeline::after {
  content: '';
  position: absolute;
  width: 0.3em;
  background-color: $primary-dark;
  top: 0;
  bottom: 0;
  left: -1.7em;
}

.timeline-dots {
  position: relative;
}

@media (max-width: 65em) {
  .timeline::after {
    content: '';
    position: absolute;
    width: 0.3em;
    background-color: $primary-dark;
    top: 0;
    bottom: 0;
    left: -1em;
  }

  .timeline-dots::after {
    counter-increment: section;
    content: counter(section);
    font-size: 1.1em;
    text-align: center;
    color: $white;
    position: absolute;
    width: 1.3em;
    left: -2em;
    top: -0.5em;
    background-color: $primary-dark;
    border-radius: 50%;
    z-index: 1;
  }
}

.formoverheid-padding {
  padding: 0px 0px 1.35em;
}
</style>
