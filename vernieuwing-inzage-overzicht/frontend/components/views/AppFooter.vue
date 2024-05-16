<template>
  <div class="footer" role="contentinfo">
    <div class="footer-content container">
      <div class="footer-text">
        {{ t('footer.text_1') }}
        <NuxtLink :to="{ name: 'footer-contact' }">
          {{ t('footer.text_2') }}</NuxtLink
        >
      </div>
      <div class="footer-links">
        <div v-for="footerKey in footerKeys" :key="footerKey">
          <ul class="list list--linked">
            <li
              v-for="page in footer[footerKey]"
              :key="page.label"
              class="list__item"
            >
              <NuxtLink
                v-if="footerKey != 'external'"
                :to="`/footer${page.path}`"
              >
                {{ t(`footer.paths.${page.key}`) }}
              </NuxtLink>
              <ExternalLink v-if="footerKey == 'external'" :href="page.path">{{
                t(`footer.paths.${page.key}`)
              }}</ExternalLink>
            </li>
          </ul>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import footer from '@/config/footer'
const { t } = useI18n()

const footerKeys = Object.keys(footer)
</script>

<style scoped lang="scss">
.footer {
  border-top: 0.7em solid $secondary;
  padding: 1.5em 0em;
  background-color: $tertiary;
  height: 13.1em !important;
}

.footer-content {
  display: flex;
  justify-content: space-between;
}

.footer-text {
  max-width: 350px;
  margin-bottom: 1em;
}
.footer-links {
  display: flex;
}

.list {
  margin-left: 15px;
}

@media (max-width: 65em) {
  .footer-content {
    flex-direction: column;
  }
  .footer {
    height: 100% !important;
  }
  .footer-links {
    flex-direction: column;
  }
}
</style>
