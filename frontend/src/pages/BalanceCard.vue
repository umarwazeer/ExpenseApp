<template>
  <!-- BACKGROUND SECTION -->
  <div class="relative rounded-b-[40px] px-4 pt-6 pb-24"  style="background-color: #2b5569;">

    <!-- WHITE BALANCE CARD -->
    <div
      class="absolute left-4 right-4 top-5 bg-white rounded-2xl shadow-xl p-5 text-center"
    >
      <!-- CURRENT BALANCE -->
      <div class="text-3xl font-bold text-teal-700">
        {{ formatCurrency(currentBalance) }}
      </div>
      <div class="text-sm text-gray-500 mt-1">
        Current Balance
      </div>

      <!-- STATS -->
      <div class="grid grid-cols-3 gap-2 mt-5">
        <!-- INCOME -->
        <div>
          <div class="text-sm font-semibold text-gray-800">
            {{ formatCurrency(income) }}
          </div>
          <div class="flex items-center justify-center gap-1 text-xs text-green-600 mt-1">
            <q-icon name="add_circle" size="14px" />
            Income
          </div>
        </div>

        <!-- PREVIOUS BALANCE -->
        <div>
          <div class="text-sm font-semibold text-gray-800">
            {{ formatCurrency(previousBalance) }}
          </div>
          <div class="flex items-center justify-center gap-1 text-xs text-blue-600 mt-1">
            <q-icon name="history" size="14px" />
            Pre. Balance
          </div>
        </div>

        <!-- EXPENSE -->
        <div>
          <div class="text-sm font-semibold text-gray-800">
            {{ formatCurrency(expense) }}
          </div>
          <div class="flex items-center justify-center gap-1 text-xs text-red-500 mt-1">
            <q-icon name="remove_circle" size="14px" />
            Expense
          </div>
        </div>
      </div>
    </div>

    <!-- HEADER TITLE -->
    <!-- <div class="text-center text-white text-lg font-semibold">
      Daily Expense Manager
    </div> -->
  </div>
</template>

<script setup>
defineProps({
  currentBalance: {
    type: Number,
    default: 10500
  },
  income: {
    type: Number,
    default: 15000
  },
  previousBalance: {
    type: Number,
    default: 1000
  },
  expense: {
    type: Number,
    default: 5500
  }
})

function formatCurrency (amount) {
  return new Intl.NumberFormat('en-US', {
    minimumFractionDigits: 2
  }).format(amount)
}
</script>

<style scoped>
/* extra smooth shadow like mobile apps */
.shadow-xl {
  box-shadow: 0 15px 30px rgba(0, 0, 0, 0.12);
}
</style>
