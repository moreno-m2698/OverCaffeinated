<script setup lang="ts">
import { ref, watch, onMounted } from "vue";
import { useAuthStore } from "../../stores/auth";

import axios from "axios";

import CaffieneGraph from "./components/CaffieneGraph.vue";
import DrinkForm from "./components/DrinkForm.vue";

const store = useAuthStore()

type Drink = {
  id: number,
  name: string,
  caffeine: number,
  date: string
}

const drinks = ref<Drink[]>([]);

type Series = {
  name?: string,
  data?: Point[]
}

type Point = {
  x: number,
  y: number
}

const series = ref<Series[]>([
  {
    name: '',
    data: []
  }
]);

const HL = 6 * 60 * 60 * 1000; // half-life in milliseconds
const K = Math.log(2) / HL; // Caffeine decay constant

function getSeries(caffeine: number | null = null, time: Date | null = null) {

  let res = []
  const MINUTES15 = 1000 * 60 * 15

  if (caffeine === null || time === null) {
    
    const today = new Date();
    today.setUTCHours(0);
    today.setUTCMinutes(0);
    today.setUTCSeconds(0);
    today.setUTCMilliseconds(0);

    // Give the current series based on the users caffeine amount
    const AMOUNT15MINUTEINTERVALSINDAY = 24 * 4;

    for (let i = 0; i < AMOUNT15MINUTEINTERVALSINDAY; i++) {
      res.push({
        x: today.valueOf() + (MINUTES15 * i),
        y: calcCaffeine(store.user?.caffeine, MINUTES15 * i)
      });
    }

    return res;
  }

  else {
    if (series.value[0].data === undefined) {
      console.log("SOMETHING VERY BAD HAS HAPPENED")
      return
    }

    const currentCaffeine = calcCaffeine(store.user?.caffeine, time.valueOf() - user.value!.lastObservation) + caffeine;
    res = [...series.value[0].data.filter((p) => p.x < time.valueOf())];

    // Updates the user model
    store.user.caffeine = currentCaffeine;
    store.user.lastObservation = time.valueOf();

    for (let i = 0; i < 24 * 4; i++) {
      
      res.push({
        x: time.valueOf() + (MINUTES15 * i),
        y: calcCaffeine(currentCaffeine, MINUTES15 * i)
      })
    }

    return res
  }
}

function calcCaffeine(c0: number, t: number) {
  return c0 * Math.exp(-K * t);
}

async function postDrink(name: string, caffeine: number) {
  if (import.meta.env.MODE = "development") {
    const current = new Date(); 
    const drink: Drink = {
      id: drinks.value.length + 1,
      name: name,
      caffeine: caffeine,
      date: current.toISOString()
    };
    
    drinks.value.push(drink);

    series.value[0].data = getSeries(caffeine, current);
  }

  else {

  }

}

function currentCaffeineAlert() {
  alert(store.user.caffeine)
}


function init() {
  if (import.meta.env.MODE === "development") {
    const today = new Date();
    today.setUTCHours(0);
    today.setUTCMinutes(0);
    today.setUTCSeconds(0);
    today.setUTCMilliseconds(0);

    const yesterday = new Date(today.valueOf() - 24 * 60 * 60 * 1000)
    const mockDrinkData = [
      { id: 1, name: "Espresso", caffeine: 80, date: yesterday.toISOString() },
      { id: 2, name: "Latte", caffeine: 100, date: yesterday.toISOString() },
      { id: 3, name: "Cold Brew", caffeine: 200, date: yesterday.toISOString() },
    ];
    drinks.value = mockDrinkData

    series.value[0].data = getSeries()
    series.value[0].name = "caffeine"

  }

  else {
    const today = new Date();
    today.setUTCHours(0);
    today.setUTCMinutes(0);
    today.setUTCSeconds(0);
    today.setUTCMilliseconds(0);

    const yesterday = new Date(today.valueOf() - 24 * 60 * 60 * 1000)
    const mockDrinkData = [
      { id: 1, name: "Espresso", caffeine: 80, date: yesterday.toISOString() },
      { id: 2, name: "Latte", caffeine: 100, date: yesterday.toISOString() },
      { id: 3, name: "Cold Brew", caffeine: 200, date: yesterday.toISOString() },
    ];
    
    drinks.value = mockDrinkData

    series.value[0].data = getSeries()
    series.value[0].name = "caffeine"
  }
}

init()

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

    <h1>Welcome User: {{ store.user?.username }}</h1>
    <CaffieneGraph :series="series"/>
    <!-- Remove this table later -->
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
    <DrinkForm @submit="postDrink"/>
    <button @click="currentCaffeineAlert">currentCaffeine</button>
  </div>
</template>