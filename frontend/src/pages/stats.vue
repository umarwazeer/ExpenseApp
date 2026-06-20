<template>
  <div class="p-4 lg:p-6 space-y-6 pb-24">

    <!-- HEADER -->
    <div class="flex items-center justify-between">
      <div>
        <h1 class="text-xl font-bold">Analytics</h1>
        <p class="text-sm text-gray-500">Your spending insights</p>
      </div>

      <select v-model="timeRange" class="border rounded-lg px-3 py-1 text-sm">
        <option value="week">This Week</option>
        <option value="month">This Month</option>
        <option value="year">This Year</option>
      </select>
    </div>

    <!-- STATS -->
    <div class="grid grid-cols-2 lg:grid-cols-4 gap-3">
      <div class="card">
        <Wallet class="icon" />
        <p class="label">Balance</p>
        <p class="value">₹{{ balance.toLocaleString() }}</p>
      </div>

      <div class="card">
        <TrendingUp class="icon" />
        <p class="label">Income</p>
        <p class="value">₹{{ totalIncome.toLocaleString() }}</p>
      </div>

      <div class="card">
        <TrendingDown class="icon" />
        <p class="label">Expense</p>
        <p class="value">₹{{ totalExpense.toLocaleString() }}</p>
      </div>

      <div class="card">
        <Target class="icon" />
        <p class="label">Savings</p>
        <p class="value">{{ savingsRate }}%</p>
      </div>
    </div>

    <!-- TABS -->
    <div class="grid grid-cols-3 bg-gray-100 rounded-xl p-1">
      <button
        v-for="t in ['overview','categories','trends']"
        :key="t"
        @click="activeTab = t"
        class="py-2 rounded-lg text-sm capitalize"
        :class="activeTab === t ? 'bg-white font-semibold' : 'text-gray-600'"
      >
        {{ t }}
      </button>
    </div>

    <!-- OVERVIEW -->
    <div v-if="activeTab === 'overview'" class="card h-[260px]">
      <Bar :data="barChartData" />
    </div>

    <!-- CATEGORIES -->
    <div v-if="activeTab === 'categories'" class="card h-[260px]">
      <Pie :data="pieChartData" />
    </div>

    <!-- TRENDS -->
    <div v-if="activeTab === 'trends'" class="card h-[260px]">
      <Line :data="lineChartData" />
    </div>

  </div>
</template>

<script setup>
import { ref, computed } from "vue";
import { format, subDays, subMonths } from "date-fns";

/* ICONS */
import { TrendingUp, TrendingDown, Wallet, Target } from "lucide-vue-next";

/* CHARTS */
import { Bar, Line, Pie } from "vue-chartjs";
import {
  Chart as ChartJS,
  BarElement,
  LineElement,
  ArcElement,
  CategoryScale,
  LinearScale,
  PointElement,
  Tooltip,
  Legend,
} from "chart.js";

ChartJS.register(
  BarElement,
  LineElement,
  ArcElement,
  CategoryScale,
  LinearScale,
  PointElement,
  Tooltip,
  Legend
);

/* STATE */
const timeRange = ref("month");
const activeTab = ref("overview");

/* BASE DATA */
const weeklyExpenses = [320, 180, 450, 220, 380, 290, 410];
const monthlyExpenses = [1200, 1800, 1500, 2000];
const yearlyExpenses = [15000, 17000, 14000, 19000, 21000, 18000];

const incomeMap = {
  week: 4200,
  month: 12000,
  year: 150000,
};

/* FILTERED DATA */
const expenseData = computed(() => {
  if (timeRange.value === "week") return weeklyExpenses;
  if (timeRange.value === "month") return monthlyExpenses;
  return yearlyExpenses;
});

const labels = computed(() => {
  if (timeRange.value === "week") {
    return Array.from({ length: 7 }, (_, i) =>
      format(subDays(new Date(), 6 - i), "EEE")
    );
  }
  if (timeRange.value === "month") {
    return ["Week 1", "Week 2", "Week 3", "Week 4"];
  }
  return ["Jan", "Feb", "Mar", "Apr", "May", "Jun"];
});

/* STATS */
const totalExpense = computed(() =>
  expenseData.value.reduce((a, b) => a + b, 0)
);

const totalIncome = computed(() => incomeMap[timeRange.value]);

const balance = computed(() => totalIncome.value - totalExpense.value);

const savingsRate = computed(() =>
  totalIncome.value
    ? Math.round((balance.value / totalIncome.value) * 100)
    : 0
);

/* CHART DATA */
const barChartData = computed(() => ({
  labels: labels.value,
  datasets: [
    {
      label: "Expenses",
      data: expenseData.value,
      backgroundColor: "#3b82f6",
      borderRadius: 6,
    },
  ],
}));

const pieChartData = computed(() => ({
  labels: ["Food", "Transport", "Shopping", "Entertainment"],
  datasets: [
    {
      data: [
        totalExpense.value * 0.4,
        totalExpense.value * 0.2,
        totalExpense.value * 0.25,
        totalExpense.value * 0.15,
      ],
      backgroundColor: ["#f97316", "#3b82f6", "#ec4899", "#a855f7"],
    },
  ],
}));

const lineChartData = computed(() => ({
  labels: labels.value,
  datasets: [
    {
      label: "Expense Trend",
      data: expenseData.value,
      borderColor: "#ef4444",
      tension: 0.4,
    },
  ],
}));
</script>

<style scoped>
.card {
  border: 1px solid #e5e7eb;
  border-radius: 12px;
  padding: 12px;
  background: white;
}

.icon {
  width: 20px;
  height: 20px;
  margin-bottom: 4px;
}

.label {
  font-size: 12px;
  color: #6b7280;
}

.value {
  font-size: 16px;
  font-weight: 600;
}
</style>
