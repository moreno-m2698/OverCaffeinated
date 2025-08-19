<script setup lang="ts">
import { ref } from "vue";

const username = ref("");
const password = ref("");

</script>

<template>
    <form @submit.prevent>
        <h1>login form</h1>
        <input 
            v-model="username"
            type="text"
            id="username"
            name="username"
            required
            placeholder="username" 
        />
        <input 
            v-model="password"
            type="text"
            id="password"
            name="password"
            required
            placeholder="password" 
        />
        <input type="submit"/>
    </form>
</template>