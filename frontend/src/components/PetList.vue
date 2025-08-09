<template>
  <div class="pet-container">
    <div v-if="pets.length > 0" class="mt-6">
      <h2 class="text-lg font-semibold">登録済みのペット</h2>
      <ul class="space-y-2 mt-2">
        <li v-for="(pet, index) in pets" :key="index" class="border p-2 rounded">
          <div><strong>ID:</strong> {{ pet.id }}</div>
          <div><strong>名前:</strong> {{ pet.name }}</div>
          <div><strong>種類:</strong> {{ pet.species }}</div>
          <div><strong>誕生日:</strong> {{ pet.birthdate }}</div>
          <button @click="editPet(pet)" class="button-orange">編集</button>
          <button @click="deletePet(pet.id)" class="button-red">削除</button>
        </li>
      </ul>
    </div>
  </div>

  <edit-pet-modal
      v-if="showModal"
      :visible="showModal"
      :pet="selectedPet"
      @close="closeModal"
      @update="updatePet"
  />
</template>

<script setup>
import { ref, onMounted } from 'vue'
import EditPetModal from "./EditPetModal.vue";

const pets = ref([])
const showModal = ref(false)
const selectedPet = ref(null)

// ペットの一覧取得
const fetchPets = async () => {
  const response = await fetch('http://localhost:8000/pets')
  pets.value = await response.json()
}

onMounted(fetchPets)

// ペットの削除
const deletePet = async (id) =>
{
  try {
    const response = await fetch(`http://localhost:8000/pets/${id}`, {
      method: 'DELETE'
    })
    if (!response.ok) throw new Error('削除に失敗しました')
    await response.json();
    alert('削除が完了しました！')
    await fetchPets()
  } catch (error) {
    console.error(error)
    alert('削除に失敗しました')
  }
}

// ペットの編集モーダル表示
const editPet = (pet) => {
  selectedPet.value = { ...pet }
  showModal.value = true
}
// ペットの編集モーダル非表示
const closeModal = () => {
  showModal.value = false
}

// ペットの情報更新
const updatePet = async (updated) => {
  try {
    const response = await fetch(`http://localhost:8000/pets/${updated.id}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(updated)
    })
    if (!response.ok) throw new Error('更新に失敗しました')
    alert('更新が完了しました！')
    showModal.value = false
    await fetchPets()
  } catch (error) {
    console.error(error)
    alert('更新に失敗しました')
  }
}
</script>

<style scoped>
@import '../styles/pet.scss';
</style>