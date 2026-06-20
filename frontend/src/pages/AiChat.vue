<template>
  <div class="fixed inset-0 bg-black/40 z-50 flex justify-end">
    <div class="w-full max-w-md h-full bg-white flex flex-col rounded-l-2xl overflow-hidden">

      <!-- HEADER -->
      <div class="bg-gradient-to-r from-purple-600 to-violet-600 p-4 flex items-center justify-between">
        <div>
          <h2 class="text-white font-semibold text-lg">AI Financial Assistant</h2>
          <p class="text-xs text-white/70">Powered by AI</p>
        </div>
        <button @click="$router.back()" class="text-white text-xl">×</button>
      </div>

      <!-- CHAT WINDOW -->
      <ChatWindow :messages="messages" class="flex-1" />

      <!-- QUICK QUESTIONS -->
      <div class="px-3 py-2 border-t bg-gray-50 flex gap-2 overflow-x-auto">
        <button
          v-for="q in quickQuestions"
          :key="q"
          @click="sendQuick(q)"
          class="px-3 py-1 text-xs rounded-full border bg-white whitespace-nowrap"
        >
          {{ q }}
        </button>
      </div>

      <!-- INPUT (FIXED BOTTOM) -->
      <ChatInput @send="handleSend" />

    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";
import ChatWindow from "../pages/components/chat/ChatWindow.vue";
import ChatInput from "../pages/components/chat/ChatInput.vue";


const messages = ref([
  {
    role: "assistant",
    content:
      "Hi! 👋 I'm your AI Financial Assistant. Ask me anything about your spending, savings, or budget. I'll analyze your data and provide personalized insights!",
  },
]);

const quickQuestions = [
  "Why is my expense high?",
  "Show spending categories",
  "How can I save money?",
];

const mockAI = (text) => {
  const q = text.toLowerCase();

  if (q.includes("category")) {
    return `Here's your spending breakdown:

🛍️ **Shopping**: ₹12,000 (48%)
🍔 **Food**: ₹8,000 (32%)
💡 **Bills**: ₹6,000 (24%)
🚗 **Transport**: ₹5,000 (20%)
🎬 **Entertainment**: ₹3,000 (12%)`;
  }

  if (q.includes("expense")) {
    return "📊 Your expenses are high mainly due to shopping and food this month.";
  }

  if (q.includes("save")) {
    return "💡 Reduce shopping by 30% and cook at home to save ₹7,000/month.";
  }

  return "🤖 Ask me about expenses, savings, or budget!";
};

const handleSend = (text) => {
  messages.value.push({ role: "user", content: text });

  setTimeout(() => {
    messages.value.push({
      role: "assistant",
      content: mockAI(text),
    });
  }, 700);
};

const sendQuick = (q) => handleSend(q);
</script>
