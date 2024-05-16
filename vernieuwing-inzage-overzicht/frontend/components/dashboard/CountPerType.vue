<template>
  <div>
    <div class="block-info">
      <div class="rows">
        <h3 id="title">
          {{ title }}
        </h3>
        <div class="row">
          <table class="table table--condensed" aria-describedby="title">
            <thead>
              <tr>
                <th class="u-columnwidth-50p">
                  <span>{{ value }} </span>
                </th>
                <th class="u-columnwidth-10p">{{ numberOfEvtps }}</th>
              </tr>
            </thead>
            <tbody>
              <tr
                v-for="row in oeStatistics.oe_by_evtp_total"
                :key="row.naam_officieel"
              >
                <td class="word-break">
                  {{ row.naam_officieel }}
                </td>
                <td>
                  <b>
                    {{ row.count }}
                  </b>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue'

import dashboardService from '../../services/dashboard'
import type { OeStatisticsList } from '../../types/besluit'

const { t } = useI18n()
const title = computed(() => t('dashboard.countPerTypeTitle'))
const value = computed(() => t('dashboard.value'))
const numberOfEvtps = computed(() => t('dashboard.numberOfEvtps'))

const { data } = await dashboardService.getOeStatistics()
const oeStatistics = ref<OeStatisticsList>(data.value as OeStatisticsList)
</script>

<style lang="scss">
.block-info {
  max-width: 100%;
}
.word-break {
  word-break: break-word;
}
.select-block {
  display: block;
}

.borderless-left {
  border-left: 0 !important;
}
</style>
