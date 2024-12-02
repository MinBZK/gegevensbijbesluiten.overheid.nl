<template>
  <div>
    <div class="container row">
      <NuxtLink class="link cta__backwards" :to="{ name: 'gegeven' }">
        {{ t('pages.gegevens.goBack') }}
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
          @keydown.enter="() => openCloseAccordion(GgHeader.h1, accordionHeader1)"
          @keydown.space.prevent="() => openCloseAccordion(GgHeader.h1, accordionHeader1)"
        >
          <h2 class="h2-sentence accordion-header-with-chevron">
            {{ t('pages.gegevens.h1') }}
          </h2>
          <NuxtIcon :name="getIconAccordion(GgHeader.h1)" />
        </div>
        <div v-show="isAccordionActive(GgHeader.h1)" :id="GgHeader.h1" class="accordion-body">
          <p>{{ t('pages.gegevens.p1') }}</p>
          <AccordionModalEvtp :evtp="ggEvtp" :title="t('pages.gegevens.p1')"> </AccordionModalEvtp>
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
          @keydown.enter="() => openCloseAccordion(GgHeader.h2, accordionHeader2)"
          @keydown.space.prevent="() => openCloseAccordion(GgHeader.h2, accordionHeader2)"
        >
          <h3 class="h3-sentence accordion-header-with-chevron">
            {{ t('pages.gegevens.h2') }}
          </h3>
          <NuxtIcon :name="getIconAccordion(GgHeader.h2)" />
        </div>
        <div v-show="isAccordionActive(GgHeader.h2)" :id="GgHeader.h2" class="accordion-body">
          <div>
            <p>{{ t('pages.gegevens.p2') }}</p>
            <AccordionModalOe :oe="oeBron" :title="t('pages.gegevens.h1')"> </AccordionModalOe>
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
          @keydown.enter="() => openCloseAccordion(GgHeader.h3, accordionHeader3)"
          @keydown.space.prevent="() => openCloseAccordion(GgHeader.h3, accordionHeader3)"
        >
          <h3 class="h3-sentence accordion-header-with-chevron">
            {{ t('pages.gegevens.h3') }}
          </h3>
          <NuxtIcon :name="getIconAccordion(GgHeader.h3)" />
        </div>
        <div v-show="isAccordionActive(GgHeader.h3)" :id="GgHeader.h3" class="accordion-body">
          <p>{{ t('pages.gegevens.p3') }}</p>
          <AccordionModalOe :oe="oeShared" :title="t('pages.gegevens.h3')"> </AccordionModalOe>
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
import evtpService from '@/services/gegeven'
import type { Gg } from '@/types/gegeven'
import type { Oe, Evtp } from '@/types/besluit'

import {
  ggNm,
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

const active = false as boolean
const iconAccordion = 'fa-chevron-down' as string

useHead({
  title: `${ggDetail.value.omschrijving}`
})

Object.keys(GgHeader).forEach((header, index) =>
  activeItem.value.push({ header, active, iconAccordion, index })
)

hideUnhideAccordionAllAccordions(true)

if (!ggDetail.value) {
  throw createError({
    statusCode: 404
  })
}
ggNm.value.name = ggDetail.value.omschrijving
ggNm.value.upc = ggDetail.value.gg_upc.toString()

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

.formoverheid-padding {
  padding: 0px 0px 1.35em;
}
</style>
