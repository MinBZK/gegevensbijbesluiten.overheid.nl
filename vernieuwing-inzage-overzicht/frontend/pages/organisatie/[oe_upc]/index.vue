<template>
  <div>
    <div class="container row">
      <NuxtLink id="content" class="link cta__backwards" :to="{ name: 'organisatie' }">
        {{ t('pages.organisaties.goBack') }}
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
          @keydown.enter="() => openCloseAccordion(GgHeader.h1, accordionHeader1)"
          @keydown.space.prevent="() => openCloseAccordion(GgHeader.h1, accordionHeader1)"
        >
          <h2 class="h2-sentence accordion-header-with-chevron">
            {{ t('pages.organisaties.h1') }}
          </h2>
          <NuxtIcon :name="getIconAccordion(GgHeader.h1)" />
        </div>
        <div v-show="isAccordionActive(GgHeader.h1)" :id="GgHeader.h1" class="accordion-body">
          <div v-if="evtpManaged.length > 0">
            <p>{{ t('pages.organisaties.p1') }}</p>
            <AccordionModalEvtp :evtp="evtpManaged" :title="t('pages.organisaties.p1')">
            </AccordionModalEvtp>
          </div>
          <div v-else>
            <p>{{ t('pages.organisaties.p1-empty') }}</p>
            <NuxtLink :to="{ name: 'organisatie' }">
              <span class="underline">
                {{ t('pages.organisaties.goBack') }}
              </span>
            </NuxtLink>
          </div>
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
import oeService from '@/services/organisatie'
import type { Oe } from '@/types/organisatie'
import type { Evtp } from '@/types/besluit'

import {
  oeNm,
  isAccordionActive,
  openCloseAccordion,
  hideUnhideAccordionAllAccordions,
  getIconAccordion,
  resetAccordion,
  activeItem
} from '@/utils/index'

const { t } = useI18n()

resetAccordion()
const GgHeader = {
  h1: 'h1',
  h2: 'h2',
  h3: 'h3'
}

const route = useRoute()
const oeUpc = route.params.oe_upc as string

const response = await oeService.getOneOe(oeUpc)
const data = response.data
const oeDetail = ref<Oe>(data.value.oe as Oe)
const evtpManaged = ref<Evtp[]>(data.value.evtpManaged as Evtp[])

const accordionHeader1 = ref<HTMLElement | null>(null)

const active = false as boolean
const iconAccordion = 'fa-chevron-down' as string

useHead({
  title: `${oeDetail.value.naam_spraakgbr}`
})

Object.keys(GgHeader).forEach((header, index) =>
  activeItem.value.push({ header, active, iconAccordion, index })
)

hideUnhideAccordionAllAccordions(true)

if (!oeDetail.value) {
  throw createError({
    statusCode: 404
  })
}
oeNm.value.name = oeDetail.value.naam_officieel
oeNm.value.upc = oeDetail.value.oe_upc.toString()

onMounted(() => {
  hideUnhideAccordionAllAccordions(false)
})
</script>
<style scoped lang="scss">
.word-break {
  word-break: break-word;
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
