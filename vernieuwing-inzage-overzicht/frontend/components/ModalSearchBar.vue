<template>
  <div>
    <label id="search-label" class="form__label form__label--accent">{{ searchExplanation }}</label>
    <div class="input-wrapper">
      <input
        id="input-text-98789"
        ref="searchInput"
        v-model="searchValue"
        type="text"
        name="98789"
        class="input input-text"
        :placeholder="searchHint"
        aria-invalid="false"
        aria-labelledby="search-label"
        @input="() => $emit('doSearch', searchValue)"
        @keyup.enter="() => $emit('doSearch', searchValue)"
      />
      <span class="icon">
        <NuxtIcon name="mdi:magnify" />
      </span>
    </div>
  </div>
</template>

<script setup lang="ts">
defineProps({
  searchExplanation: {
    type: String,
    default: ''
  }
})

const { t } = useI18n()

const emit = defineEmits<{
  (e: 'input', searchValue: string): void
  (e: 'doSearch', searchValue: string): void
}>()

const searchValue = ref<string>('')
const searchHint = computed(() => t('search'))
const searchInput = ref<HTMLElement | null>(null)

onMounted(() => {
  searchInput.value?.focus()
  // clear any search on remounting
  emit('doSearch', '')
})
</script>

<style scoped lang="css">
.input-wrapper {
  position: relative;
}

.input-wrapper .icon {
  position: absolute;
  left: 5px; /* Adjust as needed */
  top: 50%;
  transform: translateY(-50%);
}

.input-wrapper .input {
  padding-left: 30px; /* Adjust as needed */
}
.wrapper-2 {
  display: flex;
}
.wrapper-1 {
  margin-bottom: 10px;
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
</style>
