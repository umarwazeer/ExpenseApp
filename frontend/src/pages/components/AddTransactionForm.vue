<template>
  <q-card class="bg-white rounded-t-3xl" style="max-height: 90vh">
    <!-- drag handle -->
    <div class="q-mt-sm q-mb-md flex justify-center">
      <div class="drag-handle" />
    </div>
      
    <q-card-section class="row items-center">
      
      <div class="text-h6 text-weight-bold">Add Transaction</div>

      <q-space />
      <q-btn icon="close" flat round dense v-close-popup />

    </q-card-section>

    <q-card-section style="padding: 4px 15px;">
      <q-form @submit.prevent="addTransaction" class="">

        <!-- Transaction Type -->
        <div>
          <div class="text-caption  text-grey-7 q-mb-xs">Transaction Type</div>
          <q-btn-toggle
            v-model="form.expense_type"
            spread
            rounded
            no-caps
            class="full-width q-mb-md"
            :options="[
              { label: 'Expense', value: 'expense', icon: 'arrow_upward' },
              { label: 'Income', value: 'income', icon: 'arrow_downward' }
            ]"
          />
        </div>

        <!-- Amount -->
        <q-input
          v-model.number="form.amount"
          type="number"
          filled
          prefix="Rs "
          label="Amount"
          input-class="text-h5 text-weight-bold"
          :rules="[v => !!v || 'Amount is required']"
        />

        <!-- Category -->
        <q-select
          v-model="form.category"
          :options="categoryOptions"
          label="Category"
          emit-value
          map-options
          filled
          :loading="loadingCategories"
          :rules="[v => !!v || 'Category is required']"
        />

        <!-- Remarks -->
        <q-input
          v-model="form.description"
          label="Remarks"
          filled
        />

        <!-- Invoice Upload -->
        <div class="text-subtitle2 text-grey-9 q-mt-md">Invoice</div>
        <div
          class="q-pa-md q-mt-xs flex flex-center cursor-pointer"
          style="border: 2px dashed #b8b8b8; border-radius: 12px"
          @click="invoiceInput.click()"
        >
          <div class="column items-center">
            <q-icon name="upload" size="28px" color="primary" />
            <div class="text-primary q-mt-xs">Add Invoice</div>
            <div class="text-caption text-grey-6">Optional</div>
          </div>
        </div>

        <input
          ref="invoiceInput"
          type="file"
          class="hidden"
          accept="image/*,application/pdf"
          @change="onInvoiceSelect"
        />

        <!-- Invoice Preview -->
        <q-card v-if="invoiceName" flat bordered class="q-mt-sm q-pa-sm">
          <div class="row items-center">
            <q-icon name="attach_file" />
            <div class="q-ml-sm">{{ invoiceName }}</div>
            <q-space />
            <q-btn icon="close" flat dense @click="clearInvoice" />
          </div>
        </q-card>

        <!-- Payment Method -->
        <q-select
          v-model="form.payment_method"
          :options="paymentMethods"
          label="Payment Method"
          filled
        />

        <!-- Date -->
        <q-input v-model="form.date" filled label="Date" readonly>
          <template #append>
            <q-icon name="event" class="cursor-pointer">
              <q-popup-proxy transition-show="scale">
                <q-date v-model="form.date" mask="YYYY-MM-DD" />
              </q-popup-proxy>
            </q-icon>
          </template>
        </q-input>

        <!-- Actions -->
        <div class="row q-gutter-sm q-mt-md">
          <q-btn flat label="Cancel" class="col" @click="$emit('close')" />
          <q-btn label="Add Transaction" type="submit" color="indigo" class="col" />
        </div>

      </q-form>
    </q-card-section>
      
  </q-card>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { api } from 'src/boot/axios'
import { useQuasar } from 'quasar'

const emit = defineEmits(['saved', 'close'])
const $q = useQuasar()
  
const loadingCategories = ref(false)
const categoryOptions = ref([
  { label: 'Food & Groceries', value: 1 },
  { label: 'Transport', value: 2 },
  { label: 'Rent', value: 3 },
  { label: 'Utilities', value: 4 },
  { label: 'Shopping', value: 5 },
  { label: 'Entertainment', value: 6 },
  { label: 'Healthcare', value: 7 },
  { label: 'Education', value: 8 },
  { label: 'Salary', value: 9 },
  { label: 'Freelance', value: 10 },
  { label: 'Business', value: 11 },
  { label: 'Investment', value: 12 },
  { label: 'Other', value: 99 }
])
const invoiceInput = ref(null)
const invoiceFile = ref(null)
const invoiceName = ref('')

const paymentMethods = [
  'Cash',
  'Bank Transfer',
  'Card',
  'UPI'
]

const form = reactive({
  amount: null,
  category: null,
  description: '',
  expense_type: 'expense',
  payment_method: '',
  date: new Date().toISOString().slice(0, 10)
})

/* ================== FETCH CATEGORIES ================== */
onMounted(fetchCategories)

async function fetchCategories () {
  loadingCategories.value = true
  try {
    const res = await api.get('/categories/')
    categoryOptions.value = res.data.map(c => ({
    label: c.name,
    value: c.id
    }))
    console.log('categoryOptions', categoryOptions.value)

  } catch (e) {
    $q.notify({ type: 'negative', message: 'Failed to load categories' })
  } finally {
    loadingCategories.value = false
  }
}

/* ================== INVOICE ================== */
function onInvoiceSelect (e) {
  invoiceFile.value = e.target.files[0]
  invoiceName.value = invoiceFile.value?.name || ''
}

function clearInvoice () {
  invoiceFile.value = null
  invoiceName.value = ''
}

/* ================== SUBMIT ================== */
async function addTransaction () {
  try {
    const fd = new FormData()

    Object.entries(form).forEach(([key, value]) => {
      if (value !== null && value !== '' && value !== undefined) {
        fd.append(key, value)
      }
    })

    if (invoiceFile.value) {
      fd.append('receipt', invoiceFile.value)
    }

    await api.post('/expenses/', fd, {
            headers: { 'Content-Type': 'multipart/form-data' }
        })


    $q.notify({ type: 'positive', message: 'Transaction added' })
    console.log("formData", fd)
    emit('saved')
    emit('close')

  } catch (e) {
    console.error(e.response?.data || e)
    $q.notify({ type: 'negative', message: 'Failed to add transaction' })
  }
}

</script>
