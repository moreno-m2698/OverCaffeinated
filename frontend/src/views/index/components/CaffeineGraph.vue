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

const today = new Date()

const chartOptions = ref({
  annotations: {
    yaxis: [
      {
        y: 50,
        label: {
          text: "ok"
        }
      },
      {
        y: 100,
        label: {
          text: "good"
        }
      },
      {
        y: 200,
        label: {
          text: "oof"
        }
      },
      {
        y: 400,
        label: {
          text: "NO"
        }
      }

    ]
  },
  chart: {
    id: 'vuechart-example',
    toolbar: {
      show: false
    }
  },
  dataLabels: {
    enabled: false,
  },
  grid: {
    xaxis: {
      lines: {
        show: true
      }
    },
    yaxis: {
      lines: {
        show: false
      }
    }
  },
  markers: {
    size: 6
  },
  stroke: {
    curve: 'straight'
  },
  tooltip: {
    enabled: false
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
    },
    title: {
      text: today.toDateString()
    }
  },
  yaxis: {
    decimalsInFloat: 2,
    labels: {
      show: true
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