<script setup lang="ts">
import { ref } from "vue";

const name = ref<string>("");
const caffiene = ref<number>(0);

const emit = defineEmits<{
    (e: 'submit', name: string, caffeine: number) : void
}>()

async function emitSubmit() {
    emit('submit', name.value, caffiene.value)
    name.value = ""
    caffiene.value = 0
}

</script>
<template>
    <form @submit.prevent="emitSubmit">
      <input
        name="drink"
        type="text"  
        v-model="name"
        placeholder="Drink name"
        required
      />
      <input
        name="caffeine"
        type="number"
        v-model="caffiene"
        min="0"
        step="0.1"
        required
      />
      <button type="submit">Submit</button>
    </form>
</template>