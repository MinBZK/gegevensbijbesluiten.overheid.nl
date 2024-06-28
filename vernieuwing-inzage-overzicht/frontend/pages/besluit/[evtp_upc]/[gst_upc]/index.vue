<template>
  <div>
    <div class="container row">
      <NuxtLink class="link cta__backwards" :to="getLink(`/besluit/${gst.besluit.evtp_upc}`, evtpVersionNr).value">
        {{ t('goBackEvtp', { evtp_name: gst.besluit.evtp_nm }) }}
      </NuxtLink>
    </div>
    <div class="container row container--centered">
      <div class="formoverheid-padding">
        <FormOverheidButton
class="button--align-to-search-field" :label="textCollapseAllAccordions"
          :style="'secondary'" :aria-expanded="!hideUnhideAccordion"
          @click="() => hideUnhideAccordionAllAccordions(hideUnhideAccordion)" />
      </div>
      <div class="timeline">
        <div id="1" class="accordion">
          <div
ref="gstAccordionHeader1" class="accordion-header" tabindex="0" role="button"
            :aria-expanded="isAccordionActive(EvtpGstHeader.bron_organisatie)"
            @click="() => openCloseAccordion(EvtpGstHeader.bron_organisatie, gstAccordionHeader1)"
            @keydown.enter="() => openCloseAccordion(EvtpGstHeader.bron_organisatie, gstAccordionHeader1)"
            @keydown.space.prevent="() => openCloseAccordion(EvtpGstHeader.bron_organisatie, gstAccordionHeader1)">
            <span class="timeline-dots van">
            </span>
            <h3 class="psentence capitalise-first accordion-header-with-chevron">
              {{ gst.bron_organisatie.header_oe_bron_naamofficieel }}
            </h3>
            <NuxtIcon :name="getIconAccordion(EvtpGstHeader.bron_organisatie)" />
          </div>
          <div
v-show="isAccordionActive(EvtpGstHeader.bron_organisatie)" :id="EvtpGstHeader.bron_organisatie"
            class="accordion-body">
            <span v-if="gst.bron_organisatie.ibron_oe_naam_officieel">
              <p>{{ t('gegevensstromen.dataStorage', { article: gst.bron_organisatie.ibron_oe_lidwsgebr }) }}
                <b>{{ `${gst.bron_organisatie.ibron_oe_naam_officieel}` }}</b>
                <span>.</span>
                {{ t('gegevensstromen.registrationSourceOrganisation', { article: gst.bron_organisatie.oe_bron_lidwsgebr, source_organisation: gst.bron_organisatie.header_oe_bron_naamofficieel }) }}
              </p>
            </span>
            <p>
              {{ t('gegevensstromen.dataExchangeBySourceOrganisation', { article: gst.bron_organisatie.oe_bron_lidwsgebr, source_organisation: gst.bron_organisatie.oe_bron_naampraakgebr }) }}
            </p>
            <p v-for="gstType in gst.bron_organisatie.gsttype_gsttoms" :key="gstType" class="white-card">
              {{ `${gstType}` }}
            </p>
            <h4
              v-if="gst.bron_organisatie.ibron_oe_econtact || gst.bron_organisatie.gst_extlnkaut || gst.bron_organisatie.oe_bron_internetdomein">
              {{ t('gegevensstromen.wantToKnowMore') }}
            </h4>
            <p>
              <ExternalLink v-if="gst.bron_organisatie.ibron_oe_econtact" :href=gst.bron_organisatie.ibron_oe_econtact>
                {{ t('gegevensstromen.checkYourDataInRegister', { article: gst.bron_organisatie.ibron_oe_lidwsgebr, register: gst.bron_organisatie.ibron_oe_naam_spraakgbr }) }}
              </ExternalLink>
            </p>
            <p>
              <ExternalLink v-if="gst.bron_organisatie.gst_extlnkaut" :href=gst.bron_organisatie.gst_extlnkaut>
                {{ t('gegevensstromen.checkAutorisation') }}
              </ExternalLink>
            </p>
            <p>
              <ExternalLink
v-if="gst.bron_organisatie.oe_bron_internetdomein"
                :href=gst.bron_organisatie.oe_bron_internetdomein>
                {{ t('gegevensstromen.contactSourceOrganisation', { article: gst.bron_organisatie.oe_bron_lidwsgebr, source_organisation: gst.bron_organisatie.oe_bron_naampraakgebr }) }}
              </ExternalLink>
            </p>
          </div>
        </div>
        <div id="2" class="accordion">
          <div
ref="gstAccordionHeader2" class="accordion-header" tabindex="0" role="button"
            :aria-expanded="isAccordionActive(EvtpGstHeader.gegevensgroep_grondslag)"
            @click="() => openCloseAccordion(EvtpGstHeader.gegevensgroep_grondslag, gstAccordionHeader2)"
            @keydown.enter="() => openCloseAccordion(EvtpGstHeader.gegevensgroep_grondslag, gstAccordionHeader2)"
            @keydown.space.prevent="() => openCloseAccordion(EvtpGstHeader.gegevensgroep_grondslag, gstAccordionHeader2)">
            <span class="timeline-dots naar">
            </span>
            <h3 class="psentence capitalise-first accordion-header-with-chevron">
              {{ gst.gegevensgroep_grondslag.header_oe_best_naamofficieel }}
            </h3>
            <NuxtIcon :name="getIconAccordion(EvtpGstHeader.gegevensgroep_grondslag)" />
          </div>
          <div
v-show="isAccordionActive(EvtpGstHeader.gegevensgroep_grondslag)"
            :id="EvtpGstHeader.gegevensgroep_grondslag" class="accordion-body">
            <p>
              {{ t('gegevensstromen.receivesTheFollowingData', { article: gst.gegevensgroep_grondslag.oe_best_lidwsgebr, destination_organisation: gst.gegevensgroep_grondslag.oe_best_naampraakgebr }) }}
            </p>
            <ul class="white-card-list">
              <li v-for="(gg, index) in gst.gegevensgroep_grondslag.gg_child" :key="gg" class="white-card-list">
                {{ gg }}
                <img
src="@/assets/images/icons/icon-explanation.svg"
                  :alt="t('getGgPropertyExplanation', { field: gg })" class="img-question-mark" tabindex="0"
                  :aria-expanded="isKeyToggled(gg) ? 'true' : 'false'" @click="() => toggleKey(gg)"
                  @keydown.enter="() => toggleKey(gg)" @keydown.space.prevent="() => toggleKey(gg)">
                <div v-if="isKeyToggled(gg)" class="word-break">
                  <i>
                    <ParseUrl :key="gst.gegevensgroep_grondslag.gg_omschrijvinguitgebreid[index]">
                      {{ gst.gegevensgroep_grondslag.gg_omschrijvinguitgebreid[index] }}
                    </ParseUrl>
                  </i>
                </div>
              </li>
            </ul>
            <p>
              {{ t('gegevensstromen.purposeData', { article: gst.gegevensgroep_grondslag.oe_best_lidwsgebr, destination_organisation: gst.gegevensgroep_grondslag.oe_best_naampraakgebr }) }}
            </p>
            <ParseUrl>
              <p v-if="gst.gegevensgroep_grondslag.evtp_gst_conditie" class="white-card">
                {{ `${gst.gegevensgroep_grondslag.evtp_gst_conditie}` }}
              </p>
              <p v-else class="white-card">
                {{ `${gst.gegevensgroep_grondslag.evtp_aanleiding}` }}
              </p>
            </ParseUrl>
            <p>
              {{ t('gegevensstromen.followingInformationForPurposes', { article: gst.gegevensgroep_grondslag.oe_best_lidwsgebr, destination_organisation: gst.gegevensgroep_grondslag.oe_best_naampraakgebr }) }}
            </p>
            <p class="white-card">
            <h4>{{ t('gegevensstromen.goal') }}</h4>
            <p>{{ gst.gegevensgroep_grondslag.evtp_gebrdl }}</p>
            <h4>{{ t('gegevensstromen.legalBasis') }}</h4>
            <ul class="white-card-list no-padding-top">
              <li
v-for="(rge, index) in gst.gegevensgroep_grondslag.rge" :key="index"
                class="white-card-list no-padding-left">
                <ExternalLink :href=rge.re_link>
                  {{ rge.titel }}
                </ExternalLink>
              </li>
            </ul>
            <!-- eslint-disable-next-line prettier/prettier -->
            </p>
          </div>
        </div>
      </div>
      <FormOverheidButton
class="button--align-to-search-field" :label="textCollapseAllAccordions" :style="'secondary'"
        :aria-expanded="!hideUnhideAccordion" @click="() => hideUnhideAccordionAllAccordions(hideUnhideAccordion)" />
    </div>
  </div>
</template>

<script setup lang="ts">

import type { EvtpGst } from '~~/types/besluit'
import { EvtpGstHeader } from '~~/types/besluit'
import evtpService from '@/services/besluit'
import { ggNm, evtpNm, isAccordionActive, openCloseAccordion, hideUnhideAccordionAllAccordions, getIconAccordion, resetAccordion } from '@/utils/index'
import { getLink, channelIfConcept } from '~/common/common-functions'

const { t } = useI18n()

// (un)accordion
resetAccordion()

// get data
const route = useRoute()
const evtpUpc = route.params.evtp_upc as string
const gstUpc = route.params.gst_upc as string
const evtpVersionNr = parseInt(route.query.versionNr as string)
const gstAccordionHeader1 = ref<HTMLElement | null>(null)
const gstAccordionHeader2 = ref<HTMLElement | null>(null)

let data
if (channelIfConcept.value) {
  const response = await evtpService.getOneEvtpGstVersion(evtpUpc, evtpVersionNr, gstUpc)
  data = response.data
} else {
  const response = await evtpService.getOneEvtpGst(evtpUpc, gstUpc)
  data = response.data
}

const gst = ref<EvtpGst>(data.value as EvtpGst)
const active = false as boolean
const iconAccordion = "fa-chevron-down" as string

Object.keys(gst.value).forEach((header, index) => activeItem.value.push({ header, active, iconAccordion, index }))
if (!gst.value) {
  throw createError({
    statusCode: 404,
  })
}

// store gg and evtp name as ref elements
ggNm.value.name = gst.value.gegevensgroep_grondslag.gg_parent
ggNm.value.upc = gstUpc

evtpNm.value.name = gst.value.besluit.evtp_nm
evtpNm.value.upc = evtpUpc
evtpNm.value.versionNr = evtpVersionNr


// expand gegevensgroep extra info
const keyToggles = ref<string[]>([])
const toggleKey = (key: string) => {
  if (keyToggles.value.includes(key)) {
    keyToggles.value = keyToggles.value.filter((e: any) => e !== key)
  } else {
    keyToggles.value.push(key)
  }
}
const isKeyToggled = (key: string) => {
  if (keyToggles.value.includes(key)) {
    return true
  }
  else {
    return false
  }
}

useHead({ title: `${ggNm.value.name} van het besluit ${evtpNm.value.name}` })

onBeforeUnmount(() => {
  resetAccordion()
})
</script>
<style scoped lang="scss">
.no-padding-top {
  padding-top: 0;
}

.no-padding-left {
  padding-left: 0;

}
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
}

.timeline-dots::after {
  content: '';
  font-size: 1.4em;
  text-align: center;
  color: $white;
  position: absolute;
  width: 2.8em;
  height: 1.5em;
  left: -4.35em;
  top: -0.65em;
  background-color: $primary-dark;
  border-radius: 1em;
  z-index: 1;
}

.timeline-dots.van::after {
  content: 'Van:';
}

.timeline-dots.naar::after {
  content: 'Naar:';
}

.timeline::after {
  content: '';
  position: absolute;
  width: 0.3em;
  background-color: $primary-dark;
  top: 0;
  bottom: 0;
  left: -2.9em;
}

.accordion-all {
  text-decoration: underline;
  font-weight: bold;
  font-size: 1.35em;
  cursor: pointer;
}

p:first-letter {
  text-transform: capitalize;
}

a {
  text-decoration: none;
}

.timeline-dots {
  position: relative;
}

@media (max-width: 65em) {
  .timeline {
    position: relative;
    margin-left: 2.5em;
  }

  .timeline::after {
    content: '';
    position: absolute;
    width: 0.3em;
    background-color: $primary-dark;
    top: 0;
    bottom: 0;
    left: -2.1em;
  }

  .timeline-dots::after {
    content: '';
    font-size: 1em;
    text-align: center;
    color: $white;
    position: absolute;
    width: 2.8em;
    left: -4.7em;
    top: -0.65em;
    background-color: $primary-dark;
    border-radius: 1em;
    z-index: 1;
  }
}

.formoverheid-padding {
  padding: 0px 0px 1.35em;
}
</style>