// src/stores/settings.js
import { defineStore } from 'pinia';
import { ref, reactive } from 'vue';
import StorageService from 'src/utils/storageService';

const STORAGE_KEY = 'app_settings_v1';

export const useSettingsStore = defineStore('settings', () => {
  // Basic profile
  const profile = reactive({
    name: 'Olivia',
    email: '',
    avatarBase64: null, // base64 data URL
  });

  // App settings
  const ui = reactive({
    darkMode: false,
    accentColor: '#6366f1', // indigo default
    language: 'en',
    currency: 'USD',
    sound: true,
    haptics: true,
  });

  // Advanced settings
  const advanced = reactive({
    appLockEnabled: false,
    appLockPIN: null, // hashed in future; stored plain for demo — replace with proper secure store
    notifications: {
      enabled: true,
      dailySummary: false,
    },
    autoBackup: {
      enabled: false,
      schedule: 'daily', // daily|weekly|monthly
    },
    storageProvider: 'local' // local | pinia | supabase | firebase | vuex
  });

  // helper loads
  function load() {
    const raw = StorageService.get(STORAGE_KEY);
    if (raw) {
      try {
        const parsed = JSON.parse(raw);
        Object.assign(profile, parsed.profile ?? {});
        Object.assign(ui, parsed.ui ?? {});
        Object.assign(advanced, parsed.advanced ?? {});
      } catch (err) {
        console.error('Failed to parse settings from storage', err);
      }
    }
  }

  function persist() {
    const payload = JSON.stringify({ profile, ui, advanced });
    StorageService.set(STORAGE_KEY, payload);
  }

  // Profile helpers
  function setProfile({ name, email, avatarBase64 }) {
    if (name !== undefined) profile.name = name;
    if (email !== undefined) profile.email = email;
    if (avatarBase64 !== undefined) profile.avatarBase64 = avatarBase64;
    persist();
  }

  function setUI(partial) {
    Object.assign(ui, partial);
    persist();
  }

  function setAdvanced(partial) {
    Object.assign(advanced, partial);
    persist();
  }

  function setPIN(pin) {
    // NOTE: for production, DO NOT store raw PIN. Hash it and store in secure storage.
    advanced.appLockPIN = pin;
    persist();
  }

  function clearAllData() {
    profile.name = '';
    profile.email = '';
    profile.avatarBase64 = null;
    Object.assign(ui, {
      darkMode: false,
      accentColor: '#6366f1',
      language: 'en',
      currency: 'USD',
      sound: true,
      haptics: true,
    });
    Object.assign(advanced, {
      appLockEnabled: false,
      appLockPIN: null,
      notifications: { enabled: true, dailySummary: false },
      autoBackup: { enabled: false, schedule: 'daily' },
      storageProvider: 'local'
    });
    StorageService.remove(STORAGE_KEY);
  }

  // initialize
  load();

  // subscribe to changes when store used in components (you can call persist manually too)
  // For simplicity we won't add reactive watchers here; call persist when mutating.

  return {
    profile,
    ui,
    advanced,
    load,
    persist,
    setProfile,
    setUI,
    setAdvanced,
    setPIN,
    clearAllData
  };
});
