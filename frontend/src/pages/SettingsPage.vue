<template>
  <q-page :class="pageBgClass" class="settings-page q-pb-xl">
    <!-- Header -->
    <div :class="headerBgClass" class="settings-header q-pt-md q-pb-xl">
      <div class="text-h5 text-center text-weight-bold q-mb-md" :class="headerTextColor">Settings</div>

      <div class="column items-center q-mb-md">
        <q-avatar size="96px" class="q-mb-sm" :color="$q.dark.isActive ? 'grey-9' : 'grey-3'">
          <img v-if="store.profile.avatarBase64" :src="store.profile.avatarBase64" alt="avatar" />
          <q-icon v-else name="person" size="40px" />
        </q-avatar>

        <div class="row items-center q-gutter-sm">
          <div class="text-h6 text-weight-medium" :class="headerTextColor">{{ store.profile.name || 'Your Name' }}</div>
          <q-btn dense flat icon="photo_camera" @click="triggerFilePicker" />
        </div>

        <input ref="fileInput" type="file" accept="image/*" @change="onFileChange" style="display:none" />
        <div v-if="avatarPreview" class="q-mt-sm">
          <div class="text-caption q-mb-xs">Preview</div>
          <img :src="avatarPreview" alt="preview" style="max-width:140px; border-radius: 8px" />
          <div class="row q-mt-xs">
            <q-btn dense label="Save" color="indigo" @click="saveAvatar" class="q-mr-sm" />
            <q-btn dense flat label="Cancel" @click="cancelAvatar" />
          </div>
        </div>
      </div>
    </div>

    <!-- Body -->
    <main class="q-px-md" style="margin-top: -40px;">
      <!-- Profile Section -->
      <div class="setting-section-label text-grey-5 q-my-md">Profile</div>
      <q-list :class="listBgClass" class="settings-list rounded-xl q-mb-lg">
        <q-item>
          <q-item-section>
            <UserProfileForm @save="onProfileSave" />
          </q-item-section>
        </q-item>
      </q-list>

      <!-- App settings -->
      <div class="setting-section-label text-grey-5 q-my-md">Application Settings</div>
      <q-list :class="listBgClass" class="settings-list rounded-xl q-mb-lg">
        <q-item>
          <q-item-section avatar>
            <q-icon name="payments" class="list-icon" />
          </q-item-section>
          <q-item-section :class="listTextColor">Currency</q-item-section>
          <q-item-section side>
            <CurrencySelector v-model="store.ui.currency" :dark="$q.dark.isActive" @change="persist" />
          </q-item-section>
        </q-item>

                <q-separator :dark="$q.dark.isActive" inset />

            <q-item clickable v-ripple @click="openCategories">
              <q-item-section avatar>
                <q-icon name="category" class="list-icon" />
              </q-item-section>
              <q-item-section :class="listTextColor">
                Categories
                <!-- <div class="text-caption text-grey-6">
                  Manage income & expense categories
                </div> -->
              </q-item-section>
              <q-item-section side>
                <q-icon name="chevron_right" color="grey-6" />
              </q-item-section>
            </q-item>

        <q-separator :dark="$q.dark.isActive" inset />

        <q-item>
          <q-item-section avatar>
            <q-icon name="palette" class="list-icon" />
          </q-item-section>
          <q-item-section :class="listTextColor">Accent Color</q-item-section>
          <q-item-section side>
            <q-input dense type="color" v-model="store.ui.accentColor" @input="onAccentChange" />
          </q-item-section>
        </q-item>

        <q-separator :dark="$q.dark.isActive" inset />

        <q-item>
          <q-item-section avatar>
            <q-icon name="language" class="list-icon" />
          </q-item-section>
          <q-item-section :class="listTextColor">Language</q-item-section>
          <q-item-section side>
            <LanguageSelector v-model="store.ui.language" :dark="$q.dark.isActive" @change="persist" />
          </q-item-section>
        </q-item>

        <q-separator :dark="$q.dark.isActive" inset />

        <q-item>
          <q-item-section avatar>
            <q-icon name="toggle_on" class="list-icon" />
          </q-item-section>
          <q-item-section :class="listTextColor">Dark Mode</q-item-section>
          <q-item-section side>
            <ThemeSwitcher v-model="store.ui.darkMode" />
          </q-item-section>
        </q-item>
      </q-list>

      <!-- Advanced -->
      <div class="setting-section-label text-grey-5 q-my-md">Advanced Settings</div>
      <q-list :class="listBgClass" class="settings-list rounded-xl q-mb-lg">

        <!-- App Lock -->
        <q-item>
          <q-item-section avatar><q-icon name="lock" class="list-icon" /></q-item-section>
          <q-item-section :class="listTextColor">App Lock (PIN)</q-item-section>
          <q-item-section side>
            <q-toggle v-model="store.advanced.appLockEnabled" @update:model-value="onToggleAppLock" />
          </q-item-section>
        </q-item>
        <q-separator :dark="$q.dark.isActive" inset />
        <q-item v-if="store.advanced.appLockEnabled">
          <q-item-section>
            <div class="row items-center q-gutter-sm">
              <q-input dense v-model="pinInput" label="Set/Change PIN" maxlength="6" type="password" style="max-width:140px" />
              <q-btn dense label="Save PIN" color="indigo" @click="savePIN" />
            </div>
          </q-item-section>
        </q-item>

        <q-separator :dark="$q.dark.isActive" inset />

        <!-- Sound & Haptics -->
        <q-item>
          <q-item-section avatar><q-icon name="volume_up" class="list-icon" /></q-item-section>
          <q-item-section :class="listTextColor">Sound</q-item-section>
          <q-item-section side>
            <q-toggle v-model="store.ui.sound" @update:model-value="persist" />
          </q-item-section>
        </q-item>

        <q-separator :dark="$q.dark.isActive" inset />

        <q-item>
          <q-item-section avatar><q-icon name="vibration" class="list-icon" /></q-item-section>
          <q-item-section :class="listTextColor">Haptics</q-item-section>
          <q-item-section side>
            <q-toggle v-model="store.ui.haptics" @update:model-value="persist" />
          </q-item-section>
        </q-item>

        <q-separator :dark="$q.dark.isActive" inset />

        <!-- Notifications -->
        <q-item>
          <q-item-section avatar><q-icon name="notifications" class="list-icon" /></q-item-section>
          <q-item-section :class="listTextColor">Notifications</q-item-section>
          <q-item-section side>
            <q-toggle v-model="store.advanced.notifications.enabled" @update:model-value="persist" />
          </q-item-section>
        </q-item>

        <q-separator :dark="$q.dark.isActive" inset />

        <!-- Auto Backup -->
        <q-item>
          <q-item-section avatar><q-icon name="backup" class="list-icon" /></q-item-section>
          <q-item-section :class="listTextColor">Auto Backup</q-item-section>
          <q-item-section side>
            <q-toggle v-model="store.advanced.autoBackup.enabled" @update:model-value="persist" />
          </q-item-section>
        </q-item>

        <q-item v-if="store.advanced.autoBackup.enabled">
          <q-item-section>
            <q-select dense v-model="store.advanced.autoBackup.schedule" :options="['daily','weekly','monthly']" emit-value map-options />
          </q-item-section>
        </q-item>

        <q-separator :dark="$q.dark.isActive" inset />

        <!-- Storage Provider -->
        <q-item>
          <q-item-section avatar><q-icon name="cloud" class="list-icon" /></q-item-section>
          <q-item-section :class="listTextColor">Storage Provider</q-item-section>
          <q-item-section side>
            <q-select dense v-model="store.advanced.storageProvider" :options="storageOptions" @update:model-value="onStorageProviderChange" />
          </q-item-section>
        </q-item>

        <q-separator :dark="$q.dark.isActive" inset />

        <!-- Import / Export -->
        <q-item>
          <q-item-section avatar><q-icon name="file_upload" class="list-icon" /></q-item-section>
          <q-item-section :class="listTextColor">Import / Export</q-item-section>
          <q-item-section side>
            <q-btn dense flat label="Export" @click="exportSettings" />
            <q-btn dense flat label="Import" @click="triggerImport" />
            <input ref="importInput" type="file" accept="application/json" @change="onImportFile" style="display:none" />
          </q-item-section>
        </q-item>

        <q-separator :dark="$q.dark.isActive" inset />

        <!-- Connected accounts (stub) -->
        <q-item clickable v-ripple @click="notify('Connect accounts (stub)')">
          <q-item-section avatar><q-icon name="link" class="list-icon" /></q-item-section>
          <q-item-section :class="listTextColor">Manage Connected Accounts</q-item-section>
          <q-item-section side><q-icon name="chevron_right" color="grey-6" /></q-item-section>
        </q-item>

        <q-separator :dark="$q.dark.isActive" inset />

        <!-- Clear All -->
        <q-item>
          <q-item-section avatar><q-icon name="delete_forever" color="red" class="list-icon" /></q-item-section>
          <q-item-section class="text-red">Clear All Data</q-item-section>
          <q-item-section side>
            <q-btn dense flat color="red" label="Clear" @click="confirmClear" />
          </q-item-section>
        </q-item>
      </q-list>

      <!-- Other -->
      <div class="setting-section-label text-grey-5 q-my-md">Other</div>
      <q-list :class="listBgClass" class="settings-list rounded-xl q-mb-xl">
        <q-item clickable v-ripple @click="notify('Premium Upgrade!')">
          <q-item-section avatar><q-icon name="workspace_premium" color="amber" class="list-icon" /></q-item-section>
          <q-item-section :class="listTextColor">Upgrade to Premium</q-item-section>
          <q-item-section side><q-icon name="chevron_right" color="grey-6" /></q-item-section>
        </q-item>
      </q-list>
    </main>

    <!-- Confirm Clear Dialog -->
    <q-dialog v-model="confirmClearDialog">
      <q-card>
        <q-card-section class="text-h6">Confirm</q-card-section>
        <q-card-section>Are you sure you want to clear all local settings? This cannot be undone.</q-card-section>
        <q-card-actions align="right">
          <q-btn flat label="Cancel" v-close-popup />
          <q-btn flat label="Clear" color="red" @click="doClearAll" />
        </q-card-actions>
      </q-card>
    </q-dialog>

    <!-------------------currency Dailog section ---------->
    <q-dialog v-model="categoryDialog" position="bottom">
  <q-card class="rounded-t-3xl" style="max-height: 85vh">
    <q-card-section class="row items-center">
      <div class="text-h6">Manage Categories</div>
      <q-space />
      <q-btn icon="close" flat round dense v-close-popup />
    </q-card-section>

    <q-separator />

    <!-- Add Category -->
    <q-card-section>
      <q-form @submit.prevent="addCategory" class="row q-col-gutter-sm">
        <q-input
          v-model="newCategory.name"
          label="Category name"
          filled
          class="col"
          :rules="[v => !!v || 'Required']"
        />
        <q-select
          v-model="newCategory.type"
          :options="['expense', 'income']"
          label="Type"
          filled
          class="col-4"
        />
         <div class="col-2 flex justify-end pt-3">
          <q-btn
            icon="add"
            color="indigo"
            unelevated
            round
            style="height: 50px; min-width: 50px"
            type="submit"
          />
      </div>
      </q-form>
    </q-card-section>

    <q-separator />

    <!-- Category List -->
    <q-list bordered>
      <q-item v-for="cat in categories" :key="cat.id">
        <q-item-section>
          <div class="text-weight-medium">{{ cat.name }}</div>
          <div class="text-caption text-grey-6">{{ cat.type }}</div>
        </q-item-section>

        <q-item-section side>
          <q-btn
            icon="delete"
            flat
            dense
            color="red"
            @click="deleteCategory(cat.id)"
          />
        </q-item-section>
      </q-item>
    </q-list>
  </q-card>
</q-dialog>

  </q-page>
</template>

<script setup>
import { ref } from 'vue';
import { useQuasar } from 'quasar';
import { useSettingsStore } from 'src/stores/settings';
import StorageService from 'src/utils/storageService';
import { computed } from 'vue'
import { api } from 'src/boot/axios'

import UserProfileForm from 'src/pages/components/settings/UserProfileForm.vue';
import ThemeSwitcher from 'src/pages/components/settings/ThemeSwitcher.vue';
import LanguageSelector from 'src/pages/components/settings/LanguageSelector.vue';
import CurrencySelector from 'src/pages/components/settings/CurrencySelector.vue';

const categoryDialog = ref(false)

const categories = ref([])
const newCategory = ref({
  name: '',
  type: 'expense'
})

const $q = useQuasar();
const store = useSettingsStore();

// apply storage provider to service
StorageService.setProvider(store.advanced.storageProvider);

const fileInput = ref(null);
const importInput = ref(null);
const avatarPreview = ref(null);

const pinInput = ref('');
const confirmClearDialog = ref(false);

const pageBgClass = computed(() => $q.dark.isActive ? 'bg-dark-page' : 'bg-white-page');
const headerBgClass = computed(() => $q.dark.isActive ? 'bg-dark-header' : 'bg-light-header');
const headerTextColor = computed(() => $q.dark.isActive ? 'text-white' : 'text-dark-blue');
const listBgClass = computed(() => $q.dark.isActive ? 'bg-dark-list' : 'bg-white-list');
const listTextColor = computed(() => $q.dark.isActive ? 'text-white' : 'text-dark-blue');

const storageOptions = [
  { label: 'LocalStorage (default)', value: 'local' },
  { label: 'Pinia (in-memory) - not remote', value: 'pinia' },
  { label: 'Supabase (not configured)', value: 'supabase' },
  { label: 'Firebase (not configured)', value: 'firebase' },
  { label: 'Vuex (legacy)', value: 'vuex' }
];


function openCategories () {
  categoryDialog.value = true
  fetchCategories()
}

async function fetchCategories () {
  try {
    const res = await api.get('api/categories/')
    categories.value = res.data
  } catch (e) {
    $q.notify({ type: 'negative', message: 'Failed to load categories' })
  }
}

async function addCategory () {
  try {
    await api.post('/categories/', newCategory.value)
    newCategory.value.name = ''
    newCategory.value.type = 'expense'
    fetchCategories()
    $q.notify({ type: 'positive', message: 'Category added' })
  } catch (e) {
    $q.notify({ type: 'negative', message: 'Failed to add category' })
  }
}

async function deleteCategory (id) {
  try {
    await api.delete(`/categories/${id}/`)
    fetchCategories()
    $q.notify({ type: 'positive', message: 'Category deleted' })
  } catch (e) {
    $q.notify({ type: 'negative', message: 'Failed to delete category' })
  }
}

function triggerFilePicker() {
  fileInput.value && fileInput.value.click();
}

function onFileChange(e) {
  const file = e.target.files[0];
  if (!file) return;
  const reader = new FileReader();
  reader.onload = (ev) => {
    avatarPreview.value = ev.target.result;
  };
  reader.readAsDataURL(file);
}

function saveAvatar() {
  store.setProfile({ avatarBase64: avatarPreview.value });
  avatarPreview.value = null;
  $q.notify({ message: 'Profile picture saved', color: 'positive' });
}

function cancelAvatar() {
  avatarPreview.value = null;
  if (fileInput.value) fileInput.value.value = '';
}

// function onProfileSave(payload) {
//   store.setProfile(payload);
//   $q.notify({ message: 'Profile updated', color: 'positive' });
// }

function onAccentChange() {
  store.persist?.() || store.persist; // persist if available
  // Bonus: apply to document root for CSS variables
  document.documentElement.style.setProperty('--app-accent', store.ui.accentColor);
  store.persist();
}

function onToggleAppLock(val) {
  store.setAdvanced({ appLockEnabled: val });
  if (!val) store.setPIN(null);
}

function savePIN() {
  if (!pinInput.value || pinInput.value.length < 4) {
    $q.notify({ message: 'PIN must be at least 4 digits', color: 'negative' });
    return;
  }
  store.setPIN(pinInput.value);
  $q.notify({ message: 'PIN saved', color: 'positive' });
  pinInput.value = '';
}

function triggerImport() {
  importInput.value && importInput.value.click();
}

// function onImportFile(e) {
//   const f = e.target.files[0];
//   if (!f) return;
//   const reader = new FileReader();
//   reader.onload = (ev) => {
//     try {
//       const parsed = JSON.parse(ev.target.result);
//       // Basic merge - validate shape minimally
//       if (parsed.profile || parsed.ui || parsed.advanced) {
//         store.setProfile(parsed.profile || {});
//         store.setUI(parsed.ui || {});
//         store.setAdvanced(parsed.advanced || {});
//         $q.notify({ message: 'Settings imported', color: 'positive' });
//       } else {
//         $q.notify({ message: 'Invalid settings file', color: 'negative' });
//       }
//     } catch (err) {
//       $q.notify({ message: 'Failed to import: invalid JSON', color: 'negative' });
//     }
//   };
//   reader.readAsText(f);
//   if (importInput.value) importInput.value.value = '';
// }

function exportSettings() {
  const payload = JSON.stringify({
    // profile: store.profile,
    ui: store.ui,
    advanced: store.advanced
  }, null, 2);
  const blob = new Blob([payload], { type: 'application/json' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = 'expense-app-settings.json';
  a.click();
  URL.revokeObjectURL(url);
  $q.notify({ message: 'Settings exported', color: 'positive' });
}

// function onStorageProviderChange(val) {
//   StorageService.setProvider(val);
//   store.setAdvanced({ storageProvider: val });
//   $q.notify({ message: `Storage provider set to ${val}. Note: only localStorage is active by default.`, color: 'info' });
// }

function persist() {
  store.persist();
}

function notify(msg) {
  $q.notify({ message: msg, color: 'info' });
}

function confirmClear() {
  confirmClearDialog.value = true;
}

function doClearAll() {
  confirmClearDialog.value = false;
  store.clearAllData();
  // StorageService.remove('app_settings_v1');
  $q.notify({ message: 'All local settings cleared', color: 'positive' });
}

</script>

<style scoped>
/* Same helper classes as earlier */
.bg-dark-page { background-color: #1a1c22 !important; }
.bg-white-page { background-color: #f7f7f7 !important; }
.settings-header { transition: background-color 0.25s; }
.bg-dark-header { background-color: #121217 !important; }
.bg-light-header { background-color: #f7f7f7 !important; }
.text-dark-blue { color: #1a1c22 !important; }
.settings-list { box-shadow: 0 6px 18px rgba(0,0,0,0.08); transition: background-color 0.25s; }
.bg-dark-list { background-color: #2f343a !important; }
.bg-white-list { background-color: #ffffff !important; }
.list-icon { color: #6366f1; }
</style>
