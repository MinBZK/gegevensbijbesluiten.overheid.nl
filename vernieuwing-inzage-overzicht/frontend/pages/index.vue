<template>
  <div>
    <div class="container">
      <SearchBar :search-explanation="t('pages.onderwerpen.searchText')" />
    </div>
    <div class="container">
      <div class="section onderwerpen-section">
        <h2 class="h2">{{ t('onderwerpen.title') }}</h2>
        <OnderwerpenCards :number-of-tiles="6" :show-icons="false" />
        <FormOverheidButton
          class="meer-onderwerpen-button"
          :label="t('onderwerpen.moreButton')"
          :full-width="true"
          @click="() => $router.push({ name: 'onderwerp' })"
        />
      </div>
    </div>
    <div class="section faq-section">
      <h2>{{ t('faq.title') }}</h2>
      <FrontpageFrequentlyAskedQuestions />
    </div>
    <div class="container">
      <div class="section news-section mobile-section">
        <h2>{{ t('articles.title') }}</h2>
        <FrontpageNewsArticles />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
const { t } = useI18n()

definePageMeta({
  title: 'Home',
})
providePageTitle({
  title: 'homepageTitle',
  labelType: 'locale-index',
})
</script>

<style scoped lang="scss">
.section {
  display: flex;
  flex-direction: column;
  align-items: center;
  row-gap: 0.25em;
}
.news-section {
  padding-top: 4em;
  margin-bottom: 4em;

  @media (max-width: 50em) {
    padding-top: 0em;
    margin-top: 3em;
    margin-bottom: 3em;
  }
}
.faq-section {
  padding-top: 2em;
  padding-bottom: 2.5em;
  background-color: $tertiary;
  row-gap: 0em;
}
.meer-onderwerpen-button {
  width: 17em !important;
}

.onderwerpen-section {
  margin-bottom: 4em;

  @media (max-width: 50em) {
    margin-bottom: 3em;
    row-gap: 0.75em;
  }
}
</style>
