<template>
  <div class="pet-container">
    <div class="p-4 max-w-md mx-auto space-y-4">
    </div>
      <form @submit.prevent="submitForm" class="space-y-2">
        <h2 class="text-lg font-semibold">ペット情報の登録</h2>
        <div>
          <input v-model="form.name" placeholder="名前" class="border w-full p-1" />
        </div>
        <div>
          <input v-model="form.species" placeholder="種類" class="border w-full p-1" />
        </div>
        <div>
          <label for="birthdate">誕生日</label>
          <input type="date" id="birthdate" v-model="form.birthdate" />
        </div>
        <button type="submit" class="bg-blue-500 text-white px-4 py-1">登録</button>
      </form>
  </div>
</template>

<script setup>
import {ref} from 'vue'

const form = ref({
  name: '',
  species: '',
  birthdate: '',
})

// ペットの登録
const submitForm = async () => {
  try {
    const response = await fetch('http://localhost:8000/pets', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(form.value)
    })

    if (!response.ok) throw new Error('登録に失敗しました')

    const data = await response.json()
    console.log('登録成功:', data)
    alert('登録が完了しました！')
  } catch (error) {
    console.error(error)
    alert('登録に失敗しました')
  }
}
</script>

<style scoped>
@import '../styles/pet.scss';
</style>