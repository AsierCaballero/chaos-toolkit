import { createApp } from "vue";
import { createPinia } from "pinia";
import { createRouter, createWebHistory } from "vue-router";
import App from "./App.vue";
import Experiments from "./views/Experiments.vue";
import ExperimentDetail from "./views/ExperimentDetail.vue";
import Dashboard from "./views/Dashboard.vue";

const routes = [
  { path: "/", component: Dashboard },
  { path: "/experiments", component: Experiments },
  { path: "/experiments/:name", component: ExperimentDetail },
];

const router = createRouter({ history: createWebHistory(), routes });
const pinia = createPinia();

createApp(App).use(pinia).use(router).mount("#app");
