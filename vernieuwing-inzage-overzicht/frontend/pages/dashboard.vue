<template>
  <div class="container">
    <h1 class="banner">Dashboard</h1>
    <h2>{{ totalCountText }}:&nbsp; {{ evtpCount }}</h2>
    <h2>{{ currentDate }}</h2>
    <div class="block-cards">
      <DashboardCountPerType class="block-cards__card" />
    </div>
  </div>
</template>

<script setup lang="ts">
import dashboardService from '@/services/dashboard'

const { t } = useI18n()
const totalCountText = computed(() => t('dashboard.totalCountText'))

const date = new Date()
const currentDate = computed(() => {
  const month: string = t(`months.${date.getMonth() + 1}`)
  const monthDay: string = date.getDate().toString()
  const year: string = date.getFullYear().toString()
  const hours: string = date.getHours().toString()
  const minutes: string =
    date.getMinutes() < 10 ? '0'.concat(date.getMinutes().toString()) : date.getMinutes().toString()

  return monthDay + ' ' + month + ' ' + year + ' | ' + hours + ':' + minutes
})

const { data } = await dashboardService.getTotalCount()
const evtpCount = data

definePageMeta({
  title: 'Dashboard'
})
useHead({ title: 'Dashboard' })
</script>

<style scoped lang="scss">
@media (min-width: 85em) {
  .block-cards__card:first-child {
    padding-right: 2em !important;
  }
  .block-cards__card {
    width: 50% !important;
    height: 100%;
  }
}
.block-cards {
  padding-top: 2em;
}
.block-cards__card {
  margin-bottom: 0em;
  padding-bottom: 1em;
}
h2 {
  font-size: 1.4rem !important;
  margin-bottom: 0.2em;
}
h1 {
  margin-bottom: 0.4em;
}
.banner {
  padding-top: 30px;
}
</style>
