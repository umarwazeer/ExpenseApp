<template>
  <div class="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex items-center justify-center p-4 font-sans">
    <div class="w-full max-w-md bg-white rounded-2xl shadow-xl p-8 space-y-6">
      <!-- Header -->
      <div class="text-center">
        <div class="mx-auto flex items-center justify-center w-16 h-16 bg-indigo-600 rounded-2xl shadow-md mb-4">
          <Landmark class="text-white w-8 h-8" />
        </div>
        <h1 class="text-3xl font-bold text-gray-900">DailyKhata</h1>
        <p class="text-gray-600 mt-2">
          {{ isRegister ? 'Create your account to get started' : 'Welcome back! Please sign in' }}
        </p>
      </div>

      <!-- Feedback Messages -->
      <div class="min-h-[2rem]">
        <div
          v-if="error"
          class="w-full p-3 rounded-lg text-sm bg-red-100 text-red-800"
        >
          {{ error }}
        </div>
        <div
          v-else-if="success"
          class="w-full p-3 rounded-lg text-sm bg-green-100 text-green-800"
        >
          {{ success }}
        </div>
      </div>

      <!-- Auth Form -->
      <form @submit.prevent="handleSubmit" class="space-y-4">
        <!-- Name fields for registration -->
        <div v-if="isRegister" class="flex flex-col sm:flex-row gap-2">
          <div class="relative w-full">
            <User class="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" />
            <input
              type="text"
              placeholder="First Name"
              v-model="formData.firstName"
              :disabled="isLoading"
              class="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 transition-colors duration-300"
            />
          </div>
          <div class="relative w-full">
            <User class="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" />
            <input
              type="text"
              placeholder="Last Name"
              v-model="formData.lastName"
              :disabled="isLoading"
              class="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 transition-colors duration-300"
            />
          </div>
        </div>

        <!-- Username -->
        <div class="relative">
          <User class="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" />
          <input
            type="text"
            placeholder="Username"
            v-model="formData.username"
            :disabled="isLoading"
            required
            class="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 transition-colors duration-300"
          />
        </div>

        <!-- Email for registration -->
        <div v-if="isRegister" class="relative">
          <Mail class="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" />
          <input
            type="email"
            placeholder="Email"
            v-model="formData.email"
            :disabled="isLoading"
            required
            class="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 transition-colors duration-300"
          />
        </div>

        <!-- Password field with eye toggle -->
        <div class="relative">
          <KeyRound class="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" />
          <input
            :type="showPassword ? 'text' : 'password'"
            placeholder="Password"
            v-model="formData.password"
            :disabled="isLoading"
            required
            class="w-full pl-10 pr-10 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 transition-colors duration-300"
          />
          <!-- Eye icon -->
          <button
            type="button"
            class="absolute right-3 top-1/2 -translate-y-1/2 text-gray-400"
            @click="showPassword = !showPassword"
          >
            <span v-if="showPassword">
              <EyeOff class="w-5 h-5" />
            </span>
            <span v-else>
              <Eye class="w-5 h-5" />
            </span>
          </button>
        </div>

        <!-- Submit Button -->
        <button
          type="submit"
          :disabled="isLoading"
          class="w-full flex justify-center items-center gap-2 bg-indigo-600 text-white font-bold py-3 px-4 rounded-lg hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 transition-colors duration-300 disabled:bg-indigo-400 disabled:cursor-not-allowed"
        >
          <LoaderCircle v-if="isLoading" class="animate-spin w-5 h-5" />
          <template v-else>
            <UserPlus v-if="isRegister" class="w-5 h-5" />
            <LogIn v-else class="w-5 h-5" />
          </template>
          {{ isLoading ? 'Processing...' : isRegister ? 'Sign Up' : 'Sign In' }}
        </button>
      </form>

      <!-- Toggle Button -->
      <div class="text-center mt-6">
        <button
          @click="toggleMode"
          class="text-sm text-indigo-600 hover:text-indigo-800 hover:underline focus:outline-none focus:ring-2 focus:ring-indigo-500 rounded-md p-1"
        >
          {{ isRegister ? 'Already have an account? Sign In' : "Don’t have an account? Sign Up" }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { Landmark, UserPlus, LogIn, Mail, User, KeyRound, LoaderCircle, Eye, EyeOff } from 'lucide-vue-next'
import { useAuthStore } from 'src/stores/auth'
import { useQuasar } from 'quasar'
import { useRouter } from 'vue-router'

const $q = useQuasar()
const auth = useAuthStore()

const isRegister = ref(false)
const isLoading = ref(false)
const error = ref(null)
const success = ref(null)
const showPassword = ref(false)  // 🔹 new reactive variable
const router = useRouter()
  
const formData = ref({
  firstName: '',
  lastName: '',
  username: '',
  email: '',
  password: ''
})

function toggleMode() {
  isRegister.value = !isRegister.value
  error.value = null
  success.value = null
  formData.value = {
    firstName: '',
    lastName: '',
    username: '',
    email: '',
    password: ''
  }
  showPassword.value = false
}

async function handleSubmit() {
  error.value = null
  success.value = null
  isLoading.value = true

  try {
    let response
    if (isRegister.value) {
      const userData = {
        first_name: formData.value.firstName,
        last_name: formData.value.lastName,
        username: formData.value.username,
        email: formData.value.email,      
        password: formData.value.password
      }
      response = await auth.register(userData)
      if (response.success) {
        success.value = 'Account created successfully! Redirecting...'
        $q.notify({ type: 'positive', message: 'Account created!' })
      } else {
        error.value = response.error || 'Registration failed.'
      }
    } else {
      const credentials = {
        username: formData.value.username,
        password: formData.value.password
      }
      response = await auth.login(credentials)
      if (response.success) {
        success.value = 'Login successful! Redirecting...'
        $q.notify({ type: 'positive', message: 'Login successful!' })
        router.push({ name: 'home' }) 
      } else {
        error.value = response.error || 'Invalid username or password.'
      }
    }
  } catch (err) {
    error.value = 'An unexpected error occurred.'
    console.error(err)
  } finally {
    isLoading.value = false
  }
}
</script>
