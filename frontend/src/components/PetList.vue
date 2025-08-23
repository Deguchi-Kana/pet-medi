<template>
  <div class="pet-container">
    <!-- ヘッダー -->
    <div class="list-header">
      <div class="header-info">
        <h4 class="list-title">ペット一覧</h4>
        <span class="pet-count">{{ pets.length }}匹</span>
      </div>
      <button @click="showAddPetModal = true" class="add-btn">
        <span class="add-icon">➕</span>
        追加
      </button>
    </div>

    <!-- ペット一覧 -->
    <div v-if="pets.length > 0" class="pets-grid">
      <div v-for="(pet, index) in pets" :key="index" class="pet-card">
        <div class="pet-avatar">
          <span class="pet-emoji">{{ getPetEmoji(pet.species) }}</span>
        </div>
        <div class="pet-info">
          <h5 class="pet-name">{{ pet.name }}</h5>
          <div class="pet-details">
            <span class="pet-species">{{ pet.species }}</span>
            <span class="pet-birthdate">{{ formatDate(pet.birthdate) }}</span>
          </div>
        </div>
        <div class="pet-actions">
          <button @click="editPet(pet)" class="action-btn edit-btn" title="編集">
            <span class="action-icon">✏️</span>
          </button>
          <button @click="deletePet(pet.id)" class="action-btn delete-btn" title="削除">
            <span class="action-icon">🗑️</span>
          </button>
        </div>
      </div>
    </div>

    <!-- 空の状態 -->
    <div v-else class="empty-state">
      <div class="empty-icon">🐾</div>
      <h5 class="empty-title">ペットが登録されていません</h5>
      <p class="empty-description">新しいペットを追加して、投薬管理を始めましょう</p>
      <button @click="showAddPetModal = true" class="empty-action-btn">
        ペットを追加
      </button>
    </div>

    <!-- 編集モーダル -->
    <edit-pet-modal
      v-if="showModal"
      :visible="showModal"
      :pet="selectedPet"
      @close="closeModal"
      @update="updatePet"
    />

    <!-- 追加モーダル（簡易版） -->
    <div v-if="showAddPetModal" class="modal-overlay" @click="showAddPetModal = false">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h4>新しいペットを追加</h4>
          <button @click="showAddPetModal = false" class="close-btn">✕</button>
        </div>
        <div class="modal-body">
          <p>ペットの追加機能は準備中です。登録画面から追加してください。</p>
        </div>
        <div class="modal-footer">
          <button @click="showAddPetModal = false" class="btn btn-primary">閉じる</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import EditPetModal from "./EditPetModal.vue";

const pets = ref([])
const showModal = ref(false)
const showAddPetModal = ref(false)
const selectedPet = ref(null)

// ペットの一覧取得
const fetchPets = async () => {
  try {
    const response = await fetch('http://localhost:8000/pets')
    if (response.ok) {
      pets.value = await response.json()
    }
  } catch (error) {
    console.error('ペットの取得に失敗しました:', error)
  }
}

onMounted(fetchPets)

// ペットの削除
const deletePet = async (id) => {
  if (!confirm('このペットを削除しますか？')) return
  
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

// ペットの種類に応じた絵文字を取得
const getPetEmoji = (species) => {
  const emojiMap = {
    'dog': '🐕',
    'cat': '🐱',
    'bird': '🐦',
    'rabbit': '🐰',
    'hamster': '🐹',
    'fish': '🐠',
    'turtle': '🐢',
    'snake': '🐍'
  }
  return emojiMap[species.toLowerCase()] || '🐾'
}

// 日付をフォーマット
const formatDate = (dateString) => {
  if (!dateString) return '不明'
  const date = new Date(dateString)
  return date.toLocaleDateString('ja-JP')
}
</script>

<style scoped>
@import '../styles/PetList.scss';
</style>