<template>
  <div class="medicine-container">
    <div class="p-4 max-w-md mx-auto space-y-4">
    </div>
      <form @submit.prevent="submitForm" class="space-y-2">
        <h2 class="text-lg font-semibold">お薬情報の登録</h2>
        <div>
          <input v-model="form.name" placeholder="薬名" class="border w-full p-1" />
        </div>
        <div>
          <select v-model="form.dosage" class="border w-full p-1">
            <option disabled value="">分量を選択</option>
            <option>1錠</option>
            <option>1/2錠</option>
            <option>1/3錠</option>
            <option>1/4錠</option>
            <option>1包</option>
          </select>
        </div>
        <div class="timing-checkboxes">
          <label><input type="checkbox" v-model="form.timing" value="朝" /> 朝</label>
          <label><input type="checkbox" v-model="form.timing" value="昼" /> 昼</label>
          <label><input type="checkbox" v-model="form.timing" value="夜" /> 夜</label>
        </div>
        <div>
          <label>ペット</label>
          <select v-model="form.pet_id" required>
            <option disabled value="">ペットを選択</option>
            <option v-for="pet in pets" :key="pet.id" :value="pet.id">
              {{ pet.name }}
            </option>
          </select>
        </div>
        <div>
          <label><input type="checkbox" v-model="form.notify" /> 通知ON</label>
        </div>
        <div>
          <label for="start-date">開始日</label>
          <input type="date" id="start-date" v-model="form.start_date" />
        </div>
        <div>
          <input type="number" id="duration" placeholder="日数" v-model="form.duration_days" />日分
        </div>
        <button type="submit" class="bg-blue-500 text-white px-4 py-1">登録</button>
      </form>
  </div>
</template>

<script setup>
import {ref} from 'vue'

const form = ref({
  name: '',
  dosage: '',
  pet_id: '',
  timing: [],
  notify: false,
  start_date: '',
  duration_days: '',
})

// ペット情報の取得
const pets = ref([])
const fetchPets = async () => {
  try {
    const response = await fetch('http://localhost:8000/pets')
    pets.value = await response.json()
  } catch (error) {
    console.error(error)
  }
}
fetchPets()

// 薬の登録
const submitForm = async () => {
  try {
    const response = await fetch('http://localhost:8000/medicines', {
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
@import '../styles/medicine.scss';
</style>