import { createRouter, createWebHistory } from 'vue-router';
import Calendar from '../views/Calendar.vue';
import Register from '../views/Register.vue';
import MedicineList from "../components/MedicineList.vue";

const routes = [
    { path: '/', name: 'Home', component: MedicineList },
    { path: '/calendar', name: 'Calendar', component: Calendar },
    { path: '/register', name: 'Register', component: Register },
];

const router = createRouter({
    history: createWebHistory(),
    routes,
});

export default router;
