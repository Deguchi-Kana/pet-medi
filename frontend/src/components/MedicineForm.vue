<template>
  <div class="p-4 max-w-md mx-auto space-y-4">
    <form @submit.prevent="submitForm" class="space-y-2">
      <div>
        <input v-model="form.name" placeholder="薬名" class="border w-full p-1" />
      </div>
      <div>
        <select v-model="form.dosage" class="border w-full p-1">
          <option disabled value="">分量を選択</option>
          <option>1錠</option>
          <option>1/2錠</option>
          <option>1包</option>
        </select>
      </div>
      <div>
        <label><input type="checkbox" v-model="form.timing" value="朝" /> 朝</label>
        <label><input type="checkbox" v-model="form.timing" value="昼" /> 昼</label>
        <label><input type="checkbox" v-model="form.timing" value="夜" /> 夜</label>
      </div>
      <div>
        <label><input type="checkbox" v-model="form.notify" /> 通知ON</label>
      </div>
      <button type="submit" class="bg-blue-500 text-white px-4 py-1">登録</button>
    </form>

    <!-- 一覧表示 -->
    <div v-if="medicines.length > 0" class="mt-6">
      <h2 class="text-lg font-semibold">登録済みのお薬</h2>
      <ul class="space-y-2 mt-2">
        <li v-for="(m, index) in medicines" :key="index" class="border p-2 rounded">
          <div><strong>薬名:</strong> {{ m.name }}</div>
          <div><strong>分量:</strong> {{ m.dosage }}</div>
          <div><strong>タイミング:</strong> {{ m.timing.join(', ') }}</div>
          <div><strong>通知:</strong> {{ m.notify ? 'ON' : 'OFF' }}</div>
        </li>
      </ul>
    </div>
  </div>
</template>

<script setup>
import {onMounted, ref} from 'vue'

const form = ref({
  name: '',
  dosage: '',
  pet_id: 1,
  timing: [],
  notify: false
})

const medicines = ref([])

// 薬の一覧取得
const fetchMedicines = async () => {
  const response = await fetch('http://localhost:8000/medicines')
  medicines.value = await response.json()
}

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

onMounted(() => {
  fetchMedicines()
})

</script>
