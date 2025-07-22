<script setup lang="ts">
import { ref, watch, onMounted } from "vue";
import axios from "axios";
import VueApexCharts from "vue3-apexcharts";

const drinks = ref<any[]>([]);
const drinkName = ref("");
const drinkCaffeine = ref(200);
const drinkData = ref<any[]>([]);
const user = ref<any>({});


const today = new Date();
today.setUTCHours(0);
today.setUTCMinutes(0);
today.setUTCSeconds(0);
today.setUTCMilliseconds(0);

const yesterday = new Date(today.valueOf() - 24 * 60 * 60 * 1000)
const tomorrow = new Date(today.valueOf() + 24 * 60 * 60 * 1000)
const mockDrinkData = [
  { id: 1, name: "Espresso", caffeine: 80, date: yesterday.toISOString() },
  { id: 2, name: "Latte", caffeine: 100, date: yesterday.toISOString() },
  { id: 3, name: "Cold Brew", caffeine: 200, date: yesterday.toISOString() },
];

const mockUser = { // TODO: User is tied to app instance will need to import with props in final
  id: 1,
  username: "HelloWorld",
  observationTime: today.valueOf(),
  observationCaffeine: 200
}

const chartOptions = ref({
  chart: {
    id: 'vuechart-example'
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
})

const HL = 6 * 60 * 60 * 1000; // half-life in milliseconds
const K = Math.log(2) / HL; // Caffeine decay constant
function calcCaffeine(c0: number, t: number) {
  return c0 * Math.exp(-K * t);
}

function getInitialData() {

  const data = []
  const len15Min = 1000 * 60 * 15
  let caffeine = mockUser.observationCaffeine
  for ( let i = 0; i < 24 * 4; i++ ) {
    data.push({
      x: (today.valueOf() + (len15Min * i)),
      y: calcCaffeine(caffeine, i * len15Min).toFixed(2)
    })
  }
  
  return data;
}

const series = ref([
  {
    name: 'caffeine',
    data: getInitialData()
  }
])

//TODO:  A join table can be created to plot caffeine over time

function addDrink() {
  const now = new Date();

  drinks.value.push({
    id: drinks.value.length + 1,
    name: drinkName.value,
    caffeine: drinkCaffeine.value,
    date: now.toISOString(),
  });

  const currentCaffeine = calcCaffeine(user.value.observationCaffeine, now.valueOf() - user.value.observationTime) + drinkCaffeine.value
  const head = series.value[0].data.filter((p) => p.x < now.valueOf())

  user.value.observationCaffeine = currentCaffeine
  user.value.observationTime = now.valueOf()

  const remainingTime = tomorrow.valueOf() - now.valueOf();
  const init = Math.ceil(remainingTime / (1000 * 60 * 15))
  const tail = []
  const len15Min = 1000 * 60 * 15

  for (let i = init; i <= 24 * 4; i++) {
    tail.push({
      x: (today.valueOf() + (len15Min * i)),
      y: calcCaffeine(currentCaffeine, (i - init) * len15Min).toFixed(2)
    })
  }

  series.value[0].data = [...head, {x: now.valueOf(), y: currentCaffeine.toString() }, ...tail]

  drinkName.value = "";
  drinkCaffeine.value = 200;
}

function currentCaffeineAlert() {
  alert(user.value.observationCaffeine)
}

onMounted(async () => {
  if (import.meta.env.MODE === "development") {
    drinks.value = mockDrinkData;
    user.value = mockUser
    console.log("Using mock data for development");
  } else {
    try {
      const response = await axios.get("/drinks/");
      drinkData.value = response.data;
      console.log("Fetched drink data from API");
    } catch (error) {
      console.error("Failed to fetch data:", error);
    }
  }
});

watch(
  drinks,
  () => {
    console.log("Current drinks:", drinks.value);
    console.log(new Date());
  },
  { deep: true }
);
</script>

<template>
  <div>

    <h1>Welcome User: {{ user.username }}</h1>

    <div id="appl">
      <VueApexCharts
        type="area"
        height="350"
        :options="chartOptions"
        :series="series"
      />
    </div>

    <table>
      <thead>
        <tr>
          <th>Drink/ID</th>
          <th>Caffeine (mg)</th>
          <th>Date/Time</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="drink in drinks" :key="drink.id">
          <td>{{ drink.name }} (ID: {{ drink.id }})</td>
          <td>{{ drink.caffeine }}mg</td>
          <td>{{ drink.date }}</td>
        </tr>
      </tbody>
    </table>

    <form @submit.prevent="addDrink">
      <input
        name="drink"
        type="text"
        v-model="drinkName"
        placeholder="Drink name"
        required
      />
      <input
        name="caffeine"
        type="number"
        v-model="drinkCaffeine"
        min="0"
        step="0.1"
        required
      />
      <button type="submit">Submit</button>
    </form>
    <button @click="currentCaffeineAlert">currentCaffeine</button>
  </div>
</template>