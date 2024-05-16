<template>
  <div>
    <div class="container row">
      <NuxtLink class="link cta__backwards" :to="{ name: 'besluit' }">
        {{ t('goBack') }}
      </NuxtLink>
    </div>
    <div class="container row container--centered">
      <div class="md-padding">
        <div class="next-to-each-other">
          <h1 class="no-margin">{{ evtpGg.besluit.evtp_nm }}</h1>
          <span class="next-to-h1">
            <ChipsOnderwerp
              :chips="evtpGg.besluit.ond"
              class="title"
            ></ChipsOnderwerp>
          </span>
        </div>
        <p>
          <ParseUrl>
            {{ evtpGg.besluit.omschrijving }}
          </ParseUrl>
        </p>
        <div class="accordion">
          <div
            ref="gstAccordionHeaderEvtpCom"
            class="accordion-header"
            tabindex="0"
            role="button"
            :aria-expanded="
              isAccordionActive(evtpGg.besluit_communicatie.evtp_oebest)
            "
            @click="
              () =>
                openCloseAccordion(
                  evtpGg.besluit_communicatie.evtp_oebest,
                  gstAccordionHeaderEvtpCom
                )
            "
            @keydown.enter="
              () =>
                openCloseAccordion(
                  evtpGg.besluit_communicatie.evtp_oebest,
                  gstAccordionHeaderEvtpCom
                )
            "
            @keydown.space.prevent="
              () =>
                openCloseAccordion(
                  evtpGg.besluit_communicatie.evtp_oebest,
                  gstAccordionHeaderEvtpCom
                )
            "
          >
            <h3 class="psentence accordion-header-with-chevron">
              {{ t('gegevensgroepen.evtpCommunication') }}
            </h3>
            <NuxtIcon
              :name="getIconAccordion(evtpGg.besluit_communicatie.evtp_oebest)"
            />
          </div>
          <div
            v-show="isAccordionActive(evtpGg.besluit_communicatie.evtp_oebest)"
            :id="evtpGg.besluit_communicatie.evtp_oebest"
            class="accordion-body"
          >
            <p>{{ t('gegevensgroepen.youReceiveMessage') }}</p>
            <span v-if="evtpGg.besluit_communicatie.evtp_oe_com_type">
              <ul class="white-card-list">
                <li
                  v-for="(evtp_oe_com_type, index) in evtpGg
                    .besluit_communicatie.evtp_oe_com_type"
                  :key="index"
                >
                  {{ evtp_oe_com_type.omschrijving }}
                  <ParseUrl :key="evtpGg.besluit_communicatie.oe_best_econtact">
                    {{ evtp_oe_com_type.link }}
                  </ParseUrl>
                </li>
              </ul>
            </span>
            <span v-else-if="evtpGg.besluit_communicatie.oe_best_econtact">
              <p
                v-if="
                  evtpGg.besluit_communicatie.oe_best_econtact.startsWith(
                    'https'
                  )
                "
                class="white-card lowercase"
              >
                <ParseUrl :key="evtpGg.besluit_communicatie.oe_best_econtact">
                  {{ evtpGg.besluit_communicatie.oe_best_econtact }}
                </ParseUrl>
              </p>
              <p v-else>
                <ParseUrl :key="evtpGg.besluit_communicatie.oe_best_econtact">
                  {{ evtpGg.besluit_communicatie.oe_best_econtact }}
                </ParseUrl>
              </p>
            </span>
            <span v-else>
              <p class="white-card">
                <NuxtIcon
                  class="info-square"
                  name="mdi:information-box-outline"
                  alt=""
                />
                {{ t('gegevensstromen.multipleTypeMessages') }}
              </p>
            </span>
            <span v-if="evtpGg.besluit_communicatie.oe_best_internetdomein">
              <h4>{{ t('gegevensstromen.wantToKnowMore') }}</h4>
              <p>
                <ExternalLink
                  :href="evtpGg.besluit_communicatie.oe_best_internetdomein"
                >
                  {{
                    t('gegevensstromen.pleaseContact', {
                      destination_organisation:
                        evtpGg.besluit_communicatie.evtp_oebest,
                    })
                  }}
                </ExternalLink>
              </p>
            </span>
          </div>
        </div>
        <h2 class="no-margin">
          {{
            t('gegevensgroepen.dataWithEvtp', {
              evtp_name: evtpGg.besluit.evtp_nm,
            })
          }}
        </h2>
        <p>
          {{
            t('gegevensgroepen.dataWithEvtpDescription', {
              article: evtpGg.besluit.oe_lidw_sgebr || '',
              destination_organisation: evtpGg.besluit.oe_naam_officieel,
              decision_type: `${evtpGg.besluit.lidw_soort_besluit || ''} ${
                evtpGg.besluit.soort_besluit || ''
              }`,
            })
          }}
          {{ convertedString }}
          {{ t('gegevensgroepen.thisData') }}
        </p>
      </div>
      <div class="formoverheid-padding">
        <FormOverheidButton
          :label="textCollapseAllAccordions"
          :style="'secondary'"
          :aria-expanded="!hideUnhideAccordion"
          @click="() => hideUnhideAccordionAllAccordions(hideUnhideAccordion)"
        />
      </div>
      <div
        v-for="(ggParentObject, ggParent, index) in evtpGg.gegevensgroep"
        :key="index"
        class="accordion"
      >
        <div
          ref="ggAccordionHeader"
          class="accordion-header"
          role="button"
          tabindex="0"
          :aria-expanded="isAccordionActive(ggParent)"
          @click="() => openCloseAccordion(ggParent, ggAccordionHeader[index])"
          @keydown.enter="
            () => openCloseAccordion(ggParent, ggAccordionHeader[index])
          "
          @keydown.space.prevent="
            () => openCloseAccordion(ggParent, ggAccordionHeader[index])
          "
        >
          <h3 class="h3-sentence">{{ ggParent }}</h3>
          <NuxtIcon :name="getIconAccordion(ggParent)" />
        </div>
        <div class="gst-card">
          <div
            v-for="gst in ggParentObject"
            v-show="isAccordionActive(ggParent)"
            :key="gst"
            class="accordion-body-gg"
          >
            <div class="source-card">
              <p class="no-margin">
                {{ t('gegevensgroepen.sourceOrganisation') }}
              </p>
              <p class="strong no-margin">{{ gst['oe_best_naamspraakgbr'] }}</p>
              <div class="source-card-bottom">
                <br />
                <ul class="no-list">
                  <li v-for="ggChild in gst['gg_child']" :key="ggChild">
                    {{ ggChild }}
                  </li>
                </ul>
              </div>
              <FormOverheidButton
                class="button--align-to-search-field"
                label="Meer details"
                :hidden-text="` van ${ggParent} afkomstig van ${gst['oe_best_naamspraakgbr']}`"
                :role-link="'link'"
                icon="material-symbols:chevron-right"
                @click="
                  () =>
                    $router.push(
                      getLink(
                        `/besluit/${evtpGg.besluit.evtp_upc}/${gst.gst_upc}`,
                        evtpVersionNr
                      ).value
                    )
                "
              />
            </div>
          </div>
        </div>
      </div>
      <div class="formoverheid-padding">
        <FormOverheidButton
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
import type { EvtpGg } from '~~/types/besluit'
import evtpService from '@/services/besluit'
import {
  evtpNm,
  isAccordionActive,
  openCloseAccordion,
  hideUnhideAccordionAllAccordions,
  activeItem,
  resetAccordion,
  getIconAccordion,
} from '@/utils/index'
import { getLink, channelIfConcept } from '~/common/common-functions'

const { t } = useI18n()

// (un)collapse accordion
resetAccordion()

// Get data
const route = useRoute()
const evtpUpc = route.params.evtp_upc as string
const evtpVersionNr = parseInt(route.query.versionNr as string)
const ggAccordionHeader = ref<HTMLElement[]>([])
const gstAccordionHeaderEvtpCom = ref<HTMLElement | null>(null)

let data
if (channelIfConcept.value) {
  const response = await evtpService.getOneEvtpGgVersion(evtpUpc, evtpVersionNr)
  data = response.data
} else {
  const response = await evtpService.getOneEvtpGg(evtpUpc)
  data = response.data
}

const evtpGg = ref<EvtpGg>(data.value as EvtpGg)
const active = false as boolean
const iconAccordion = 'fa-chevron-down' as string

Object.keys(evtpGg.value.gegevensgroep).forEach((header, index) =>
  activeItem.value.push({ header, active, iconAccordion, index })
)

activeItem.value.push({
  header: evtpGg.value.besluit_communicatie.evtp_oebest,
  active,
  iconAccordion,
  index: 100,
})

if (!evtpGg.value) {
  throw createError({
    statusCode: 404,
  })
}

const evtpName = evtpGg.value.besluit.evtp_nm
const convertedString = computed(() => {
  const convertWord = (word: string) => {
    if (word.length > 1 && isAllUpperCase(word.slice(0, 2))) {
      return word
    }

    return word.charAt(0) + word.slice(1).toLowerCase()
  }

  const isAllUpperCase = (str: string) => {
    return str === str.toUpperCase()
  }

  return evtpName
    .split(/(?=[A-Z])/)
    .map(convertWord)
    .join('')
})

// store evtp name in ref
evtpNm.value.name = evtpGg.value.besluit.evtp_nm
evtpNm.value.upc = evtpUpc
evtpNm.value.versionNr = evtpVersionNr

useHead({
  title: `${evtpGg.value.besluit.evtp_nm} - ${evtpGg.value.besluit.oe_naam_spraakgbr}`,
})

onMounted(() => {
  const focusableElements = document.querySelectorAll(
    'button:not(.close-button, .show-button), [href], a:not(.items, a:not(.items, .is-external-icon, .external-link), input, select, textarea'
  )
  focusableElements.forEach((el) => el.removeAttribute('tabindex'))
})
</script>
<style scoped lang="scss">
.strong:first-letter {
  text-transform: uppercase;
}

.strong {
  font-weight: bold;
}

.info-square {
  margin-right: 0.45em;
  margin-bottom: 0.12em;
  font-size: 1.05em;
}

.lowercase:first-letter {
  text-transform: lowercase;
}

@media (max-width: 70em) {
  .title {
    margin-top: 8px;
    margin-bottom: 8px;
  }

  .next-to-each-other {
    align-items: center;
  }

  .next-to-h1 {
    border-bottom: 1em;
  }
}

@media (min-width: 70em) {
  .title {
    margin-top: 1px;
  }

  .next-to-each-other {
    align-items: center;
  }

  .next-to-h1 {
    margin-left: 20px;
    margin-top: 10px;
    white-space: nowrap;
    display: inline;
    position: absolute;
  }

  h1 {
    display: inline;
  }
}

a {
  text-decoration: none;
}

p:first-letter {
  text-transform: capitalize;
}

.button--align-to-search-field {
  margin-top: 1.75em;
}

.md-padding {
  padding: 0.8em 0em;
}

ul.no-list {
  margin: 0;
  list-style-type: none;
  padding: 0em;
  hyphens: auto;
  word-break: break-word;
}

@media (max-width: 50em) {
  .source-card {
    background-color: $white;
    margin-left: 1.35em;
    margin-right: 1.35em;
    margin-bottom: 1.35em;
    padding: 1.35em 32px;
    border-radius: 4px;
    height: calc(100% - 16px);
    box-shadow: 0 2px 50em rgba(0, 0, 0, 0.05);
    border-left: 8px solid $primary;
    position: relative;
    width: 80%;

    .source-card-bottom {
      width: 100%;
    }
  }
}

@media (min-width: 50em) {
  .gst-card {
    display: grid;
    grid-template-columns: 50% 50%;
  }

  .gst-card > .accordion-body-gg > .source-card {
    background-color: $white;
    margin-left: 1.35em;
    margin-right: 1.35em;
    margin-bottom: 1.35em;
    padding: 1.35em 32px;
    border-radius: 4px;
    height: calc(100% - 16px);
    box-shadow: 0 0.1em 50em rgba(0, 0, 0, 0.05);
    border-left: 8px solid $primary;
    position: relative;
    display: flex;
    flex-direction: column;

    .source-card-bottom {
      margin-bottom: auto;
    }

    .source-card-icon {
      margin-left: auto;
    }
  }
}

@media (max-width: 65em) {
  .button--align-to-search-field {
    margin-top: 0.6em;
  }
}

.formoverheid-padding {
  padding: 0px 0px 1.35em;
}
</style>
