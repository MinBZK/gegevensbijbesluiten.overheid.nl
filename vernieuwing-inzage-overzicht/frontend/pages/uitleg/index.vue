<template>
  <div class="container">
    <h1 class="h1 margin-top">
      {{ t(`uitleg.h1`) }}
    </h1>
    <h2>{{ t(`uitleg.h2`) }}</h2>
    <img src="@/assets/images/explanation-2.svg" alt="" />
    <ol class="columns">
      <li class="cols">
        <div class="list-item">1</div>
        <p class="p-bold">{{ t(`uitleg.li1`) }}</p>
        <p>
          {{ t(`uitleg.li1_1`) }}
        </p>
      </li>
      <li class="cols">
        <div class="list-item">2</div>
        <p class="p-bold">
          {{ t(`uitleg.li2`) }}
        </p>
        <p>
          {{ t(`uitleg.li2_1`) }}
        </p>
      </li>
      <li class="cols">
        <div class="list-item">3</div>
        <p class="p-bold">
          {{ t(`uitleg.li3`) }}
        </p>
        <p>
          {{ t(`uitleg.li3_1`) }}
        </p>
      </li>
    </ol>
  </div>
</template>

<script setup lang="ts">
const { t } = useI18n()

useHead({ title: t('navigation.uitleg') })
</script>

<style scoped lang="scss">
.list-item {
  display: flex;
  align-items: baseline;
  justify-content: center;
  width: 1.5em;
  height: 1.5em;
  background-color: $primary-dark;
  color: #fff;
  border-radius: 1em;
  margin-right: 0.5em;
  float: left;
}
ol {
  padding: 0em;
}
.p-bold {
  font-weight: bold;
}
img {
  padding-bottom: 1em;
}
</style>
