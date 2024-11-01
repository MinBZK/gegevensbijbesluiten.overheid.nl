<template>
  <h2>{{ t('onderwerpen.title') }}</h2>
  <ul class="ond-card-container ul-padding">
    <li
      v-for="(ond, index) in onds"
      :key="ond.ond_cd"
      class="ond-card"
      :role="isMobile ? 'button' : ''"
      :tabindex="isMobile ? 0 : ''"
      @click.prevent="showModal(ond, index)"
      @keydown.enter.prevent="showModal(ond, index)"
      @keydown.space.prevent="showModal(ond, index)"
    >
      <div>
        <div class="card-header">
          <img class="card-icon" :alt="ond.titel" :src="`${getIcon(ond.titel)}`" />
          <h3 :id="'onderwerpenTitle-' + index">{{ ond.titel }}</h3>
        </div>
        <p class="mobile-description">{{ ond.omschrijving }}</p>
      </div>
      <div class="card-link">
        <img
          src="assets/images/icons/icon-chevron-right-primary-darker.svg"
          class="mobile-description"
          alt=""
        />
        <a
          ref="anchorListItems"
          role="button"
          class="mobile-description"
          href="#"
          aria-haspopup="dialog"
          @click.prevent="showModal(ond, index)"
          @keydown.enter.prevent="showModal(ond, index)"
          @keydown.space.prevent="showModal(ond, index)"
        >
          {{
            t('pages.onderwerpen.referenceToEvtp', {
              evtpName: ond.titel
            })
          }}</a
        >
      </div>
    </li>
    <ModalShell
      v-model="isModalVisible"
      width="500px"
      height="80%"
      :index-modal-title="Number(lastAnchorItem)"
      modal-title="Besluiten"
      aria-labelledby="selectedOnd"
      aria-describedby="selectedOnd"
    >
      <BesluitModal v-if="!!selectedOnd" :ond="selectedOnd" />
    </ModalShell>
  </ul>
</template>

<script setup lang="ts">
import ondService, { getIcon } from '~~/services/onderwerp'
import type { Ond } from '~~/types/besluit'
import { useMobileBreakpoint } from '~~/composables/mobile'

const { t } = useI18n()
const isModalVisible = ref<boolean>(false)
const selectedOnd = ref<Ond>()
const isMobile = useMobileBreakpoint().small

const props = defineProps({
  numberOfTiles: {
    type: Number,
    default: 11
  },
  showIcons: {
    type: Boolean,
    default: true
  }
})

const { data } = await ondService.getPopulatedOnd({
  limit: props.numberOfTiles
})
const onds = ref<Ond[]>(data.value || [])
const anchorListItems = ref<HTMLElement[]>([])
const lastAnchorItem = ref<Number>(0)

const showModal = (ond: Ond, index: number) => {
  selectedOnd.value = ond
  isModalVisible.value = true
  lastAnchorItem.value = index
}

watch(isModalVisible, (newValue) => {
  if (!newValue) {
    anchorListItems.value[lastAnchorItem.value as number].focus()
  }
})
</script>

<style scoped lang="scss">
.ond-card-container {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  row-gap: 0.9em;
  column-gap: 0.9em;

  .ond-card {
    border-radius: 4px;
    padding: 0.7em 1.5em 1em 1.5em;
    background-color: $tertiary;
    transition: box-shadow 0.3s ease-out;

    &:hover {
      box-shadow: 0 0 10px rgb(147, 180, 205);
    }

    cursor: pointer;

    // Spacing for link
    display: flex;
    flex-direction: column;
    justify-content: space-between;

    .card-header {
      display: inline-flex;
      align-items: center;

      h3 {
        margin-bottom: 0;
        font-size: 1em;
      }

      .card-icon {
        background-repeat: no-repeat;
        width: 2.75em;
        height: 2.75em;
        background-size: 2.5em;
        background-position: center;
        margin-right: 0.5em;
      }
    }
  }
}

@media (max-width: 50em) {
  .ond-card-container {
    grid-template-columns: repeat(2, 1fr);
    width: 100%;
  }

  .mobile-description {
    display: none;
  }
}

@media (max-width: 50em) {
  .ond-card {
    padding: 1em;

    .card-header {
      display: flex;
      flex-direction: column;
      align-items: center;
      text-align: center;
      justify-content: center;
      width: 100%;

      .card-icon {
        margin: 0em 0em 1em 0em !important;
        width: 52em !important;
        height: 5em !important;
        background-size: 5em !important;
      }
    }
  }
}

.card-link {
  display: inline-flex;
  align-items: center;
  column-gap: 0.25em;

  a {
    font-weight: 600;
    text-decoration: none !important;
  }
}
</style>
