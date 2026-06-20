<template>
<div class="p-4 lg:p-6 space-y-4 pb-24 lg:pb-8">

  <!-- Tabs -->
   <div class="grid grid-cols-4 bg-gray-100 rounded-lg p-0.5 select-none">
      <button
        v-for="t in tabs"
        :key="t"
        @click="activeTab=t"
        class="py-1 rounded-lg text-sm font-medium transition cursor-pointer"
        :class="activeTab===t ? 'bg-white shadow' : 'text-gray-500 hover:text-gray-800'"
      >
        {{ t }}
      </button>
    </div>

    <!-- Search + Export -->
<div class="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
      <input
        v-model="search"
        type="text"
        placeholder="Search transactions..."
        class="w-full border rounded-xl px-4 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-gray-300"
      />

      <button
        @click="exportCSV"
        class="flex items-center justify-center gap-2 px-4 py-2 text-sm rounded-xl border hover:bg-gray-100 transition"
      >
        <Download class="w-4 h-4" />
        Export
      </button>
    </div>

    <!-- Custom Dates -->
    <div v-if="activeTab==='custom'" class="flex gap-3">
      <input type="date" v-model="fromDate" class="border p-2 rounded w-full" />
      <input type="date" v-model="toDate" class="border p-2 rounded w-full" />
    </div>

    <!-- Filters -->
    <div class="flex flex-wrap gap-2 items-center">
      <div class="flex bg-gray-100 p-1 rounded-lg">
        <button
          v-for="t in ['all','income','expense']"
          :key="t"
          @click="reportType=t"
          class="px-3 py-1.5 text-xs rounded cursor-pointer"
          :class="reportType===t ? activeTypeClass(t) : 'text-gray-500'"
        >
          {{ t }}
        </button>
      </div>

      <select v-model="selectedCategory" class="border p-2 rounded">
        <option value="all">All Categories</option> 
        <option v-for="c in categories" :key="c.id" :value="c.name">
          {{ c.name }}
        </option>
      </select>
    </div>

    <!-- Empty -->
    <div v-if="groupedTransactions.length===0" class="border p-8 text-center rounded-xl">
      No transactions found
    </div>

    <!-- Transactions -->
    <div v-for="group in groupedTransactions" :key="group.date" class="space-y-2">
      <div class="flex justify-between">
        <div>
          <p class="font-semibold">{{ group.dayLabel }}</p>
          <p class="text-xs text-gray-500">{{ group.fullDate }}</p>
        </div>
        <div class="text-xs flex gap-2">
          <span v-if="group.income>0" class="text-green-600">+₹{{ group.income }}</span>
          <span v-if="group.expense>0" class="text-red-600">-₹{{ group.expense }}</span>
        </div>
      </div>

      <div class="border rounded-xl divide-y">
        <div
          v-for="tx in group.transactions"
          :key="tx.id"
          class="flex items-center gap-3 p-4"
        >
          <div
            class="w-10 h-10 rounded-xl flex items-center justify-center"
            :class="tx.type==='income' ? 'bg-green-100' : 'bg-red-100'"
          >
            <TrendingUp v-if="tx.type==='income'" class="w-5 h-5 text-green-600"/>
            <TrendingDown v-else class="w-5 h-5 text-red-600"/>
          </div>

          <div class="flex-1">
            <p class="font-medium">{{ tx.title }}</p>
            <div class="flex gap-2 mt-1">
              <span class="text-[10px] px-2 py-0 rounded" :class="categoryColor(tx.category)">
                {{ tx.category }}
              </span>
              <span class="text-xs text-gray-500">
                {{ format(tx.date, 'h:mm a') }}
              </span>
            </div>
          </div>

          <p :class="tx.type==='income'?'text-green-600':'text-red-600'" class="font-bold">
            {{ tx.type==='income' ? '+' : '-' }}₹{{ tx.amount }}
          </p>
        </div>
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, computed , onMounted, watch} from 'vue'
import { format, startOfDay, startOfWeek, startOfMonth, endOfMonth, isWithinInterval } from 'date-fns'
import { Download, TrendingUp, TrendingDown } from 'lucide-vue-next'
import {
  fetchExpenses,
  fetchExpenseStats,
  fetchCategories
} from '../api/expenses'  

const tabs = ['today','weekly','monthly','custom']
const activeTab = ref('today')
const reportType = ref('all')
const selectedCategory = ref('all')
const fromDate = ref(null)
const toDate = ref(null)
const search = ref('')

const transactions = ref([])
const categories = ref([])
const stats = ref(null)
const loading = ref(false)


// const categories = [
//   'Food & Drinks','Transport','Entertainment','Shopping',
//   'Bills & Utilities','Salary','Freelance','Investment'
// ]

// const transactions = ref([
//   { id:'1', title:'Salary Deposit', category:'Salary', amount:3200, type:'income', date:new Date() },
//   { id:'2', title:'Netflix', category:'Entertainment', amount:16, type:'expense', date:new Date() },
//   { id:'3', title:'Groceries', category:'Food & Drinks', amount:125, type:'expense', date:new Date(Date.now()-86400000) }
// ])


const name = ref('umar khan')
const msg = computed(() => {
  return `Hello! ${name.value}`
})

console.log(msg.value)

console.log(transactions.value)

const loadExpenses = async () => {
  loading.value = true
console.log(transactions.value)

  try {
    // const params = buildDateParams() 
    const { data } = await fetchExpenses()
    console.log("data", data[0])

    transactions.value = data.map(e => ({
      
      id: e.id,
      title: e.description,
      category: e.category?.name || 'Uncategorized',
      amount: Number(e.amount),
      type: e.expense_type, // 👈 Django field
      date: new Date(e.date)

    }))
  } catch (err) {
    console.error('Expense fetch failed', err)
  } finally {
    loading.value = false
  }
}


const loadCategories = async () => {
  try {
    const { data } = await fetchCategories()
    categories.value = data
  } catch (err) {
    console.error('Category fetch failed', err)
  }
}

const loadStats = async () => {
  try {
    const params = {
      period: activeTab.value === 'today' ? 'daily' : activeTab.value
    }
    const { data } = await fetchExpenseStats(params)
    stats.value = data
  } catch (err) {
    console.error('Stats fetch failed', err)
  }
} 


const buildDateParams = () => {
  const now = new Date()

  if (activeTab.value === 'today') {
    return {
      start_date: format(now, 'yyyy-MM-dd'),
      end_date: format(now, 'yyyy-MM-dd')
    }
  }

  if (activeTab.value === 'weekly') {
    return {
      start_date: format(startOfWeek(now), 'yyyy-MM-dd'),
      end_date: format(now, 'yyyy-MM-dd')
    }
  }

  if (activeTab.value === 'monthly') {
    return {
      start_date: format(startOfMonth(now), 'yyyy-MM-dd'),
      end_date: format(endOfMonth(now), 'yyyy-MM-dd')
    }
  }

  if (activeTab.value === 'custom' && fromDate.value && toDate.value) {
    return {
      start_date: fromDate.value,
      end_date: toDate.value
    }
  }

  return {}
}

const filtered = computed(() => {
  let list = [...transactions.value]
  const now = new Date()

  if (activeTab.value==='today')
    list = list.filter(t => startOfDay(t.date).getTime() === startOfDay(now).getTime())

  if (activeTab.value==='weekly')
    list = list.filter(t => t.date >= startOfWeek(now))

  if (activeTab.value==='monthly')
    list = list.filter(t => t.date >= startOfMonth(now) && t.date <= endOfMonth(now))

  if (activeTab.value==='custom' && fromDate.value && toDate.value)
    list = list.filter(t =>
      isWithinInterval(t.date,{start:new Date(fromDate.value),end:new Date(toDate.value)})
    )

  if (reportType.value!=='all')
    list = list.filter(t => t.type===reportType.value)

  if (selectedCategory.value !== 'all') {
  list = list.filter(t => t.category === selectedCategory.value)
   }


  if (search.value)
    list = list.filter(t =>
      t.title.toLowerCase().includes(search.value.toLowerCase()) ||
      t.category.toLowerCase().includes(search.value.toLowerCase())
    )

  return list.sort((a,b)=>b.date-a.date)
})

const totals = computed(() => {
  const income = filtered.value.filter(t=>t.type==='income').reduce((s,t)=>s+t.amount,0)
  const expense = filtered.value.filter(t=>t.type==='expense').reduce((s,t)=>s+t.amount,0)
  return { income, expense, net: income-expense }
})

const groupedTransactions = computed(() => {
  const map = {}
  filtered.value.forEach(tx=>{
    const key = format(tx.date,'yyyy-MM-dd')
    map[key] ??= []
    map[key].push(tx)
  })

  return Object.entries(map).map(([date, txs])=>{
    const d = new Date(date)
    return {
      date,
      dayLabel: format(d,'EEE'),
      fullDate: format(d,'MMMM d, yyyy'),
      income: txs.filter(t=>t.type==='income').reduce((s,t)=>s+t.amount,0),
      expense: txs.filter(t=>t.type==='expense').reduce((s,t)=>s+t.amount,0),
      transactions: txs
    }
  })
})

const exportCSV = () => {
  const rows = filtered.value.map(t =>
    `${t.title},${t.category},${t.type},${t.amount},${format(t.date,'yyyy-MM-dd')}`
  )
  const blob = new Blob([`Title,Category,Type,Amount,Date\n${rows.join('\n')}`])
  const a = document.createElement('a')
  a.href = URL.createObjectURL(blob)
  a.download = `report-${activeTab.value}.csv`
  a.click()
}

watch(
  [activeTab, fromDate, toDate],
  () => {
    loadExpenses()
    loadStats()
  }
)

onMounted(() => {
  loadExpenses()
  loadCategories()
  loadStats()
})


const normalize = (c) => {
  if (!c) return ''
  if (typeof c === 'string') return c.toLowerCase()
  if (typeof c === 'object' && c.name) return c.name.toLowerCase()
  return ''
}
const activeTypeClass = t =>
  t==='income'?'bg-green-600 text-white':
  t==='expense'?'bg-red-600 text-white':'bg-white shadow'

const categoryColor = c =>
  ({
    'Food & Drinks':'bg-orange-100 text-orange-700',
    'Transport':'bg-blue-100 text-blue-700',
    'Entertainment':'bg-purple-100 text-purple-700',
    'Salary':'bg-green-100 text-green-700'
  }[c] || 'bg-gray-100 text-gray-600')
</script>
