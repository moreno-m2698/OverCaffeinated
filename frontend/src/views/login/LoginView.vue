<script setup lang="ts">
import { ref } from "vue";
import { useRouter } from "vue-router"

import axios from "axios";

type User = {
  id: number,
  username: string,
  lastObservation: number,
  caffeine: number
}

const username = ref("");
const password = ref("");
const router = useRouter();

const today = new Date();
today.setUTCHours(0);
today.setUTCMinutes(0);
today.setUTCSeconds(0);
today.setUTCMilliseconds(0);

const mockUser = { // TODO: User is tied to app instance will need to import with props in final
    id: 1,
    username: "janedoe",
    password: "secret",
    lastObservation: today.valueOf(),
    caffeine: 200
}

axios.defaults.withCredentials = true;

async function login() {
    try {
        await axios.post("/login", new URLSearchParams({
            username: username.value,
            password: password.value
        }), {
            headers: { "Content-Type": "application/x-www-form-urlencodded" },
            withCredentials: true
        });

        router.push("/dashboard");
    } catch (err) {
        console.error("Login failed", err);
    }
}

function validateUser() {
    
}

</script>

<template>
    <form @submit.prevent="login">
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