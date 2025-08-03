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
          <button @click="editMedicine(m)" class="button-orange">編集</button>
          <button @click="deleteMedicine(m.id)" class="button-red">削除</button>
        </li>
      </ul>
    </div>
  </div>

  <edit-medicine-modal
      v-if="showModal"
      :visible="showModal"
      :medicine="selectedMedicine"
      @close="closeModal"
      @update="updateMedicine"
  />
</template>

<script setup>
import { ref, onMounted } from 'vue'
import EditMedicineModal from './EditMedicineModal.vue'

const medicines = ref([])
const showModal = ref(false)
const selectedMedicine = ref(null)

// 薬の一覧取得
const fetchMedicines = async () => {
  const response = await fetch('http://localhost:8000/medicines')
  medicines.value = await response.json()
}

onMounted(fetchMedicines)

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
    await fetchMedicines()
  } catch (error) {
    console.error(error)
    alert('削除に失敗しました')
  }
}

// 薬の編集モーダル表示
const editMedicine = (medicine) => {
  selectedMedicine.value = { ...medicine }
  showModal.value = true
}
// 薬の編集モーダル非表示
const closeModal = () => {
  showModal.value = false
}

// 薬の情報更新
const updateMedicine = async (updated) => {
  try {
    const response = await fetch(`http://localhost:8000/medicines/${updated.id}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(updated)
    })
    if (!response.ok) throw new Error('更新に失敗しました')
    alert('更新が完了しました！')
    showModal.value = false
    await fetchMedicines()
  } catch (error) {
    console.error(error)
    alert('更新に失敗しました')
  }
}
</script>

<style scoped>
@import '../styles/medicine.scss';
</style>