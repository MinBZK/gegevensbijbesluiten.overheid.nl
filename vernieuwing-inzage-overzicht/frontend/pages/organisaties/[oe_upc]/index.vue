<template>
  <div>
    <div class="container row">
      <NuxtLink class="link cta__backwards" :to="{ name: 'organisaties' }">
        {{ p('organisaties.goBack') }}
      </NuxtLink>
    </div>
    <div class="container row container--centered">
      <div class="md-padding">
        <div class="next-to-each-other">
          <h1 class="no-margin capitalise-first">
            {{ oeDetail.naam_spraakgbr }}
          </h1>
        </div>
        <p>
          <ParseUrl>
            {{ oeDetail.naam_officieel }}
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
            {{ p('organisaties.h1') }}
          </h3>
          <NuxtIcon :name="getIconAccordion(GgHeader.h1)" />
        </div>
        <div
          v-show="isAccordionActive(GgHeader.h1)"
          :id="GgHeader.h1"
          class="accordion-body"
        >
          <div v-if="evtpManaged.length > 0">
            <p>{{ p('organisaties.p1') }}</p>
            <AccordionModalEvtp
              :evtp="evtpManaged"
              :title="p('organisaties.p1')"
            >
            </AccordionModalEvtp>
          </div>
          <div v-else>
            <p>{{ p('organisaties.p1-empty') }}</p>
            <NuxtLink :to="{ name: 'organisaties' }">
              <span class="underline">
                {{ p('organisaties.goBack') }}
              </span>
            </NuxtLink>
          </div>
          <NuxtLink :to="{ name: 'organisaties' }">
            <span class="underline">
              {{ p('organisaties.goBack') }}
            </span>
          </NuxtLink>
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
import oeService from '@/services/organisaties'
import type { Oe } from '@/types/organisaties'
import type { Evtp } from '@/types/besluit'
// import type { Gg } from '@/types/gegevens'

import {
  oeNm,
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
const oeUpc = route.params.oe_upc as string

const response = await oeService.getOneOe(oeUpc)
const data = response.data
const oeDetail = ref<Oe>(data.value.oe as Oe)
const evtpManaged = ref<Evtp[]>(data.value.evtpManaged as Evtp[])
// const ggManaged = ref<Gg[]>(data.value.ggManaged as Gg[])
// const ggReceive = ref<Gg[]>(data.value.ggReceive as Gg[])

const accordionHeader1 = ref<HTMLElement | null>(null)
// const accordionHeader2 = ref<HTMLElement | null>(null)
// const accordionHeader3 = ref<HTMLElement | null>(null)

const active = false as boolean
const iconAccordion = 'fa-chevron-down' as string

Object.keys(GgHeader).forEach((header, index) =>
  activeItem.value.push({ header, active, iconAccordion, index })
)

if (!oeDetail.value) {
  throw createError({
    statusCode: 404,
  })
}
oeNm.value.name = oeDetail.value.naam_officieel
oeNm.value.upc = oeDetail.value.oe_upc.toString()
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
