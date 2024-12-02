<template>
  <header class="header no-margin">
    <div class="header__start">
      <div class="container">
        <button
          type="button"
          class="hidden-desktop button button--icon-hamburger"
          data-handler="toggle-nav"
          aria-controls="nav"
          tabindex="3"
          :aria-expanded="menuExpanded ? 'true' : 'false'"
          @click="menuExpanded = !menuExpanded"
        >
          Menu
        </button>
        <div class="logo">
          <NuxtLink :to="{ name: 'index' }" tabindex="2">
            <img
              src="@/assets/images/logo.svg"
              :alt="`Logo Overheid.nl, ga naar de startpagina ${url}`"
            />
          </NuxtLink>
          <div class="logo__you-are-here">
            <p class="visually-hidden">U bent nu hier:</p>
            <p>
              {{ t(`logoCaption`) }}
              {{ $colorMode.value === 'concept' ? '(Concept)' : '' }}
            </p>
          </div>
        </div>
      </div>
    </div>
    <nav id="nav" class="header__nav" :class="!menuExpanded && 'header__nav--closed'">
      <div class="container">
        <ul>
          <li
            v-for="item in navigationHeaders"
            :key="item.label"
            :class="{
              active: item.highlightOnRoutes.includes(currentRoute.name as string)
            }"
          >
            <NuxtLink
              :to="{ name: item.routeName }"
              class="focus-border"
              @click="menuExpanded = false"
              >{{ t(`${item.label}`) }}</NuxtLink
            >
          </li>
        </ul>
      </div>
    </nav>
  </header>
</template>

<script setup lang="ts">
import { navigationHeaders } from '@/config/navigation'
const { t } = useI18n()

const currentRoute = useRoute()
const menuExpanded = ref<boolean>(false)
const url = (process.env.NUXT_PUBLIC_API_BASE_URL?.replace('/api', '') ||
  'gegevensbijbesluiten.overheid.nl') as string

// set expanded to false after route change
watch(currentRoute, () => (menuExpanded.value = false))
</script>

<style scoped lang="scss">
// fix mismatch in min-width from koop
@media (min-width: 50em) {
  .header__nav--closed {
    display: block;
    z-index: auto;
  }
  .header__nav ul {
    flex-direction: row !important;
  }
}

.active a {
  background-color: $secondary;
  color: $primary-darker !important;
}
a:focus {
  background-color: $secondary;
  color: $primary-dark;
}
</style>
