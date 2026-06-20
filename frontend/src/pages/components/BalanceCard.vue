<script setup>
import { ref, computed } from 'vue'
import {
  Eye,
  EyeOff,
  ArrowDownLeft,
  ArrowUpRight
} from 'lucide-vue-next'

/**
 * Props definition (JavaScript-safe)
 */
const props = defineProps({
  balance: {
    type: Number,
    required: true
  },
  income: {
    type: Number,
    required: true
  },
  expenses: {
    type: Number,
    required: true
  }
})

const showBalance = ref(true)

const isNegative = computed(() => props.balance < 0)

function formatCurrency(amount) {
  const formatted = Math.abs(amount).toLocaleString('en-US', {
    minimumFractionDigits: 0,
    maximumFractionDigits: 0
  })
  return amount < 0 ? `-$${formatted}` : `$${formatted}`
}
</script>

<template>
  <div
    class="bg-gradient-hero rounded-3xl p-5 text-white shadow-glow animate-fade-in"
  >
    <!-- Total Balance -->
    <div class="mb-5">
      <p class="text-sm font-medium text-white/80 mb-1">
        Total Balance
      </p>

      <div class="flex items-center gap-3">
        <h2
          class="text-4xl font-bold tracking-tight"
          :class="isNegative ? 'text-red-200' : ''"
        >
          {{ showBalance ? formatCurrency(balance) : '••••••' }}
        </h2>

        <button
          @click="showBalance = !showBalance"
          class="p-2 rounded-full bg-white/10 hover:bg-white/20 transition"
        >
          <Eye v-if="showBalance" class="w-5 h-5" />
          <EyeOff v-else class="w-5 h-5" />
        </button>
      </div>
    </div>

    <!-- Income & Expenses -->
    <div class="grid grid-cols-2 gap-3">
      <!-- Income -->
      <div class="glass-effect rounded-2xl p-4">
        <div class="flex items-center gap-2 mb-2">
          <div
            class="w-6 h-6 rounded-full bg-green-500/20 flex items-center justify-center"
          >
            <ArrowDownLeft class="w-4 h-4 text-green-300" />
          </div>
          <span class="text-sm font-medium text-white/80">
            Income
          </span>
        </div>

        <p class="text-xl font-bold text-green-300">
          {{ formatCurrency(income) }}
        </p>
      </div>

      <!-- Expenses -->
      <div class="glass-effect rounded-2xl p-4">
        <div class="flex items-center gap-2 mb-2">
          <div
            class="w-6 h-6 rounded-full bg-red-500/20 flex items-center justify-center"
          >
            <ArrowUpRight class="w-4 h-4 text-red-300" />
          </div>
          <span class="text-sm font-medium text-white/80">
            Expenses
          </span>
        </div>

        <p class="text-xl font-bold text-red-300">
          {{ formatCurrency(expenses) }}
        </p>
      </div>
    </div>
  </div>
</template>
