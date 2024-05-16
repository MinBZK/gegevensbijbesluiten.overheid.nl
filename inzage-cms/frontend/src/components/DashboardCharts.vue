<template>
  <v-row>
    <v-col
      cols="10"
      lg="6"
    >
      <BarChart
        :chart-options="chartOptions"
        :categories="categories"
        :series="series"
      />
    </v-col>
    <v-col
      cols="10"
      lg="6"
      style="padding: 0em"
    >
      <v-table>
        <thead>
          <tr>
            <th class="text-left">
              Verantwoordelijke organisatie
            </th>
            <th
              v-for="(status, indexstatus) in statusOe.columns"
              :key="indexstatus"
              class="text-middle"
            >
              {{ status }}
            </th>
          </tr>
        </thead>
        <tbody>
          <tr
            v-for="(oe, indexOe) in statusOe.index"
            :key="indexOe"
          >
            <td>{{ oe }}</td>
            <td
              v-for="(item, indexOeNested) in statusOe.data[indexOe]"
              :key="indexOeNested"
            >
              {{ item }}
            </td>
          </tr>
        </tbody>
      </v-table>
    </v-col>
  </v-row>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import axios from 'axios'
import store from '@/store/index'
import { Table } from '@/types/Tables'
import { StatusOe } from '@/types/PublicatieStatus'
import type { PropType } from 'vue'
import BarChart from '@/components/ApexCharts/BarChart.vue'

export default defineComponent({
  name: 'DashboardCharts',
  components: {
    BarChart,
  },
  props: {
    tables: {
      type: Array as PropType<Table[]>,
      required: true,
    },
  },
  data() {
    return {
      chartOptions: {
        chart: {
          id: 'chart-status',
        },
        xaxis: {
          categories: [] as string[],
          style: {
            colors: [
              '#800000',
              '#FF0000',
              '#FFFF00',
              '#FFFF00',
              '#FFFF00',
              '#800000',
            ],
            fontSize: '17px',
          },
        },
        title: {
          text: '',
        },
      },
      series: [
        {
          name: '',
          data: [] as number[],
        },
      ],
      categories: [] as string[],
      statusEvtp: [] as number[],
      statusOe: {} as StatusOe,
      valid: false,
      state: 'idle',
      error: undefined,
      detail: [],
    }
  },
  computed: {},
  async created() {
    await this.getStatusEvtp()
    await this.getStatusOe()
    this.updateChart()
  },
  methods: {
    async getStatusEvtp() {
      this.state = 'loading'
      this.error = undefined
      await axios
        .get(`${store.state.APIurl}/evtp-version/publicatiestatus/evtp/`)
        .then((response) => {
          this.statusEvtp = response.data
          this.state = 'loaded'
        })
        .catch((error) => {
          if (error.response.status >= 400) {
            this.detail = error.response
          }
          this.state = 'failed'
          this.error = error
        })
    },
    async getStatusOe() {
      this.state = 'loading'
      this.error = undefined
      await axios
        .get(`${store.state.APIurl}/evtp-version/publicatiestatus/oe/`)
        .then((response) => {
          this.statusOe = response.data
          this.state = 'loaded'
        })
        .catch((error) => {
          if (error.response.status >= 400) {
            this.detail = error.response
          }
          this.state = 'failed'
          this.error = error
        })
    },
    updateChart() {
      this.chartOptions = {
        chart: {
          id: 'chart-status',
        },
        xaxis: {
          categories: Object.keys(this.statusEvtp),
          style: {
            colors: [
              '#800000',
              '#FF0000',
              '#FFFF00',
              '#FFFF00',
              '#FFFF00',
              '#800000',
            ],
            fontSize: '19px',
          },
        },
        title: {
          text: 'Aantallen per status',
        },
      }
      this.series = [
        {
          name: 'Besluiten',
          data: Object.values(this.statusEvtp),
        },
      ]
    },
  },
})
</script>

<style scoped lang="scss">
@import '/src/styles/styles.scss';

tbody tr:nth-of-type(odd) {
  background-color: $tertiary;
}

table {
  border: 0;
}
</style>
