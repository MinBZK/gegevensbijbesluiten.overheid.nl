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
  }>(),
  {
    width: 'auto',
    height: 'auto',
    maxHeight: 'auto'
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
const focusableElements = 'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'

const handleFocus = (e: KeyboardEvent) => {
  const isTabPressed = e.key === 'Tab'

  if (!isTabPressed) return
  const modal = document.querySelector('.modal-view')
  const firstFocusableElement = modal?.querySelectorAll(focusableElements)[0]
  const focusableContent = modal?.querySelectorAll(focusableElements)
  const lastFocusableElement = focusableContent?.[focusableContent.length - 1]

  if (!modal || !firstFocusableElement || !lastFocusableElement) return

  if (e.shiftKey) {
    if (document.activeElement === firstFocusableElement) {
      ;(lastFocusableElement as HTMLElement)?.focus()
      e.preventDefault()
    }
  } else if (document.activeElement === lastFocusableElement) {
    ;(firstFocusableElement as HTMLElement)?.focus()
    e.preventDefault()
  }
}

const trapFocus = (enable: boolean) => {
  if (enable) {
    document.addEventListener('keydown', handleFocus)
    const modal = document.querySelector('.modal-view')
    const firstFocusableElement = modal?.querySelectorAll(focusableElements)[0]
    if (firstFocusableElement) {
      ;(firstFocusableElement as HTMLElement)?.focus()
    }
  } else {
    document.removeEventListener('keydown', handleFocus)
  }
}

onBeforeUnmount(() => {
  trapFocus(false)
})

watch(
  () => props.modelValue,
  (modelValue) => {
    trapFocus(modelValue)
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
