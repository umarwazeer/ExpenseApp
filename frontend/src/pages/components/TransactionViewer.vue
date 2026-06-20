    <!-- src/pages/components/TransactionViewer.vue -->
    <template>
    <q-dialog :model-value="modelValue" @update:model-value="$emit('update:modelValue', $event)" full-width full-height>
        <q-card class="viewer-card q-pa-none">
        
        <!-- Top Toolbar (Back and Delete Icons) -->
        <q-toolbar class="viewer-toolbar text-white">
            <q-btn icon="arrow_back" flat round dense v-close-popup />
            <q-toolbar-title class="text-weight-medium">Transaction Details</q-toolbar-title>
            <q-btn icon="delete" flat round dense @click="deleteTransactionConfirm(transaction)" />
        </q-toolbar>

        <!-- Main Content Area -->
        <q-card-section class="q-pt-lg q-pb-xl">
            <div class="dash-border q-pa-lg">
            
            <!-- Category Icon & Amount -->
            <div class="column items-center">
                <q-avatar size="80px" :color="getCategoryColor(transaction.category) + '-4'">
                <q-icon :name="getCategoryIcon(transaction.category)" size="40px" color="white" />
                </q-avatar>
                
                <q-badge
                :color="transaction.type === 'expense' ? 'red-8' : 'green-8'"
                class="q-mt-md text-weight-medium"
                style="padding: 4px 10px;"
                >
                {{ transaction.type === 'expense' ? 'Expense' : 'Income' }}
                </q-badge>
                
                <div class="text-h4 text-white text-weight-bold q-mt-sm">
                <!-- {{ formatCurrency(transaction.amount) }} -->
                </div>
            </div>
            
            <!-- Edit Button -->
            <q-btn 
                fab 
                icon="edit" 
                color="indigo" 
                size="sm"
                class="edit-fab"
                @click="$emit('edit', transaction)"
            />

            <!-- Transaction Details List -->
            <div class="text-h6 text-white q-mt-xl q-mb-md">Transaction Details</div>
            
            <q-list separator class="details-list">
                <q-item>
                <q-item-section class="detail-label">Status</q-item-section>
                <q-item-section side :class="transaction.type === 'expense' ? 'text-red' : 'text-positive'">
                    {{ transaction.type === 'expense' ? 'Expense' : 'Income' }}
                </q-item-section>
                </q-item>
                
                <q-item>
                <q-item-section class="detail-label">To / Remarks</q-item-section>
                <q-item-section side class="detail-value text-white">{{ transaction.remarks || 'N/A' }}</q-item-section>
                </q-item>

                <q-item>
                <q-item-section class="detail-label">Category</q-item-section>
                <q-item-section side class="detail-value text-white">{{ getCategoryLabel(transaction.category) }}</q-item-section>
                </q-item>
                
                <q-item>
                <q-item-section class="detail-label">Date</q-item-section>
                <q-item-section side class="detail-value text-white">{{ transaction.date }}</q-item-section>
                </q-item>
                
                <q-item>
                <q-item-section class="detail-label">Payment</q-item-section>
                <q-item-section side class="detail-value text-white">{{ transaction.paymentMethod }}</q-item-section>
                </q-item>

                <q-item>
                <q-item-section class="detail-label">Amount</q-item-section>
                <!-- <q-item-section side class="detail-value text-white">{{ formatCurrency(transaction.amount) }}</q-item-section> -->
                </q-item>
                
                <q-item v-if="transaction.invoiceBase64">
                <q-item-section class="detail-label">Invoice</q-item-section>
                <q-item-section side>
                    <q-btn flat dense label="View" color="indigo" @click="$emit('viewInvoice', transaction)" />
                </q-item-section>
                </q-item>
            </q-list>
            </div>
        </q-card-section>
        
        <!-- Download FAB -->
        <q-page-sticky position="bottom-right" :offset="[20, 20]">
            <q-btn 
            fab 
            icon="download" 
            color="indigo" 
            @click="$emit('downloadInvoice', transaction)" 
            :disable="!transaction.invoiceBase64"
            />
        </q-page-sticky>
        
        </q-card>
    </q-dialog>
    </template>

    <script setup>
    import { 
    ref, 
    reactive, 
    computed, 
    watch, 
    onMounted, 
    onUnmounted, 
    nextTick 
    } from 'vue';

    import { useQuasar } from 'quasar';

    const props = defineProps({
    modelValue: Boolean,
    transaction: Object, // The transaction object to display
    categoryOptions: Array,
    });

    const emit = defineEmits(['update:modelValue', 'edit', 'viewInvoice', 'downloadInvoice', 'delete']);

    const $q = useQuasar();

    // function formatCurrency(amount) {
    // if (amount == null) return 'Rs 0.00'
    // return `Rs ${Number(amount).toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`;
    // }

    function getCategoryLabel(cat) {
    const f = props.categoryOptions.find(c => c.value === cat);
    return f ? f.label : cat;
    }

    function getCategoryIcon(category) {
    const icons = { food: 'restaurant', transport: 'directions_car', shopping: 'shopping_bag', bills: 'receipt', entertainment: 'movie', health: 'favorite', salary: 'payments', freelance: 'work', other: 'label' }
    return icons[category] || 'label'
    }

    function getCategoryColor(category) {
    const colors = { food: 'orange', transport: 'blue', shopping: 'purple', bills: 'teal', entertainment: 'pink', health: 'red', salary: 'green', freelance: 'cyan', other: 'grey' }
    return colors[category] || 'grey'
    }

    function deleteTransactionConfirm(tx) {
    $q.dialog({
        title: 'Confirm Delete',
        message: `Are you sure you want to delete this ${tx.type}?`,
        cancel: true,
        persistent: true,
        ok: { label: 'Delete', color: 'negative' }
    }).onOk(() => {
        emit('delete', tx);
    });
    }
    </script>

    <style scoped>
    .viewer-card {
    background-color: #1a1c22; /* Dark background matching screenshot */
    color: white;
    }

    .viewer-toolbar {
    background-color: #2f343a; /* Dark toolbar color */
    color: white;
    }

    .dash-border {
    border: 2px dashed rgba(255, 255, 255, 0.2);
    border-radius: 20px;
    position: relative;
    padding: 30px 15px 50px 15px;
    }

    .edit-fab {
    position: absolute;
    top: 15px;
    right: 15px;
    background-color: #4f46e5;
    }

    .details-list {
    background: transparent;
    }
    .details-list .q-item {
    padding: 10px 0;
    color: #c9c9c9;
    }

    .detail-label {
    flex: 0 0 40%;
    font-weight: 500;
    color: #c9c9c9;
    }
    .detail-value {
    flex: 1;
    text-align: right;
    font-weight: 700;
    }
    .text-red { color: #f87171 !important; }
    .text-positive { color: #4ade80 !important; }
    </style>