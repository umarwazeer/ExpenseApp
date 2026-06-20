<!-- src/pages/components/settings/ChangePasswordForm.vue -->
<template>
  <q-form @submit.prevent="onSubmit" class="q-gutter-md">
    <q-input filled :dark="dark" v-model="oldPass" label="Old password" type="password" />
    <q-input filled :dark="dark" v-model="newPass" label="New password" type="password" />
    <q-input filled :dark="dark" v-model="confirmPass" label="Confirm password" type="password" />
    <div>
      <q-btn label="Change" color="indigo" type="submit" />
    </div>
  </q-form>
</template>

<script setup>
const props = defineProps({ dark: { type: Boolean, default: false } });
const emit = defineEmits(['submit']);
import { ref } from 'vue';
const oldPass = ref('');
const newPass = ref('');
const confirmPass = ref('');

function onSubmit() {
  if (newPass.value !== confirmPass.value) {
    // prefer to use Quasar notify from parent; emit an error
    alert('Passwords do not match'); // simple fallback
    return;
  }
  // Hook in real auth backend here
  emit('submit');
}   
</script>
