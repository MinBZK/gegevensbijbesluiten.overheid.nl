<template>
  <div class="article-cards">
    <div
      v-for="article in reversedArticles"
      :key="article.title"
      class="article-card"
      @click.prevent="navigateTo(article.link, { external: true, open: { target: '_blank' } })"
      @keydown.enter.prevent="
        navigateTo(article.link, { external: true, open: { target: '_blank' } })
      "
      @keydown.space.prevent="
        navigateTo(article.link, { external: true, open: { target: '_blank' } })
      "
    >
      <img :src="article.image" alt="" class="article-card-image" tabindex="-1" />
      <div class="article-card-text">
        <h3 class="no-margin">{{ t(article.title) }}</h3>
        <p>{{ t(article.date) }}</p>
        <p>{{ t(article.summary) }}</p>
        <ExternalLink :href="article.link" class="external-link">
          <span aria-hidden="true">{{ t('articles.readMore') }}</span>
          <span class="sr-only">{{ t('articles.readMoreArticle', { n: t(article.title) }) }}</span>
        </ExternalLink>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { articles } from '@/config/articles'

const reversedArticles = computed(() => {
  return articles.slice(-3).reverse()
})

const { t } = useI18n()
</script>

<style scoped lang="scss">
.article-cards {
  display: flex;
  column-gap: 1em;
  max-width: 72em;
}

.article-card {
  background-color: white;
  width: 33%;
  border-radius: 4px;
  box-shadow: 0 0 3px rgb(147, 180, 205);

  transition: box-shadow 0.3s ease-out;

  &:hover {
    box-shadow: 0 0 10px rgb(147, 180, 205);
    cursor: pointer;
  }

  .article-card-text {
    padding: 1em;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    height: calc(100% - 250px);

    h3 {
      margin-top: 0em;
      font-size: 1em;
    }

    .external-link {
      margin-top: auto;
      width: 11.3em;
      justify-content: center;
      display: flex;
      align-items: center;
      background-position: 10.2em;
    }
  }
}

@media (max-width: 50em) {
  .article-cards {
    flex-direction: column;
    row-gap: 0.85em;
  }

  .article-card {
    width: 100%;
  }
}

.article-card-image {
  width: 100%;
  height: 250px;

  border-top-right-radius: 4px;
  border-top-left-radius: 4px;
  object-fit: cover;
}
</style>
