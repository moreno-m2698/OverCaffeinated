<script setup lang="ts">
import { ref, watch, onMounted } from "vue";
import axios from "axios";
import VueApexCharts from "vue3-apexcharts";

const HL = 6 * 60 * 60 * 1000; // half-life in milliseconds
const K = Math.log(2) / HL; // Caffeine decay constant

type User = {
  id: number,
  username: string,
  lastObservation: number,
  caffeine: number
}

type Drink = {
  id: number,
  name: string,
  caffeine: number,
  date: string
}

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

const drinks = ref<Drink[]>(mockDrinkData);
const drinkName = ref("");
const drinkCaffeine = ref(200);

const mockUser = { // TODO: User is tied to app instance will need to import with props in final
  id: 1,
  username: "janedoe",
  password: "secret",
  lastObservation: today.valueOf(),
  caffeine: 200
}

const user = ref<User>(mockUser);

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


function getSeries(caffeine: number | null = null, time: Date | null = null) {

// TODO: Add a drink to drink posts
// 
// Validate drink object
// True:
//  Create new drink object
//  Add drink object to drink posts
//  Update series for graph
// False:
//  Send a 400 code

  let res = []
  const MINUTES15 = 1000 * 60 * 15
  if (caffeine === null || time === null) {
    
    // Give the current series based on the users caffeine amount
    const QUARTERHOURS = 24 * 4;

    for (let i = 0; i < QUARTERHOURS; i++) {
      res.push({
        x: today.valueOf() + (MINUTES15 * i),
        y: calcCaffeine(user.value.caffeine, MINUTES15 * i)
      });
    }

    return res;
  }

  else {
    if (series.value[0].data === undefined) {
      console.log("SOMETHING VERY BAD HAS HAPPENED")
      return
    }

    const currentCaffeine = calcCaffeine(user.value.caffeine, time.valueOf() - user.value.lastObservation) + caffeine;
    res = [...series.value[0].data.filter((p) => p.x < time.valueOf())];
    // Update the users's model
    user.value.caffeine = currentCaffeine;
    user.value.lastObservation = time.valueOf();

    for (let i = 0; i < 24 * 4; i++) {
      res.push({
        x: time.valueOf() + (MINUTES15 * i),
        y: calcCaffeine(currentCaffeine, MINUTES15 * i)
      })
    }

    return res
  }
}

const series = ref([
  {
    name: 'caffeine',
    data: getSeries()
  }
]);


function calcCaffeine(c0: number, t: number) {
  return c0 * Math.exp(-K * t);
}

async function addDrink() {
  
  const errors = []

  if (import.meta.env.MODE === "development") {
    if (!drinkName.value || drinkName.value.length < 0) {
      errors.push("Invalid drink name");
    }

    if (typeof drinkCaffeine.value !== "number" || isNaN(drinkCaffeine.value)) {
      errors.push("Caffeine must be numeric");

    } else if (drinkCaffeine.value < 0) {
      errors.push("Caffeine cannot be negative");
    }

    if (errors.length > 0 ) {
      console.log("Errors: " + errors)
      return; 
    }

    const currentTime = new Date();

    const newDrink: Drink = {
      id: drinks.value.length + 1,
      name: drinkName.value,
      caffeine: drinkCaffeine.value,
      date: currentTime.toISOString()
    }

    drinks.value.push(newDrink)

    series.value[0].data = getSeries(drinkCaffeine.value, currentTime)

    drinkName.value = "";
    drinkCaffeine.value = 0;
  }
  
  else {

  }
}

// TODO: Create function to update the series being shown in the app
// 
// 2. Find caffeine at current time
// 3. Add new caffeine to current time
// 4. Delete all points after current time
// 5. Add new points

function currentCaffeineAlert() {
  alert(user.value.caffeine)
}

onMounted(async () => {
  if (import.meta.env.MODE === "development") {
    console.log("Using mock data for development");
  } else {
    try {
      const response = await axios.get("/api/drinks/");
      drinks.value = response.data;
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