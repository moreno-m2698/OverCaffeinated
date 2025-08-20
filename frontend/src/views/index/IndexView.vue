<script setup lang="ts">
import { ref, watch, onMounted } from "vue";
import { useAuthStore } from "../../stores/auth";
import axios from "axios";

import CaffeineGraph from "./components/CaffeineGraph.vue";
import DrinkForm from "./components/DrinkForm.vue";
import DrinkFeed from "./components/DrinkFeed.vue";

const store = useAuthStore();

type Drink = {
  id: number;
  name: string;
  caffeine: number;
  date: string;
  userId: number
};
type Point = { x: number; y: number };
type Series = { name?: string; data?: Point[] };

const drinks = ref<Drink[]>([]);
const series = ref<Series[]>([{ name: "caffeine", data: [] }]);

const HL = 6 * 60 * 60 * 1000; // half-life in ms
const K = Math.log(2) / HL;    // decay constant

function calcCaffeine(c0: number, t: number) {
  return c0 * Math.exp(-K * t);
}

// TODO: Component mounting ( I should display the component whether or not 
// the data has come in yet)
// Series: Needs ability to listen when a drink is added/user checks caffeine
// Display a loading box until:
// Mount Series:
//  Request series data from server
//  Display Data

// Feed:
// Display loading boxes:
// Mount:
//  

function getSeries(caffeine: number | null = null, time: Date | null = null) {
  const res: Point[] = [];
  const MINUTES30 = 1000 * 60 * 30;
  const userCaffeine = store.user?.caffeine ?? 0;
  const userLastObs = store.user?.lastObservation ?? 0;

  if (caffeine === null || time === null) {
    const today = new Date();
    today.setUTCHours(0, 0, 0, 0);

    for (let i = 0; i < 24 * 2; i++) {
      res.push({
        x: today.valueOf() + MINUTES30 * i,
        y: calcCaffeine(userCaffeine, MINUTES30 * i),
      });
    }
    return res;
  } else {
    const currentCaffeine =
      calcCaffeine(userCaffeine, time.valueOf() - userLastObs) + caffeine;

    if (store.user) {
      store.user.caffeine = currentCaffeine;
      store.user.lastObservation = time.valueOf();
    }

    const oldData = series.value[0].data ?? [];
    const before = oldData.filter((p) => p.x < time.valueOf());
    const after: Point[] = [];

    for (let i = 0; i < 24 * 2; i++) {
      after.push({
        x: time.valueOf() + MINUTES30 * i,
        y: calcCaffeine(currentCaffeine, MINUTES30 * i),
      });
    }

    return [...before, ...after];
  }
}

// Something broke here
async function postDrink(name: string, caffeine: number) {
  if (import.meta.env.MODE === "development") {
    const current = new Date();
    const drink: Drink = {
      id: drinks.value.length + 1,
      name,
      caffeine,
      date: current.toISOString(),
      userId: 1
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

onMounted(async () => {
  if (import.meta.env.MODE === "development") {

    console.log("Using mock data for development");
    const today = new Date();
    today.setUTCHours(0, 0, 0, 0);
    const yesterday = new Date(today.valueOf() - 24 * 60 * 60 * 1000);
    drinks.value = drinks.value = [
      { id: 1, name: "Espresso", caffeine: 80, date: yesterday.toISOString(), userId: 1 },
      { id: 2, name: "Latte", caffeine: 100, date: yesterday.toISOString(), userId: 1 },
      { id: 3, name: "Cold Brew", caffeine: 200, date: yesterday.toISOString(), userId: 1 },
    ];

    series.value[0].data = getSeries();

  } else {
    try {
      const response = await axios.get("/api/drinks?userId="+store.user!.id);
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
    if (import.meta.env.MODE === "development") {
      // when drinks are added we want to update the user's 
      // caffeine & observation time
    }
  },
  { deep: true }
);
</script>

<template>
  <div>
    <h1>Welcome User: {{ store.user?.username }}</h1>
    <CaffeineGraph :series="series" />
    <DrinkFeed :drinks="drinks"/>
    <DrinkForm @submit="postDrink" />
  </div>
</template>