<script setup lang="ts">
import { ref, watch, computed } from "vue";

const drinks = ref<[any]>([]);
const drinkName = ref("");
const drinkCaffeine = ref(200);
const initTime = ref(new Date())
const tcaffeine = ref(0);
// NIH: https://www.ncbi.nlm.nih.gov/books/NBK223808/#:~:text=Structurally%2C%20caffeine%20(and%20the%20other,individuals%20is%20about%205%20hours.
// biological half-life of 5 hrs

const HL = 5 * 60; // Unit minutes 
const K = Math.log(2) / HL; // Units of per minutes

// Wikipedia(biological half-life): https://en.wikipedia.org/wiki/Biological_half-life

// ui look at stock apps, health apps, and animal crossing

function currentCaffeine() {
    const deltaT = (Date.now() - initTime.value.getTime()) / (1000 * 60) // Unit: minutes
    tcaffeine.value = calcCaffeine(totalCaffeine.value, deltaT)
}

function calcCaffeine(c0: number, t: number) {
    return c0 * Math.exp(-K * t)
}

function addDrink() {

    const date = new Date();
    initTime.value = date;

    drinks.value.push({
        "id": drinks.value.length,
        "name": drinkName.value,
        "caffeine": drinkCaffeine.value,
        "date": date.toISOString()
    })
}

const totalCaffeine = computed(() => {
    return drinks.value.reduce((accumulator, drink) => accumulator + drink.caffeine, 0) // Error is here
})

watch(drinks,
    () => {
        console.log("Current drinks: " + drinks.value)
        alert("Current drinks: " + drinks.value)
    },
    { deep: true }
)

</script>

    
<template>
    <body>
        <h2>Total Caffeine</h2>
        <p>
            {{ totalCaffeine }}mg
        </p>
        <h2>Initial Time Reference:</h2> 
        <p>{{ initTime.toDateString() }} : {{ initTime.toTimeString() }}</p>
        <h2>Current Caffeine:</h2>
        <p>{{  tcaffeine }}</p>
        <table>
            <thead>
                <tr>
                    <th>Drink/ID</th>
                    <th>Caffeine(mg)</th>
                    <th>Date/Time</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="drink in drinks">
                    <td>id: {{ drink.id }}</td>
                    <td>caffeine: {{drink.caffeine}}mg</td>
                    <td>date: {{ drink.date }}</td>
                </tr>
            </tbody>
        </table>
        <form>
            <input 
                name="drink"
                type="text"
                v-model="drinkName"
            />
            <input
                name="caffeine"
                type="number"
                v-model="drinkCaffeine"
                min="0"
                step="0.1"
            />
            <button @click.prevent="addDrink">Submit</button>
        </form>
        <button @click.prevent="currentCaffeine">Update</button>
    </body>
</template>

