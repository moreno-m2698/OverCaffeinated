<script setup lang="ts">
import { ref } from "vue";

import VueApexCharts from "vue3-apexcharts";

type Series = {
  name?: string,
  data?: Point
}

type Point = {
  x: number,
  y: number
}

defineProps<{
    series: Series
}>()

const chartOptions = ref({
  chart: {
    id: 'vuechart-example'
  },
  dataLabels: {
    enabled: false,
  },
  xaxis: {
    type: 'datetime',
    labels: {
      datetimeFormatter: { // This is formatted to utc
        year: 'yyyy',
        month: "MMM 'yy",
        day: 'dd MMM',
        hour: 'HH:mm',
        minute: 'HH:mm:ss TT',
        second: 'HH:mm:ss TT',
      }
    }
  }
});


</script>

<template>
    <div id="appl">
      <VueApexCharts
        type="area"
        height="350"
        :options="chartOptions"
        :series="series"
      />
    </div>
</template>