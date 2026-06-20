// src/utils/storageService.js
// Simple storage abstraction. Default: localStorage.
// Extend this file to add supabase/firebase calls.

const localImpl = {
  get(key) {
    try {
      return localStorage.getItem(key);
    } catch (err) {
      console.warn('localStorage.get failed', err);
      return null;
    }
  },
  set(key, value) {
    try {
      localStorage.setItem(key, value);
    } catch (err) {
      console.warn('localStorage.set failed', err);
    }
  },
  remove(key) {
    try {
      localStorage.removeItem(key);
    } catch (err) {
      console.warn('localStorage.remove failed', err);
    }
  }
};

// Placeholder stubs for other providers
const stubbedRemoteImpl = {
  get(/*key*/) { return null; },
  set(/*key, value*/) { /* no-op */ },
  remove(/*key*/) { /* no-op */ }
};

// Exported API chooses impl based on an in-memory provider; you can wire this to Pinia advanced.storageProvider
let provider = 'local'; // default
let impl = localImpl;

export default {
  setProvider(newProvider) {
    provider = newProvider;
    if (provider === 'local') impl = localImpl;
    else {
      // For now, keep using localImpl but you can replace impl with remote ones.
      impl = stubbedRemoteImpl;
    }
  },
  get(key) { return impl.get(key); },
  set(key, value) { impl.set(key, value); },
  remove(key) { impl.remove(key); }
};
