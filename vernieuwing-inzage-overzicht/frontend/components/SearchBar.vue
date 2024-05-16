<template>
  <div class="block-search">
    <div class="columns">
      <div class="column column-d-5">
        <div class="form__row less-bottom-margin">
          <label id="search-label" class="form__label form__label--accent">{{
            searchExplanation
          }}</label>

          <div class="wrapper-searchbar">
            <!-- <select v-model="searchSubject" class="dropdown">
              <option
                v-for="option in options"
                :key="option.value"
                :value="option.value"
                class="dropdown-item"
              >
                {{ option.label }}
              </option>
            </select> -->

            <input
              id="input-text-98789"
              v-model="searchValue"
              type="text"
              name="98789"
              class="input input-text"
              :placeholder="searchHint"
              aria-invalid="false"
              aria-labelledby="search-label"
              @keyup.enter="() => doSearch()"
            />
          </div>
        </div>
      </div>
      <div class="column column-d-0.5">
        <div class="form__row">
          <FormOverheidButton
            class="button--align-to-search-field"
            :label="search"
            icon="ic:round-search"
            :full-width="true"
            @click="() => doSearch()"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
const { t } = useI18n()

const emit = defineEmits<{
  (e: 'doSearch', searchValue: string): void
}>()

// const options = [
//   { value: 'besluiten', label: 'Besluiten' },
//   { value: 'onderwerpen', label: 'Onderwerpen' },
//   { value: 'besluiten', label: 'Besluiten' },
//   { value: 'gegevens', label: 'Gegevens' },
//   { value: 'organisaties', label: 'Organisaties' },
// ]
const props = defineProps<{
  searchExplanation: string
}>()

const searchValue = ref(useRoute().query.searchtext || '')

const search = computed(() => t('search'))
const searchHint = computed(() => t('searchHint'))

const searchExplanation = props.searchExplanation

const doSearch = () => {
  const router = useRouter()
  router.push({
    name: 'besluit',
    query: {
      searchtext: searchValue.value,
      scrollTo: 'searchbar',
    },
  })
  emit('doSearch', searchValue.value as string)
}
</script>

<style scoped lang="scss">
.wrapper-searchbar {
  display: flex;
}
.dropdown {
  background-color: $primary;
  color: white;
  border-radius: 0.25em;
  border-top-right-radius: 0px;
  border-bottom-right-radius: 0px;
  width: 200px;
}

.dropdown-item {
  background-color: $secondary;
  color: black;
}

.input-text {
  border-top-left-radius: 0px;
  border-bottom-left-radius: 0px;
}
.button--align-to-search-field {
  margin-top: 1.75em;
}
@media (max-width: 65em) {
  .button--align-to-search-field {
    margin-top: 0.6em;
  }
}
.form__label {
  margin-bottom: 0.5em !important;
}
.less-bottom-margin {
  margin-bottom: 0px !important;
}

.block-search {
  scroll-margin-top: 1em;
}
</style>
