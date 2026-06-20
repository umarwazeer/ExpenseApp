<template>
  <q-layout view="lHh Lpr lFf" class="bg-gray-50 font-sans">

    <!-- ================= SIDEBAR OVERLAY (MOBILE) ================= -->
    <transition name="fade">
      <div
        v-if="mobileSidebarOpen"
        class="fixed inset-0 bg-black/30 backdrop-blur-sm z-40 lg:hidden"
        @click="mobileSidebarOpen = false"
      />
    </transition>

    <!-- ================= SIDEBAR ================= -->
    <aside
      class="fixed top-0 left-0 z-50 h-full w-64 bg-white border-r border-gray-200
             transform transition-transform duration-300
             lg:translate-x-0 lg:static"
      :class="mobileSidebarOpen ? 'translate-x-0' : '-translate-x-full lg:translate-x-0'"
    >
      <q-scroll-area class="fit">

        <!-- Sidebar Header -->
        <div class="flex items-center justify-between p-4 border-b border-gray-100">
          <div class="flex items-center gap-3">
            <div class="w-10 h-10 rounded-xl bg-gradient-to-br from-purple-600 to-indigo-500 flex items-center justify-center shadow-lg">
              <TrendingUp class="w-5 h-5 text-white" />
            </div>
            <div>
              <div class="text-lg font-bold text-gray-900">DailyKhata</div>
              <div class="text-[11px] text-gray-400">Expense Manager</div>
            </div>
          </div>

          <button class="lg:hidden" @click="mobileSidebarOpen = false">
            <X class="w-5 h-5 text-gray-500" />
          </button>
        </div>

        <!-- Menu -->
        <nav class="p-3">
          <p class="text-xs font-semibold text-gray-400 uppercase tracking-wider px-3 mb-2">
            Main Menu
          </p>

          <router-link
            v-for="link in menuLinks"
            :key="link.title"
            :to="link.to"
            @click="mobileSidebarOpen = false"
            class="flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium mb-1 transition-all"
            :class="isActive(link.to)
              ? 'bg-teal-50 text-teal-700 border-r-4 border-teal-600'
              : 'text-gray-600 hover:bg-gray-50'"
          >
            <component :is="link.icon" class="w-5 h-5" />
            {{ link.title }}
            <span
              v-if="link.title === 'AI Assistant'"
              class="ml-auto text-[10px] px-2 py-0.5 rounded-full bg-purple-100 text-purple-600 font-semibold"
            >
              AI
            </span>
          </router-link>

          <q-separator class="my-4" />

          <p class="text-xs font-semibold text-gray-400 uppercase tracking-wider px-3 mb-2">
            System
          </p>

          <router-link
            to="/setting"
            class="flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium text-gray-600 hover:bg-gray-50"
          >
            <Settings class="w-5 h-5" />
            Settings
          </router-link>

          <button
            @click="showLogoutDialog = true"
            class="w-full flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium text-red-600 hover:bg-red-50"
          >
            <LogOut class="w-5 h-5" />
            Logout
          </button>
        </nav>

      </q-scroll-area>
    </aside>

    <!-- ================= HEADER ================= -->
   <header class="sticky top-0 z-30 bg-gradient-to-r from-teal-700 to-teal-600">
      <div class="flex items-center justify-between h-14 px-4 text-white">

        <div class="flex items-center gap-3">
          <button
            class="lg:hidden p-2 rounded-md hover:bg-white/10"
            @click="mobileSidebarOpen = true"
          >
            <Menu class="w-5 h-5" />
          </button>

          <div>
            <div class="text-lg font-bold">DailyKhata     </div>
            <div class="text-[10px] opacity-80 hidden sm:block">
              {{ today }}
            </div>
          </div>
        </div>

        <div class="flex items-center gap-1">
          <button class="relative p-2 rounded-md hover:bg-white/10">
            <Bell class="w-5 h-5" />
            <span class="absolute top-2 right-2 w-2 h-2 bg-red-400 rounded-full"></span>
          </button>

          <button class="p-2 rounded-md hover:bg-white/10">
            <Moon class="w-5 h-5" />
          </button>
        </div>

      </div>
    </header>

    <!-- ================= PAGE CONTENT ================= -->
    <q-page-container class="bg-gray-50">
      <router-view class="h-full flex flex-col" />
    </q-page-container>

    <!-- ================= BOTTOM NAV (MOBILE) ================= -->
    <nav class="fixed bottom-0 left-0 right-0 z-30 bg-white/95 backdrop-blur border-t lg:hidden">
      <div class="flex items-center justify-around h-16">

        <router-link
          v-for="item in bottomNav"
          :key="item.label"
          :to="item.to"
          class="flex flex-col items-center gap-1 flex-1 py-2 transition"
          :class="isActive(item.to) ? 'text-teal-600' : 'text-gray-400'"
        >
          <div class="p-1.5 rounded-xl" :class="isActive(item.to) && 'bg-teal-100'">
            <component :is="item.icon" class="w-5 h-5" />
          </div>
          <span class="text-[10px] font-medium">{{ item.label }}</span>
        </router-link>

      </div>
    </nav>

    <!-- ================= LOGOUT DIALOG ================= -->
    <q-dialog v-model="showLogoutDialog">
      <q-card class="rounded-2xl p-4 w-[320px]">
        <q-card-section class="text-center">
          <div class="w-14 h-14 bg-red-50 rounded-full flex items-center justify-center mx-auto mb-3">
            <LogOut class="w-7 h-7 text-red-500" />
          </div>
          <div class="text-lg font-bold">Log out?</div>
          <div class="text-sm text-gray-500 mt-1">
            Are you sure you want to sign out?
          </div>
        </q-card-section>

        <q-card-actions align="center" class="gap-3">
          <q-btn flat label="Cancel" v-close-popup class="bg-gray-100 rounded-lg" />
          <q-btn flat label="Logout" class="bg-red-600 text-white rounded-lg" @click="handleLogout" />
        </q-card-actions>
      </q-card>
    </q-dialog>

  </q-layout>
</template>

<script setup>
import { ref } from "vue";
import { useRoute, useRouter } from "vue-router";
import { useQuasar } from "quasar";
import { useAuthStore } from "src/stores/auth";

import {
  Menu,
  Bell,
  Moon,
  TrendingUp,
  LayoutGrid,
  Receipt,
  BarChart3,
  PieChart,
  Wallet,
  Settings,
  LogOut,
  X,
  Home,
  User,
  Bot,

} from "lucide-vue-next";

const route = useRoute();
const router = useRouter();
const auth = useAuthStore();
const $q = useQuasar();

const mobileSidebarOpen = ref(false);
const showLogoutDialog = ref(false);

const today = new Date().toLocaleDateString("en-US", {
  weekday: "short",
  month: "short",
  day: "numeric",
});

const menuLinks = [
  { title: "Dashboard", to: "/", icon: LayoutGrid },
  { title: "Transactions", to: "/transactions", icon: Receipt },
  { title: "Reports", to: "/report", icon: BarChart3 },
  { title: "Analytics", to: "/stats", icon: PieChart },
  { title: "My Budget", to: "/budget", icon: Wallet },
  { title: "AI Assistant", to: "/ai-chat", icon: Bot },
];

const bottomNav = [
  { label: "Home", to: "/", icon: Home },
  { label: "Stats", to: "/stats", icon: BarChart3 },
  // { label: "AI", to: "/ai-chat", icon: Bot }, // 🤖
  { label: "Report", to: "/report", icon: Receipt },
  { label: "Profile", to: "/setting", icon: User },
];

const isActive = (path) => route.path === path;

const handleLogout = async () => {
  showLogoutDialog.value = false;
  await auth.logout();
  $q.notify({ type: "positive", message: "Logged out successfully" });
  router.push("/auth/login");
};
</script>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s ease;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
