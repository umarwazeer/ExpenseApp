<template>
  <q-form @submit.prevent="submit" class="q-gutter-md">
    <q-input filled :dark="$q.dark.isActive" v-model="form.name" label="Full name" :rules="[val => !!val || 'Required']" />
    <q-input filled :dark="$q.dark.isActive" v-model="form.email" label="Email" type="email" :rules="[emailRule]" />
    <div class="row items-center q-gutter-sm">
      <q-btn label="Save" color="indigo" type="submit" />
    </div>
  </q-form>
</template>

<script setup>
import { reactive, toRefs } from 'vue';
import { useSettingsStore } from 'src/stores/settings';
const store = useSettingsStore();

const form = reactive({
  name: store.profile.name || '',
  email: store.profile.email || ''
});

function emailRule(val) {
  if (!val) return true;
  // simple email check
  return /^\S+@\S+\.\S+$/.test(val) || 'Invalid email';
}

function submit() {
  store.setProfile({ name: form.name, email: form.email });
  // emit save event to parent
  const { emit } = defineEmits(['save']);
  emit('save', { name: form.name, email: form.email });
}
</script>
