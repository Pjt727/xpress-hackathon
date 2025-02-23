import { createRouter, createWebHistory } from "vue-router";
import Login from "@/components/Login.vue";
import Register from "@/components/Register.vue";
import Invoice from "@/components/Invoice.vue";
import History from "@/components/History.vue";
import Group from "@/components/Group.vue";

const routes = [
  { path: "/", redirect: "/login" },
  { path: "/login", component: Login },
  { path: "/register", component: Register },
  { path: "/invoice", component: Invoice },
  { path: "/history", component: History },
  { path: "/group", component: Group },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
