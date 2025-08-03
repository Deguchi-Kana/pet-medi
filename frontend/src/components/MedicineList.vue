<template>
  <div class="medicine-container">
    <div v-if="medicines.length > 0" class="mt-6">
      <h2 class="text-lg font-semibold">登録済みのお薬</h2>
      <ul class="space-y-2 mt-2">
        <li v-for="(m, index) in medicines" :key="index" class="border p-2 rounded">
          <div><strong>薬名:</strong> {{ m.name }}</div>
          <div><strong>分量:</strong> {{ m.dosage }}</div>
          <div><strong>タイミング:</strong> {{ m.timing.join(', ') }}</div>
          <div><strong>通知:</strong> {{ m.notify ? 'ON' : 'OFF' }}</div>
          <button @click="editMedicine(m.id)" class="button-orange">編集</button>
          <button @click="deleteMedicine(m.id)" class="button-red">削除</button>
        </li>
      </ul>
    </div>
  </div>
</template>

<script setup>
import {onMounted, ref} from 'vue'
ref({
  name: '',
  dosage: '',
  pet_id: 1,
  timing: [],
  notify: false
});
const medicines = ref([])

onMounted(() => {
  fetchMedicines()
})

// 薬の一覧取得
const fetchMedicines = async () => {
  const response = await fetch('http://localhost:8000/medicines')
  medicines.value = await response.json()
}

// 薬の削除
const deleteMedicine = async (id) =>
{
  try {
    const response = await fetch(`http://localhost:8000/medicines/${id}`, {
      method: 'DELETE'
    })
    if (!response.ok) throw new Error('削除に失敗しました')
    await response.json();
    alert('削除が完了しました！')
  } catch (error) {
    console.error(error)
    alert('削除に失敗しました')
  }
}
</script>


<style scoped>
@import '../styles/medicine.scss';
</style>