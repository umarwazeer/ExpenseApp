<template>
  <div class="w-full min-h-screen bg-gray-50 pb-20">

    <!-- HEADER -->
    <div class="px-4 pt-4">
      <h1 class="text-xl font-bold text-gray-900">My Budget</h1>
      <p class="text-sm text-gray-500">Manage your monthly spending limits</p>

      <button
        class="mt-4 w-full flex items-center justify-center gap-2 rounded-lg bg-blue-600 py-3 text-white font-medium active:scale-95"
        @click="openAdd = true"
      >
        + Add Budget
      </button>
    </div>

    <!-- STATS -->
    <section class="grid grid-cols-2 sm:grid-cols-4 gap-3">
        <SummaryCard title="Total Budget" :value="totalBudget" />
        <SummaryCard title="Total Spent" :value="totalSpent" />
        <SummaryCard title="On Track" :text="onTrackCount + ' categories'" :currency="false" />
        <SummaryCard title="Over Budget" :text="overBudgetCount + ' categories'" :currency="false" />
      </section>

    <!-- OVERALL PROGRESS -->
    <div class="px-4 mt-6">
      <div class="rounded-xl bg-white p-4 shadow-sm">
        <div class="flex justify-between text-sm font-medium mb-2">
          <span>Overall Budget</span>
          <span>{{ usedPercent }}% used</span>
        </div>
        <div class="h-3 w-full rounded-full bg-gray-200 overflow-hidden">
          <div
            class="h-full bg-blue-600 transition-all"
            :style="{ width: usedPercent + '%' }"
          ></div>
        </div>
      </div>
    </div>

    <!-- CATEGORY LIST -->
    <div class="px-4 mt-8">
      <h2 class="mb-4 text-base font-semibold text-gray-800">
        Category Budgets
      </h2>

      <div class="space-y-4">
        <div
          v-for="b in budgets"
          :key="b.id"
          class="flex items-center gap-4 rounded-xl bg-white p-4 shadow-sm"
        >
          <!-- ICON -->
          <div class="flex h-12 w-12 items-center justify-center rounded-full bg-orange-500 text-white text-lg">
            🍽️
          </div>

          <!-- INFO -->
          <div class="flex-1">
            <div class="flex justify-between items-center">
              <h3 class="font-medium text-gray-900">{{ b.category }}</h3>
              <div class="text-sm">
                <button class="text-blue-600 mr-2" @click="editBudget(b)">
                  Edit
                </button>
                <button class="text-red-500" @click="removeBudget(b.id)">
                  Delete
                </button>
              </div>
            </div>

            <p class="text-xs text-gray-500">
              Limit: ₹{{ b.limit }}
            </p>

            <div class="mt-2 h-2 w-full rounded-full bg-gray-200 overflow-hidden">
              <div
                class="h-full bg-green-500"
                :style="{ width: budgetPercent(b) + '%' }"
              ></div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- ADD / EDIT MODAL -->
    <div
      v-if="openAdd || editing"
      class="fixed inset-0 z-50 flex items-end bg-black/40"
    >
      <div class="w-full rounded-t-xl bg-white p-4">
        <h3 class="text-lg font-semibold mb-4">
          {{ editing ? 'Edit Budget' : 'Add Budget' }}
        </h3>

        <input
          v-model="form.category"
          placeholder="Category"
          class="mb-3 w-full rounded-md border px-3 py-2 text-sm"
        />

        <input
          v-model.number="form.limit"
          type="number"
          placeholder="Monthly Limit"
          class="mb-4 w-full rounded-md border px-3 py-2 text-sm"
        />

        <div class="flex gap-3">
          <button
            class="flex-1 rounded-md bg-gray-200 py-2"
            @click="closeModal"
          >
            Cancel
          </button>
          <button
            class="flex-1 rounded-md bg-blue-600 py-2 text-white"
            @click="saveBudget"
          >
            Save
          </button>
        </div>
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

const budgets = ref([
  { id: 1, category: 'Food & Drinks', limit: 5000, spent: 3500 }
])

const openAdd = ref(false)
const editing = ref(false)
const editingId = ref(null)

const form = ref({
  category: '',
  limit: 0
})

const totalBudget = computed(() =>
  budgets.value.reduce((s, b) => s + b.limit, 0)
)

const totalSpent = computed(() =>
  budgets.value.reduce((s, b) => s + b.spent, 0)
)

const usedPercent = computed(() =>
  totalBudget.value
    ? Math.round((totalSpent.value / totalBudget.value) * 100)
    : 0
)

const onTrack = computed(() =>
  budgets.value.filter(b => b.spent <= b.limit).length
)

const overBudget = computed(() =>
  budgets.value.filter(b => b.spent > b.limit).length
)

const budgetPercent = b =>
  Math.min(100, Math.round((b.spent / b.limit) * 100))

function saveBudget() {
  if (editing.value) {
    const b = budgets.value.find(x => x.id === editingId.value)
    b.category = form.value.category
    b.limit = form.value.limit
  } else {
    budgets.value.push({
      id: Date.now(),
      category: form.value.category,
      limit: form.value.limit,
      spent: 0
    })
  }
  closeModal()
}

function editBudget(b) {
  editing.value = true
  editingId.value = b.id
  form.value = { category: b.category, limit: b.limit }
}

function removeBudget(id) {
  budgets.value = budgets.value.filter(b => b.id !== id)
}

function closeModal() {
  openAdd.value = false
  editing.value = false
  editingId.value = null
  form.value = { category: '', limit: 0 }
}
</script>
