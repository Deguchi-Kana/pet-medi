<template>
  <div class="ai-chat-container">
    <div class="chat-header">
      <h2>AIチャット</h2>
      <label class="toggle">
        <input type="checkbox" v-model="enabled" />
        <span class="slider"></span>
      </label>
    </div>

    <div class="chat-window">
      <div v-for="(msg, index) in displayedMessages" :key="index"
           :class="['chat-bubble', msg.role]">
        <p>{{ msg.content }}</p>
      </div>
      <div v-if="loading" class="chat-bubble ai loading">...</div>
    </div>

    <form @submit.prevent="sendMessage">
      <textarea
          v-model="userMessage"
          placeholder="メッセージを入力（Cmd/Ctrl + Enterで送信）"
          @keydown.enter.prevent="handleEnter($event)"
      ></textarea>
      <button type="submit" :disabled="!enabled || loading">送信</button>
    </form>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

const enabled = ref(false)
const loading = ref(false)
const userMessage = ref('')
const messages = ref([])

// 最新10件だけ表示
const displayedMessages = computed(() => messages.value.slice(-10))

// openaiに送信
const sendMessage = async () => {
  if (!userMessage.value.trim() || !enabled.value) return
  messages.value.push({ role: 'user', content: userMessage.value })
  const text = userMessage.value
  userMessage.value = ''
  loading.value = true

  if (enabled.value) {
    try {
      const res = await fetch('http://localhost:8000/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: text })
      })
      const data = await res.json()
      messages.value.push({ role: 'ai', content: data.reply })
    } catch (e) {
      messages.value.push({ role: 'ai', content: 'エラーが発生しました。' })
    } finally {
      loading.value = false
    }
  } else {
    // モック
    setTimeout(() => {
      messages.value.push({ role: 'ai', content: `受け取ったメッセージ: ${text}` })
      loading.value = false
    }, 500)
  }
}

// ctrl+Enterで送信
const handleEnter = (e) => {
  if ((e.metaKey || e.ctrlKey) && !loading.value) {
    sendMessage()
  }
}
</script>

<style lang="scss" scoped>
@import '../styles/AiChat.scss';
</style>
