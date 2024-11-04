<template>
  <div
    v-if="modelValue"
    class="modal-background"
    role="dialog"
    aria-modal="true"
    @click.self="$emit('update:modelValue', false)"
  >
    <div class="modal-view">
      <button
        class="close-button"
        :aria-label="$t('closeSubjectTile')"
        @click="$emit('update:modelValue', false)"
      >
        <NuxtIcon name="mdi:close-thick" />
      </button>
      <slot />
    </div>
  </div>
</template>

<script setup lang="ts">
const props = withDefaults(
  defineProps<{
    modelValue: boolean
    height?: string
    width?: string
    maxHeight?: string
    modalTitle?: string
    indexModalTitle?: number
  }>(),
  {
    width: 'auto',
    height: 'auto',
    maxHeight: 'auto',
    modalTitle: '',
    indexModalTitle: 0
  }
)

const emit = defineEmits<{
  (e: 'update:modelValue', modelValue: boolean): void
}>()

onMounted(() => {
  const escListener = (event: any) => {
    if (event.key === 'Escape') {
      emit('update:modelValue', false)
    }
  }
  window.addEventListener('keydown', escListener)
  onBeforeUnmount(() => {
    window.removeEventListener('keydown', escListener)
  })
})

const unfocus = (modelValue: boolean) => {
  const focusableElements = document.querySelectorAll(`
      a:not(.modal-view):not(.modal-view *),
      div:not(.modal-view):not(.modal-view *),
      input:not(.modal-view):not(.modal-view *),
      button:not(.modal-view):not(.modal-view *)
      `)
  if (modelValue) {
    document.body.style.overflow = 'hidden'
    focusableElements.forEach((el) => {
      if (el.hasAttribute('tabindex')) {
        // temporary store tabindex
        el.setAttribute('data-original-tabindex', el.getAttribute('tabindex') as string)
      }
    })
    focusableElements.forEach((el) => el.setAttribute('tabindex', '-2'))
  } else {
    document.body.style.overflow = ''
    focusableElements.forEach((el) => el.removeAttribute('tabindex'))

    focusableElements.forEach((el) => {
      // reset tabindex
      if (el.hasAttribute('data-original-tabindex')) {
        el.setAttribute('tabindex', el.getAttribute('data-original-tabindex') as string)
      }
    })
  }
}

onBeforeUnmount(() => {
  unfocus(false)
})

watch(
  () => props.modelValue,
  (modelValue) => {
    unfocus(modelValue)
  }
)

onBeforeUnmount(() => {
  document.body.style.overflow = ''
})
</script>

<style scoped lang="scss">
.modal-background {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background-color: rgba(0, 0, 0, 0.5);
  z-index: 10;
  padding: 1em;
  border: 10em;

  display: flex;
  justify-content: center;
  align-items: center;
}

.modal-view {
  position: relative;
  padding: 0.8em;
  background-color: $tertiary;
  border: 10px white solid;
  border-radius: 8px;
  overflow-y: auto;
  width: v-bind('width');
  height: v-bind('height');
  max-height: v-bind('maxHeight');
}
.icon {
  padding-left: 0px !important;
}
</style>
<style global>
.slot {
  background-color: aqua;
}
</style>
