<template>
  <q-page class="bg-grey-2">

    <!-- HEADER / BALANCE -->
       <BalanceCard
      :currentBalance="10500"
      :income="15000"
      :previousBalance="1000"
      :expense="5500"
    />


    <!-- MAIN CONTENT -->
    <main class="q-pa-md" style="margin-top: 50px;">
      <!-- Quick actions -->
      <!-- <div class="row q-col-gutter-sm q-mb-md q-mt-md">
        <div v-for="action in quickActions" :key="action.name" class="col-3">
          <q-card flat class="action-btn bg-white rounded-xl q-pa-sm card-shadow cursor-pointer text-center" @click="onActionClick(action)">
            <div class="column items-center">
              <div class="action-icon-bg q-mb-xs" :style="{ background: action.bgColor }">
                <q-icon :name="action.icon" color="white" size="20px" />
              </div>
              <div class="text-caption text-grey-8 text-weight-medium">{{ action.name }}</div>
            </div>
          </q-card>
        </div>
      </div> -->

      <!-- Filters card -->
      <q-card class="bg-white rounded-xl q-mt-md q-pa-sm q-mb-sm card-shadow">
        <div class="row items-center q-gutter-xs q-mb-xs">
          <q-chip v-for="f in filters" :key="f.value" clickable :color="activeFilter === f.value ? 'indigo-5' : 'grey-3'"
                  :text-color="activeFilter === f.value ? 'white' : 'grey-8'" size="sm" @click="setFilter(f.value)">
            {{ f.label }}
          </q-chip>
          <q-space />
          <q-btn flat dense round icon="tune" size="sm" @click="showAdvancedFilters = !showAdvancedFilters" />
        </div>

        <q-slide-transition>
          <div v-show="showAdvancedFilters" class="q-pt-sm">
            <div class="row q-col-gutter-xs">
              <div class="col-5">
                <q-input dense outlined v-model="searchText" placeholder="Search..." clearable>
                  <template #prepend><q-icon name="search" /></template>
                </q-input>
              </div>
              <div class="col-3">
                <q-select dense outlined v-model="filterType" :options="typeOptions" emit-value map-options />
              </div>
              <div class="col-4">
                <q-select dense outlined v-model="filterCategory" :options="filterCategoryOptions" emit-value map-options />
              </div>
            </div>
          </div>
        </q-slide-transition>
      </q-card>

      <!-- Recent Transactions -->
      <div class="row items-center justify-between q-mb-xs q-mt-sm">
        <div class="text-subtitle2 text-weight-bold">Recent Transactions</div>
        <q-btn flat dense color="indigo" label="View All" size="sm" @click="$router.push({ name: 'report' })" />
      </div>

      <div class="q-mb-xl" id="transactionsContainer">
        <q-card v-for="group in fullyFilteredGroups" :key="group.date" class="date-group bg-white rounded-xl q-mb-sm card-shadow overflow-hidden">
          <div class="row items-center justify-between q-pa-md cursor-pointer" @click="toggleGroup(group.date)">
            <div class="row items-center">
              <q-avatar :color="group.isToday ? 'indigo-6' : 'grey-4'" text-color="white" size="40px" class="q-mr-sm">
                <span class="text-body2 text-weight-bold">{{ group.dateNumber }}</span>
              </q-avatar>
              <div>
                <div class="text-body2 text-weight-medium">{{ group.displayDate }}</div>
                <div class="text-caption text-grey-6">{{ group.dayName }}</div>
              </div>
            </div>

            <div class="row items-center q-gutter-xs">
              <div class="text-right">
                <div class="text-positive text-weight-medium text-caption">+{{ formatCurrency(group.dailyIncome) }}</div>
                <div class="text-negative text-weight-medium text-caption">-{{ formatCurrency(group.dailyExpense) }}</div>
              </div>
              <q-icon name="expand_more" class="expand-icon text-grey-5" :class="{ 'rotate-180': expandedGroups.includes(group.date) }" />
            </div>
          </div>

          <q-slide-transition>
            <div v-show="expandedGroups.includes(group.date)">
              <q-separator />
              <div>
                <!-- CLICKING HERE OPENS DETAIL DIALOG -->
                <q-item v-for="(tx, index) in groupFilteredTransactions(group.transactions)" :key="tx.id || index" clickable v-ripple class="q-py-sm" @click="openTransactionDetail(tx)">
                  <q-item-section avatar>
                    <q-avatar :color="getCategoryColor(tx.category) + '-1'" size="36px">
                      <q-icon :name="getCategoryIcon(tx.category)" :color="getCategoryColor(tx.category)" size="18px" />
                    </q-avatar>
                  </q-item-section>

                  <q-item-section>
                    <q-item-label class="text-body2 text-weight-medium">{{ tx.remarks || tx.description }}</q-item-label>
                    <q-item-label caption class="row items-center q-gutter-xs">
                      <q-badge :color="getCategoryColor(tx.category)" :label="getCategoryLabel(tx.category)" dense class="text-white" />
                      <span>{{ tx.paymentMethod }}</span>
                      <span v-if="tx.invoiceName" class="q-ml-sm text-caption text-grey-6">• Invoice</span>
                    </q-item-label>
                  </q-item-section>

                  <q-item-section side>
                    <q-item-label class="text-body2 text-weight-bold" :class="tx.type === 'income' ? 'text-positive' : 'text-negative'">
                      {{ tx.type === 'income' ? '+' : '-' }}{{ formatCurrency(tx.amount) }}
                    </q-item-label>
                  </q-item-section>
                </q-item>

                <div v-if="!groupFilteredTransactions(group.transactions).length" class="q-pa-md text-caption text-grey-5 text-center">No transactions match your filters</div>
              </div>
            </div>
          </q-slide-transition>
        </q-card>

        <div v-if="!fullyFilteredGroups.length" class="q-pa-lg text-center">
          <q-icon name="receipt_long" size="48px" color="grey-4" />
          <div class="text-body2 text-grey-6 q-mt-sm">No transactions found</div>
          <q-btn flat color="indigo" label="Add your first transaction" class="q-mt-sm" @click="openManualFromFab" />
        </div>
      </div>
    </main>

    <!-- FAB (opens choice dialog) -->
    <q-page-sticky position="bottom-right" :offset="[18, 80]">
      <q-btn fab color="indigo" icon="add" class="floating-btn" @click="showChoiceDialog = true" />
    </q-page-sticky>

    <!-- CHOICE DIALOG: Manual or Scan -->
    <q-dialog v-model="showChoiceDialog">
      <q-card class="rounded-lg q-pa-md" style="min-width: 300px">
        <div class="text-h6 q-mb-md">Add Transaction</div>
        <div class="row q-col-md q-gutter-x-md">
          <q-btn class="col" color="indigo" label="Manual" icon="edit" @click="openManualFromFab" />
          <q-btn class="col" color="green" label="Scan" icon="camera_alt" @click="openScanChoice" />
        </div>
        <div class="q-mt-md row justify-end">
          <q-btn flat label="Close" v-close-popup />
        </div>
      </q-card>
    </q-dialog>

    <!-- ADD TRANSACTION DIALOG (Manual form) -->
    <q-dialog v-model="showAddModal" v-close-popup position="bottom" persistent>
     <AddTransactionForm
        @saved="reloadTransactions"
        @close="showAddModal = false"
      />
    </q-dialog>

    <!-- SCAN CHOICE DIALOG (camera or upload) -->
    <q-dialog v-model="showScanChoiceDialog">
      <q-card class="rounded-lg q-pa-md" style="min-width: 320px">
        <div class="text-h6 q-mb-md">Scan Invoice</div>
        <div class="row q-col-md q-gutter-x-md">
          <q-btn class="col" color="primary" label="Scan with Camera" icon="photo_camera" @click="openCameraScan" />
          <q-btn class="col" color="secondary" label="Upload & Scan" icon="upload" @click="openUploadScan" />
        </div>
        <div class="q-mt-md row justify-end">
          <q-btn flat label="Close" v-close-popup />
        </div>
      </q-card>
    </q-dialog>

    <!-- SCAN DIALOG (preview + OCR result) -->
    <q-dialog v-model="showScanModal" persistent>
      <q-card class="rounded-lg q-pa-md" style="min-width: 320px; max-width: 720px;">
        <div class="text-h6 q-mb-sm">Scan Receipt</div>
        <div class="text-caption text-grey-7 q-mb-md">Take a photo or upload a receipt. We’ll extract total, category and remarks. Review before saving.</div>

        <div v-if="scanPreview && !isPdf" class="q-mb-md">
          <q-img :src="scanPreview" ratio="16/9" spinner-color="indigo" class="rounded-borders" />
        </div>
        <div v-if="isPdf" class="q-mb-md">
          <q-icon name="picture_as_pdf" size="36px" color="primary" />
          <div class="text-caption q-mt-xs">{{ scanFile?.name }}</div>
        </div>

        <div v-if="scanning" class="q-mt-sm">
          <q-linear-progress indeterminate color="teal" />
          <div class="text-caption text-grey-7 q-mt-xs">Scanning with AI…</div>
        </div>
        <div v-if="scanError" class="text-negative text-caption q-mt-sm">{{ scanError }}</div>

        <div v-if="scanResult" class="q-mt-md q-pa-sm bg-grey-1 rounded-borders">
          <div class="text-caption text-grey-7 q-mb-xs">Parsed</div>
          <div class="row items-center justify-between">
            <div class="text-body2">Amount</div>
            <div class="text-body2 text-weight-bold">{{ scanResult.amount ? formatCurrency(scanResult.amount) : '—' }}</div>
          </div>
          <div class="row items-center justify-between">
            <div class="text-body2">Category</div>
            <div class="text-body2">{{ getCategoryLabel(scanResult.category) || '—' }}</div>
          </div>
          <div class="row items-center justify-between">
            <div class="text-body2">Date</div>
            <div class="text-body2">{{ scanResult.date || '—' }}</div>
          </div>
          <div class="row items-center justify-between">
            <div class="text-body2">Invoice #</div>
            <div class="text-body2">{{ scanResult.invoiceNumber || '—' }}</div>
          </div>
          <div class="text-caption text-grey-6 q-mt-xs">Remarks: {{ scanResult.remarks || '—' }}</div>
        </div>

        <div class="row q-mt-md justify-between">
          <div>
            <q-btn flat label="Cancel" v-close-popup />
          </div>
          <div class="row q-gutter-sm">
            <q-btn outline color="primary" label="Retake/Choose" @click="retakeScan" />
            <q-btn color="indigo" label="Review & Save" :disable="!scanReady" @click="useScanResult" />
          </div>
        </div>
      </q-card>
    </q-dialog>

    <!-- Hidden global inputs for camera/upload -->
    <input ref="cameraInputRef" type="file" accept="image/*" capture="environment" class="hidden" @change="onCameraCaptured" />
    <input ref="uploadInputRef" type="file" accept="image/*,application/pdf" class="hidden" @change="onUploadSelected" />

    <!-- ================================================== -->
    <!-- NEW: TRANSACTION DETAIL DIALOG -->
    <!-- ================================================== -->
    <q-dialog v-model="showDetailDialog" maximized>
      <q-card class="detail-card-root bg-white">
        <!-- Header -->
        <div class="row items-center justify-between detail-header q-pa-sm q-pl-md q-pr-md">
          <q-btn flat round dense icon="arrow_back" @click="showDetailDialog = false" />
          <div class="text-subtitle1 text-weight-bold">Transaction Details</div>
          <q-btn flat round dense icon="delete" color="negative" @click="deleteTransactionConfirm" />
        </div>

        <q-separator />

        <q-card-section class="q-pt-md">
          <div class="detail-outer">
            <!-- Top: icon, chip, amount -->
            <div class="column items-center q-mb-lg">
              <q-avatar size="72px" :color="getCategoryColor(selectedTransaction?.category) + '-1'">
                <q-icon :name="getCategoryIcon(selectedTransaction?.category)" :color="getCategoryColor(selectedTransaction?.category)" size="36px" />
              </q-avatar>

              <q-chip
                square
                dense
                :color="selectedTransaction?.type === 'expense' ? 'red-6' : 'green-6'"
                text-color="white"
                class="q-mt-md"
              >
                {{ selectedTransaction?.type === 'expense' ? 'Expense' : 'Income' }}
              </q-chip>

              <div class="text-h4 text-weight-bold q-mt-sm">
                {{ formatCurrency(selectedTransaction?.amount || 0) }}
              </div>
            </div>

            <!-- Details List -->
            <div class="q-pa-sm">
              <div class="row justify-between q-py-sm detail-row">
                <div class="detail-label">Category</div>
                <div class="detail-value">{{ getCategoryLabel(selectedTransaction?.category) }}</div>
              </div>
              
              <q-separator class="q-my-xs" />

              <div class="row justify-between q-py-sm detail-row">
                <div class="detail-label">Date</div>
                <div class="detail-value">{{ selectedTransaction?.date }}</div>
              </div>

              <q-separator class="q-my-xs" />

              <div class="row justify-between q-py-sm detail-row">
                <div class="detail-label">Payment Method</div>
                <div class="detail-value">{{ selectedTransaction?.paymentMethod }}</div>
              </div>

              <q-separator class="q-my-xs" />

              <div class="row justify-between q-py-sm detail-row">
                <div class="detail-label">Remarks</div>
                <div class="detail-value text-right" style="max-width: 60%;">{{ selectedTransaction?.remarks || '—' }}</div>
              </div>

              <!-- Invoice Section -->
              <div v-if="selectedTransaction?.invoiceBase64" class="q-mt-lg">
                <q-separator class="q-mb-md" />
                <div class="text-subtitle2 text-grey-7 q-mb-sm">Attached Invoice</div>
                <q-card flat bordered class="q-pa-sm cursor-pointer bg-grey-1" @click="viewInvoice(selectedTransaction)">
                  <div class="row items-center">
                    <q-icon name="receipt" size="24px" color="primary" class="q-mr-sm" />
                    <div class="text-body2 ellipsis col">{{ selectedTransaction.invoiceName || 'View Invoice' }}</div>
                    <q-icon name="chevron_right" color="grey-5" />
                  </div>
                </q-card>
              </div>
            </div>
          </div>
        </q-card-section>
      </q-card>
    </q-dialog>

    <!-- NEW: INVOICE VIEWER DIALOG -->
    <q-dialog v-model="showInvoiceViewer" maximized>
      <q-card style="background: #000;">
        <q-bar class="bg-white text-black">
          <div class="text-weight-bold">Invoice Viewer</div>
          <q-space />
          <q-btn dense flat icon="close" v-close-popup />
          <q-btn dense flat icon="download" @click="downloadCurrentInvoice" />
        </q-bar>
        
        <q-card-section class="full-height q-pa-none" style="height: calc(100vh - 32px); overflow: auto; display: flex; justify-content: center; align-items: center; background: #222;">
          <div v-if="isInvoicePdf(invoiceViewerSrc)" class="text-center text-white">
            <q-icon name="picture_as_pdf" size="80px" color="primary" />
            <div class="q-mt-md">Preview not available for PDF</div>
            <q-btn color="primary" label="Download PDF" class="q-mt-md" @click="downloadCurrentInvoice" />
          </div>
          <img v-else :src="invoiceViewerSrc" alt="Invoice" style="max-width: 100%; max-height: 100%; object-fit: contain;" />
        </q-card-section>
      </q-card>
    </q-dialog>

    <!-- BOTTOM NAV -->
    <!-- <q-footer elevated class="bg-white">
      <div class="row justify-around items-center q-py-xs">
        <q-btn flat dense class="col column items-center nav-btn active" @click="$router.push({ name: 'home' })">
          <q-icon name="home" size="24px" /><span class="text-caption">Home</span>
        </q-btn>
        <q-btn flat dense class="col column items-center nav-btn" @click="$router.push({ name: 'stats' })">
          <q-icon name="bar_chart" size="24px" /><span class="text-caption">Stats</span>
        </q-btn>
        <q-btn flat dense class="col column items-center nav-btn" @click="$router.push({ name: 'report' })">
          <q-icon name="receipt_long" size="24px" /><span class="text-caption">Report</span>
        </q-btn>
        <q-btn flat dense class="col column items-center nav-btn" @click="$router.push({ name: 'setting' })">
          <q-icon name="person" size="  24px" /><span class="text-caption">Setting</span>
        </q-btn>
      </div>
    </q-footer> -->
  </q-page> 
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { useQuasar } from 'quasar'
import { useRouter } from 'vue-router'
import BalanceCard from '../pages/BalanceCard.vue'
import AddTransactionForm from 'pages/components/AddTransactionForm.vue'

const $q = useQuasar()
const $router = useRouter()

// STATE
const currentDate = ref('')
const balance = ref(12450)
const income = ref(3200)
const expense = ref(1240)
const showBalance = ref(true)
const notificationCount = ref(0)

const showChoiceDialog = ref(false)
const showAddModal = ref(false)
const showScanModal = ref(false)
const showScanChoiceDialog = ref(false)
const showAdvancedFilters = ref(false)

// Detail Dialog State
const showDetailDialog = ref(false)
const selectedTransaction = ref(null)
const showInvoiceViewer = ref(false)
const invoiceViewerSrc = ref('')
const invoiceViewerName = ref('')

const activeFilter = ref('all')
const transactionType = ref('expense')
const expandedGroups = ref(['today'])

const searchText = ref('')
const filterType = ref('all')
const filterCategory = ref('all')

const invoiceInputRef = ref(null) // file input reference for manual form
const scanFile = ref(null) // holds QFile value for scan flow
const scanPreview = ref(null)
const isPdf = ref(false)
const scanResult = ref(null) // parsed object { amount, category, currency }
const scanning = ref(false)
const scanError = ref('')
const scanReady = ref(false)

// LOCAL data + transaction groups
const STORAGE_KEY = 'expense_data'
const transactionGroups = ref([])

// NEW transaction reactive (manual)
const newTransaction = reactive({
  amount: null,
  category: '',
  remarks: '',
  paymentMethod: 'Cash',
  date: new Date().toISOString().slice(0, 10),
  invoiceBase64: null,
  invoiceName: null
})

// options
const typeOptions = [
  { label: 'All Types', value: 'all' },
  { label: 'Income', value: 'income' },
  { label: 'Expense', value: 'expense' }
]
const paymentMethods = ['Cash', 'Credit Card', 'Debit Card', 'Bank Transfer', 'PayPal', 'Other']
const filters = [
  { label: 'All', value: 'all' },
  { label: 'Today', value: 'today' },
  { label: 'This Week', value: 'week' },
  { label: 'This Month', value: 'month' }
]
const categoryOptions = [
  { label: 'Food & Dining', value: 'food' },
  { label: 'Transport', value: 'transport' },
  { label: 'Shopping', value: 'shopping' },
  { label: 'Bills & Utilities', value: 'bills' },
  { label: 'Entertainment', value: 'entertainment' },
  { label: 'Health', value: 'health' },
  { label: 'Salary', value: 'salary' },
  { label: 'Freelance', value: 'freelance' },
  { label: 'Other', value: 'other' }
]
const filterCategoryOptions = [ { label: 'All Categories', value: 'all' }, ...categoryOptions ]
const quickActions = [
  { name: 'Transfer', icon: 'swap_horiz', bgColor: 'linear-gradient(135deg,#667eea,#764ba2)' },
  { name: 'Budget', icon: 'account_balance_wallet', bgColor: 'linear-gradient(135deg,#f093fb,#f5576c)' },
  { name: 'Goals', icon: 'flag', bgColor: 'linear-gradient(135deg,#4facfe,#00f2fe)' },
  { name: 'Cards', icon: 'credit_card', bgColor: 'linear-gradient(135deg,#43e97b,#38f9d7)' }
]

// helper computed groups show (filtering)
const baseFilteredGroups = computed(() => {
  if (activeFilter.value === 'today') return transactionGroups.value.filter(g => g.date === 'today')
  if (activeFilter.value === 'week') return transactionGroups.value
  if (activeFilter.value === 'month') return transactionGroups.value
  return transactionGroups.value
})

//const showBalance = ref(true)

function toggleBalance () {
  showBalance.value = !showBalance.value
}


function groupFilteredTransactions(transactions) {
  let rows = [...transactions]
  if (filterType.value !== 'all') rows = rows.filter(t => t.type === filterType.value)
  if (filterCategory.value !== 'all') rows = rows.filter(t => t.category === filterCategory.value)
  const q = (searchText.value || '').trim().toLowerCase()
  if (q) {
    rows = rows.filter(t => (t.remarks || '').toLowerCase().includes(q) || (t.category || '').toLowerCase().includes(q))
  }
  return rows
}

const fullyFilteredGroups = computed(() => {
  return baseFilteredGroups.value.map(g => ({ ...g, hasVisible: groupFilteredTransactions(g.transactions).length > 0 })).filter(g => g.hasVisible)
})

// Currency formatting
function formatCurrency(amount) {
  return new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD', minimumFractionDigits: 0 }).format(amount)
}

// toggle dark mode
function toggleDarkMode() { $q.dark.toggle() }
function toggleBalanceVisibility() { showNotify('Balance toggle (demo)', 'info') }
function showNotifications() { showNotify('Notifications panel coming soon!', 'info') }
function setFilter(f) { activeFilter.value = f }
function toggleGroup(date) {
  const idx = expandedGroups.value.indexOf(date)
  if (idx > -1) expandedGroups.value.splice(idx, 1)
  else expandedGroups.value.push(date)
}
function getCategoryIcon(category) {
  const icons = { food: 'restaurant', transport: 'directions_car', shopping: 'shopping_bag', bills: 'receipt', entertainment: 'movie', health: 'favorite', salary: 'payments', freelance: 'work', other: 'label' }
  return icons[category] || 'label'
}
function getCategoryColor(category) {
  const colors = { food: 'orange', transport: 'blue', shopping: 'purple', bills: 'teal', entertainment: 'pink', health: 'red', salary: 'green', freelance: 'cyan', other: 'grey' }
  return colors[category] || 'grey'
}
function getCategoryLabel(cat) { const f = categoryOptions.find(c => c.value === cat); return f ? f.label : cat }

// STORAGE helpers
function saveToLocalStorage() {
  const data = { groups: transactionGroups.value }
  try { localStorage.setItem(STORAGE_KEY, JSON.stringify(data)),
    console.log("formData",data.groups)
   } catch (e) { console.error('localStorage save error', e) }
}
function loadFromLocalStorage() {
  try {
    const raw = localStorage.getItem(STORAGE_KEY)
    if (!raw) return false
    const parsed = JSON.parse(raw)
    if (parsed && parsed.groups) {
      transactionGroups.value = parsed.groups
      recalcTotals()
      return true
    }
  } catch (e) { console.error('localStorage load error', e) }
  return false
}

function recalcTotals() {
  let inc = 0, exp = 0
  transactionGroups.value.forEach(g => {
    g.transactions.forEach(t => {
      if (t.type === 'income') inc += Number(t.amount || 0)
      else exp += Number(t.amount || 0)
    })
  })
  income.value = Math.round(inc)
  expense.value = Math.round(exp)
  balance.value = Math.round(inc - exp)
}

// initial demo data (updated with IDs)
function setDemoDataIfEmpty() {
  if (loadFromLocalStorage()) return
  transactionGroups.value = [
    {
      date: 'today',
      dateNumber: new Date().getDate(),
      displayDate: 'Today',
      dayName: new Date().toLocaleDateString('en-US', { weekday: 'long' }),
      dailyIncome: 3200,
      dailyExpense: 127.49,
      isToday: true,
      transactions: [
        { id: 'tx-demo-1', amount: 3200, category: 'salary', remarks: 'Salary Deposit', paymentMethod: 'Bank Transfer', type: 'income' },
        { id: 'tx-demo-2', amount: 12.5, category: 'food', remarks: 'Starbucks Coffee', paymentMethod: 'Credit Card', type: 'expense' },
        { id: 'tx-demo-3', amount: 89.99, category: 'shopping', remarks: 'Amazon Purchase', paymentMethod: 'Debit Card', type: 'expense' },
        { id: 'tx-demo-4', amount: 25.0, category: 'transport', remarks: 'Uber Ride', paymentMethod: 'PayPal', type: 'expense' }
      ]
    },
    {
      date: 'yesterday',
      dateNumber: new Date().getDate() - 1,
      displayDate: 'Yesterday',
      dayName: 'Yesterday',
      dailyIncome: 500,
      dailyExpense: 156.75,
      isToday: false,
      transactions: [
        { id: 'tx-demo-5', amount: 500, category: 'freelance', remarks: 'Freelance Payment', paymentMethod: 'PayPal', type: 'income' },
        { id: 'tx-demo-6', amount: 85.0, category: 'bills', remarks: 'Electricity Bill', paymentMethod: 'Auto Pay', type: 'expense' },
        { id: 'tx-demo-7', amount: 21.75, category: 'food', remarks: "McDonald's", paymentMethod: 'Cash', type: 'expense' },
        { id: 'tx-demo-8', amount: 50.0, category: 'transport', remarks: 'Gas Station', paymentMethod: 'Credit Card', type: 'expense' }
      ]
    }
  ]
  recalcTotals()
  saveToLocalStorage()
}

// open manual form from FAB
function openManualFromFab() {
  showChoiceDialog.value = false
  showScanModal.value = false
  resetNewTransaction()
  showAddModal.value = true
}

// open scan flow from FAB
function openScanChoice() {
  showChoiceDialog.value = false
  showScanChoiceDialog.value = true
}

function openCameraScan() {
  showScanChoiceDialog.value = false
  document.querySelector('[capture="environment"]').click()
}

function openUploadScan() {
  showScanChoiceDialog.value = false
  document.querySelectorAll('input[type="file"]')[1].click()
}

function retakeScan() {
  scanFile.value = null
  scanPreview.value = null
  scanResult.value = null
  scanning.value = false
  scanError.value = ''
  scanReady.value = false
  openUploadScan()
}

// invoice upload actions for manual form
function triggerInvoiceUpload() {
  invoiceInputRef.value && invoiceInputRef.value.click()
}

// handle file from manual invoice input
function handleInvoiceSelected (event) {
  const file = event.target.files ? event.target.files[0] : null
  if (!file) return
  const reader = new FileReader()
  reader.onload = e => {
    newTransaction.invoiceBase64 = e.target.result
    newTransaction.invoiceName = file.name
  }
  reader.readAsDataURL(file)
}

// clear invoice selection
function clearInvoice() {
  newTransaction.invoiceBase64 = null
  newTransaction.invoiceName = null
  if (invoiceInputRef.value) invoiceInputRef.value.value = null
}

// Add transaction (manual form submit)
function addTransaction() {
  if (!newTransaction.amount || !newTransaction.category) {
    showNotify('Please fill amount and category', 'negative')
    return
  }

  // find or create today group
  let todayGroup = transactionGroups.value.find(g => g.date === 'today')
  if (!todayGroup) {
    todayGroup = {
      date: 'today',
      dateNumber: new Date().getDate(),
      displayDate: 'Today',
      dayName: new Date().toLocaleDateString('en-US', { weekday: 'long' }),
      dailyIncome: 0,
      dailyExpense: 0,
      isToday: true,
      transactions: []
    }
    transactionGroups.value.unshift(todayGroup)
  }

  const tx = {
    id: Date.now(),
    amount: Number(newTransaction.amount),
    category: newTransaction.category,
    remarks: newTransaction.remarks || '',
    paymentMethod: newTransaction.paymentMethod,
    date: newTransaction.date,
    type: transactionType.value,
    invoiceBase64: newTransaction.invoiceBase64 || null,
    invoiceName: newTransaction.invoiceName || null
  }

  todayGroup.transactions.unshift(tx)

  // update group counters
  if (transactionType.value === 'income') {
    todayGroup.dailyIncome += tx.amount
    income.value += tx.amount
    balance.value += tx.amount
  } else {
    todayGroup.dailyExpense += tx.amount
    expense.value += tx.amount
    balance.value -= tx.amount
  }

  saveToLocalStorage()
  showAddModal.value = false
  resetNewTransaction()
  showNotify('Transaction added!', 'positive')
}

// reset manual form
function resetNewTransaction() {
  newTransaction.amount = null
  newTransaction.category = ''
  newTransaction.remarks = ''
  newTransaction.paymentMethod = 'Cash'
  newTransaction.date = new Date().toISOString().slice(0, 10)
  newTransaction.invoiceBase64 = null
  newTransaction.invoiceName = null
  if (invoiceInputRef.value) invoiceInputRef.value.value = null
}

// ==================================================
// NEW LOGIC: Transaction Details & Viewer
// ==================================================

function openTransactionDetail(tx) {
  selectedTransaction.value = tx
  showDetailDialog.value = true
}

function deleteTransactionConfirm() {
  $q.dialog({
    title: 'Delete Transaction',
    message: 'Are you sure you want to delete this transaction?',
    cancel: true,
    persistent: true
  }).onOk(() => {
    deleteTransaction()
  })
}

function deleteTransaction() {
  if (!selectedTransaction.value) return
  
  const txId = selectedTransaction.value.id
  // Find in groups and remove
  for (const group of transactionGroups.value) {
    const idx = group.transactions.findIndex(t => t.id === txId)
    if (idx !== -1) {
      group.transactions.splice(idx, 1)
      break
    }
  }
  
  recalcTotals()
  saveToLocalStorage()
  showDetailDialog.value = false
  showNotify('Transaction deleted', 'info')
}

function viewInvoice(tx) {
  if (tx && tx.invoiceBase64) {
    invoiceViewerSrc.value = tx.invoiceBase64
    invoiceViewerName.value = tx.invoiceName || 'invoice'
    showInvoiceViewer.value = true
  }
}

function downloadCurrentInvoice() {
  if (!invoiceViewerSrc.value) return
  const link = document.createElement('a')
  link.href = invoiceViewerSrc.value
  link.download = invoiceViewerName.value || 'invoice'
  link.click()
}

function isInvoicePdf(src) {
  if (!src) return false
  return src.startsWith('data:application/pdf')
}

// Scan file handling
function onCameraCaptured(e) {
  const file = e.target.files[0]
  if (file) {
    scanFile.value = file
    processScanFile(file)
  }
}

function onUploadSelected(e) {
  const file = e.target.files[0]
  if (file) {
    scanFile.value = file
    processScanFile(file)
  }
}

function processScanFile(file) {
  const reader = new FileReader()
  reader.onload = e => {
    const url = e.target.result
    if (file.type === 'application/pdf') {
      isPdf.value = true
      scanPreview.value = null
    } else {
      isPdf.value = false
      scanPreview.value = url
    }
    // Simulate parsing
    scanning.value = true
    scanError.value = ''
    scanResult.value = null
    scanReady.value = false
    
    setTimeout(() => {
      scanning.value = false
      // Mock result
      scanResult.value = tryParseFromFilenameAndData(file.name, url)
      scanReady.value = true
    }, 1500)
  }
  reader.readAsDataURL(file)
}

function tryParseFromFilenameAndData(filename, dataUrl) {
  const filenameNumbers = filename.match(/([0-9]+(?:[.,][0-9]{1,2})?)/g)
  let amount = null
  if (filenameNumbers && filenameNumbers.length) {
    amount = filenameNumbers[filenameNumbers.length - 1].replace(',', '.')
  }
  const lower = filename.toLowerCase()
  const mapping = [
    { kw: ['uber', 'taxi'], cat: 'transport' },
    { kw: ['starbucks', 'coffee', 'cafe'], cat: 'food' },
    { kw: ['amazon', 'shop', 'shopping'], cat: 'shopping' },
    { kw: ['electric', 'power', 'bill'], cat: 'bills' },
    { kw: ['salary', 'payroll'], cat: 'salary' }
  ]
  let category = null
  for (const m of mapping) {
    if (m.kw.some(k => lower.includes(k))) { category = m.cat; break }
  }
  return { amount: amount ? parseFloat(amount) : null, currency: amount ? 'USD' : null, category }
}

function useScanResult() {
  if (!scanResult.value) {
    showNotify('Nothing parsed. Please use manual entry.', 'negative')
    return
  }
  newTransaction.amount = scanResult.value.amount || null
  newTransaction.category = scanResult.value.category || ''
  newTransaction.remarks = (scanFile.value && scanFile.value.name) ? `Scanned: ${scanFile.value.name}` : 'Scanned invoice'
  newTransaction.invoiceBase64 = null
  newTransaction.invoiceName = (scanFile.value && scanFile.value.name) ? scanFile.value.name : null
  
  const fileObj = scanFile.value
  if (fileObj) {
    const reader = new FileReader()
    reader.onload = e => {
      newTransaction.invoiceBase64 = e.target.result
    }
    reader.readAsDataURL(fileObj)
  }
  showScanModal.value = false
  showAddModal.value = true
}

function closeAddModal() {
  showAddModal.value = false
}

function showNotify(message, type = 'info') {
  $q.notify({ message, type, position: 'top', timeout: 2000 })
}

function onActionClick(action) { showNotify(`${action.name} coming soon!`, 'info') }

// LIFECYCLE
onMounted(() => {
  const now = new Date()
  currentDate.value = now.toLocaleDateString('en-US', { weekday: 'short', month: 'short', day: 'numeric' })
  setDemoDataIfEmpty()
})
</script>

<style scoped>
/* ===== Bank Header ===== */
.bank-header {
  background: #2b5569;
  border-radius: 0 0 24px 24px;
}

/* Main glass card */
.bank-card {
  background: rgba(255, 255, 255, 0.14);
  backdrop-filter: blur(10px);
  border-radius: 20px;
  border: 1px solid rgba(255,255,255,0.18);
}

/* Mini cards */
.mini-card {
  padding: 14px;
  border-radius: 16px;
  backdrop-filter: blur(6px);
}

/* Expense */
.expense-glass {
  background: rgba(239, 68, 68, 0.18);
}

/* Income */
.income-glass {
  background: rgba(16, 185, 129, 0.18);
}

/* Soft colors */
.text-green-soft { color: #6ee7b7; }
.text-red-soft { color: #fca5a5; }
w { box-shadow: 0 6px 18px rgba(15,23,42,0.06); }

/* Action icon background */
.action-icon-bg { width:36px; height:36px; border-radius:10px; display:flex; align-items:center; justify-content:center; }

/* Toggle styling for income/expense */
.custom-toggle .q-btn { background: #f3f4f6; color: #1f2937; border-radius: 10px; }
.custom-toggle .expense-btn.q-btn--active { background-color: #ef4444 !important; color: #fff !important; }
.custom-toggle .income-btn.q-btn--active { background-color: #10b981 !important; color: #fff !important; }

/* small visuals */
.rotate-180 { transform: rotate(180deg); }
.expand-icon { transition: transform 0.25s ease; }

/* Floating button pulse */
.floating-btn { animation: pulse 2s infinite; }
@keyframes pulse {
  0% { box-shadow: 0 0 0 0 rgba(79,70,229,0.35); }
  70% { box-shadow: 0 0 0 10px rgba(79,70,229,0); }
  100% { box-shadow: 0 0 0 0 rgba(79,70,229,0); }
}

/* Drag handle for bottom sheet */
.drag-handle { width:40px; height:4px; background:#e5e7eb; border-radius:4px; }

/* Colors */
.text-positive { color: #16a34a !important; }
.text-negative { color: #dc2626 !important; }

/* Nav */
.nav-btn { color: #9ca3af; }
.nav-btn.active { color: #6366f1; }
.nav-btn .text-caption { font-size: 10px; margin-top:2px; }

/* Detail Dialog Styling */
.detail-label { color: #6b7280; font-size: 0.9rem; }
.detail-value { color: #111827; font-weight: 500; font-size: 0.95rem; text-align: right; }
.detail-row { min-height: 40px; }
</style>