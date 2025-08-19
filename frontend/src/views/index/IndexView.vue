<script setup lang="ts">
import { ref, watch, onMounted } from "vue";
import { useAuthStore } from "../../stores/auth";
import axios from "axios";

import CaffieneGraph from "./components/CaffieneGraph.vue";
import DrinkForm from "./components/DrinkForm.vue";

const store = useAuthStore();

type Drink = {
  id: number;
  name: string;
  caffeine: number;
  date: string;
};

const drinks = ref<Drink[]>([]);

type Point = { x: number; y: number };
type Series = { name?: string; data?: Point[] };

const series = ref<Series[]>([{ name: "caffeine", data: [] }]);

const HL = 6 * 60 * 60 * 1000; // half-life in ms
const K = Math.log(2) / HL;    // decay constant

function calcCaffeine(c0: number, t: number) {
  return c0 * Math.exp(-K * t);
}

function getSeries(caffeine: number | null = null, time: Date | null = null) {
  const res: Point[] = [];
  const MINUTES15 = 1000 * 60 * 15;
  const userCaffeine = store.user?.caffeine ?? 0;
  const userLastObs = store.user?.lastObservation ?? 0;

  if (caffeine === null || time === null) {
    const today = new Date();
    today.setUTCHours(0, 0, 0, 0);

    for (let i = 0; i < 24 * 4; i++) {
      res.push({
        x: today.valueOf() + MINUTES15 * i,
        y: calcCaffeine(userCaffeine, MINUTES15 * i),
      });
    }
    return res;
  } else {
    const currentCaffeine =
      calcCaffeine(userCaffeine, time.valueOf() - userLastObs) + caffeine;

    // update user state
    if (store.user) {
      store.user.caffeine = currentCaffeine;
      store.user.lastObservation = time.valueOf();
    }

    // rebuild series from new event time forward
    const oldData = series.value[0].data ?? [];
    const before = oldData.filter((p) => p.x < time.valueOf());
    const after: Point[] = [];

    for (let i = 0; i < 24 * 4; i++) {
      after.push({
        x: time.valueOf() + MINUTES15 * i,
        y: calcCaffeine(currentCaffeine, MINUTES15 * i),
      });
    }

    return [...before, ...after];
  }
}

async function postDrink(name: string, caffeine: number) {
  if (import.meta.env.MODE === "development") {
    const current = new Date();
    const drink: Drink = {
      id: drinks.value.length + 1,
      name,
      caffeine,
      date: current.toISOString(),
    };
    drinks.value.push(drink);
    series.value[0].data = getSeries(caffeine, current);
  } else {
    try {
      const res = await axios.post("/api/drinks/", { name, caffeine });
      drinks.value.push(res.data);
      series.value[0].data = getSeries(caffeine, new Date(res.data.date));
    } catch (err) {
      console.error("Failed to post drink:", err);
    }
  }
}

function currentCaffeineAlert() {
  alert(store.user?.caffeine ?? 0);
}

function init() {
  const today = new Date();
  today.setUTCHours(0, 0, 0, 0);
  const yesterday = new Date(today.valueOf() - 24 * 60 * 60 * 1000);

  if (import.meta.env.MODE === "development") {
    drinks.value = [
      { id: 1, name: "Espresso", caffeine: 80, date: yesterday.toISOString() },
      { id: 2, name: "Latte", caffeine: 100, date: yesterday.toISOString() },
      { id: 3, name: "Cold Brew", caffeine: 200, date: yesterday.toISOString() },
    ];
    series.value[0].data = getSeries();
  }
}

init();

onMounted(async () => {
  if (import.meta.env.MODE === "development") {
    console.log("Using mock data for development");
  } else {
    try {
      const response = await axios.get("/api/drinks/");
      drinks.value = response.data;
      series.value[0].data = getSeries();
      console.log("Fetched drink data from API");
    } catch (error) {
      console.error("Failed to fetch drinks:", error);
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
    <CaffieneGraph :series="series" />

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

    <DrinkForm @submit="postDrink" />
    <button @click="currentCaffeineAlert">Current Caffeine</button>
  </div>
</template>