<script setup lang="ts">

type Drink = {
  id: number;
  name: string;
  caffeine: number;
  date: string;
};

defineProps<{
    drinks: Drink[]
}>()

</script>


<template>
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
</template>