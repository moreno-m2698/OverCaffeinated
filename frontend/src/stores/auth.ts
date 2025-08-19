import { defineStore } from "pinia";
import { ref } from "vue"
import axios from "axios";

axios.defaults.withCredentials = true;

export const useAuthStore = defineStore('auth', () => {
    
    type User = {
        id: number,
        username: string,
        lastObservation: number,
        caffeine: number
    }

    const user = ref<User|null>(null);
    const loading = ref(true);

    async function fetchUser() {
        if (import.meta.env.MODE === "development") {

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

            user.value = mockUser;
            loading.value = false;

        } else {
            try {
                const res = await axios.get("/users/me");
                user.value = res.data;
            } catch (err) {
                user.value = null;
            } finally {
                loading.value = false;
            }    
        }
        
    }

    async function logout() {
        await axios.post("/logout");
        user.value = null;
    }


    return { user, loading, fetchUser, logout }

})

