<template>
  <div>
    <apexchart
      type="bar"
      :options="chartOptions"
      :series="series"
    />
  </div>
</template>

<script lang="ts">
import { defineComponent } from "vue"
import VueApexCharts from "vue3-apexcharts"


export default defineComponent({
	name: "BarChart",
	components: {
		apexchart: VueApexCharts,
  },
	props: {
		chartOptions: {
			type: Object,
			required: true,
			default: () => {
				return {
					chart: Object,
					xaxis: Object,
          title: Object,
				}
			},
		},
		categories: {
			type: Array,
			required: true,
			default: () => { },
		},
		series: {
			type: Object,
			required: true,
			default: () => {
				return {
					name: String,
					data: Array,
				}
			},
		},
	},
})
</script>

<style scoped lang="scss">
@import "/src/styles/styles.scss";

</style>
