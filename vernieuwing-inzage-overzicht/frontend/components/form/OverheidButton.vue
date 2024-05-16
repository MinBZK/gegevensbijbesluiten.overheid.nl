<template>
  <form
    :class="props.alignHorizontally && 'inline-form'"
    :action="action"
    @click="clickButton"
  >
    <button
      :id="buttonId"
      ref="button"
      class="button button--nolabel"
      :class="[
        {
          'button--block': fullWidth,
          disabled: disabled,
        },
        `button--${props.style}`,
      ]"
      type="submit"
      :aria-disabled="disabled ? 'true' : 'false'"
      :aria-label="ariaLabel"
      :aria-expanded="ariaExpanded == undefined ? undefined : ariaExpanded"
      :role="roleLink == undefined ? undefined : roleLink"
    >
      <span v-if="!textCollapseAllAccordions" class="button__label">
        {{ label }} <NuxtIcon v-if="icon" size="0.9em" :name="icon"
      /></span>
      <span v-else class="button__label">
        <span>{{ label }} </span>
        <span class="visually-hidden"> {{ textCollapseAllAccordions }} </span>
        <NuxtIcon v-if="icon" size="0.9em" :name="icon"
      /></span>
    </button>
  </form>
</template>

<script setup lang="ts">
const props = withDefaults(
  defineProps<{
    label: string
    icon?: string | null
    fullWidth?: boolean
    style?: 'primary' | 'secondary' | 'tertiary'
    action?: string | undefined
    alignHorizontally?: boolean
    disabled?: boolean
    buttonId?: string | undefined
    ariaLabel?: string | undefined
    textCollapseAllAccordions?: string | undefined
    ariaExpanded?: boolean | undefined
    roleLink?: string | undefined
  }>(),
  {
    icon: null,
    fullWidth: false,
    primary: true,
    action: undefined,
    alignHorizontally: false,
    disabled: false,
    style: 'primary',
    buttonId: undefined,
    ariaLabel: undefined,
    textCollapseAllAccordions: undefined,
    ariaExpanded: undefined,
    roleLink: undefined,
  }
)

const emit = defineEmits<{
  (e: 'click'): void
}>()

const button = ref<HTMLButtonElement>()

const clickButton = (e: Event) => {
  if (!props.action) {
    e.preventDefault()
    if (!props.disabled) {
      emit('click')
      button.value?.focus()
    }
  }
}
</script>

<style scoped lang="scss">
@media (max-width: 50em) {
  .button {
    width: 100%;
  }
}
form button {
  margin-top: 9px;
}

.inline-form {
  display: inline-block;
  margin-right: 1em;
}

.disabled {
  cursor: not-allowed;
}

.button--primary[aria-disabled='true'] {
  background-color: $primary-darker !important;
  color: white !important;
}
</style>
