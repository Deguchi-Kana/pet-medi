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
.pet-container {
  width: 100%;
}

.list-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--spacing-6);
}

.header-info {
  display: flex;
  align-items: center;
  gap: var(--spacing-3);
}

.list-title {
  color: var(--gray-800);
  margin: 0;
  font-size: var(--font-size-lg);
}

.pet-count {
  background: var(--primary-green);
  color: var(--white);
  padding: var(--spacing-1) var(--spacing-3);
  border-radius: var(--radius-xl);
  font-size: var(--font-size-sm);
  font-weight: 500;
}

.add-btn {
  display: flex;
  align-items: center;
  gap: var(--spacing-2);
  background: var(--primary-green);
  color: var(--white);
  border: none;
  padding: var(--spacing-2) var(--spacing-4);
  border-radius: var(--radius);
  cursor: pointer;
  font-weight: 500;
  transition: var(--transition);
}

.add-btn:hover {
  background: var(--primary-green-dark);
  transform: translateY(-1px);
}

.add-icon {
  font-size: var(--font-size-sm);
}

.pets-grid {
  display: grid;
  gap: var(--spacing-4);
}

.pet-card {
  display: flex;
  align-items: center;
  gap: var(--spacing-4);
  background: var(--white);
  padding: var(--spacing-4);
  border-radius: var(--radius-lg);
  border: 1px solid var(--gray-200);
  transition: var(--transition);
}

.pet-card:hover {
  border-color: var(--primary-green);
  box-shadow: var(--shadow-md);
  transform: translateY(-1px);
}

.pet-avatar {
  width: 60px;
  height: 60px;
  background: linear-gradient(135deg, var(--accent-green) 0%, var(--secondary-green) 100%);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.pet-emoji {
  font-size: 2rem;
}

.pet-info {
  flex: 1;
  min-width: 0;
}

.pet-name {
  color: var(--gray-800);
  margin: 0 0 var(--spacing-2) 0;
  font-size: var(--font-size-lg);
  font-weight: 600;
}

.pet-details {
  display: flex;
  gap: var(--spacing-4);
  font-size: var(--font-size-sm);
  color: var(--gray-600);
}

.pet-species {
  background: var(--gray-100);
  padding: var(--spacing-1) var(--spacing-2);
  border-radius: var(--radius);
}

.pet-birthdate {
  color: var(--gray-500);
}

.pet-actions {
  display: flex;
  gap: var(--spacing-2);
  flex-shrink: 0;
}

.action-btn {
  width: 40px;
  height: 40px;
  border: none;
  border-radius: var(--radius);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: var(--transition);
}

.edit-btn {
  background: var(--warning);
  color: var(--white);
}

.edit-btn:hover {
  background: #d97706;
  transform: scale(1.05);
}

.delete-btn {
  background: var(--error);
  color: var(--white);
}

.delete-btn:hover {
  background: #dc2626;
  transform: scale(1.05);
}

.action-icon {
  font-size: var(--font-size-sm);
}

.empty-state {
  text-align: center;
  padding: var(--spacing-12);
  color: var(--gray-500);
}

.empty-icon {
  font-size: 4rem;
  margin-bottom: var(--spacing-4);
}

.empty-title {
  color: var(--gray-600);
  margin-bottom: var(--spacing-2);
  font-size: var(--font-size-lg);
}

.empty-description {
  margin-bottom: var(--spacing-6);
  line-height: 1.6;
}

.empty-action-btn {
  background: var(--primary-green);
  color: var(--white);
  border: none;
  padding: var(--spacing-3) var(--spacing-6);
  border-radius: var(--radius);
  cursor: pointer;
  font-weight: 500;
  transition: var(--transition);
}

.empty-action-btn:hover {
  background: var(--primary-green-dark);
  transform: translateY(-1px);
}

/* モーダルスタイル */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-content {
  background: var(--white);
  border-radius: var(--radius-lg);
  max-width: 500px;
  width: 90%;
  max-height: 90vh;
  overflow-y: auto;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: var(--spacing-6);
  border-bottom: 1px solid var(--gray-200);
}

.modal-header h4 {
  margin: 0;
  color: var(--gray-800);
}

.close-btn {
  background: none;
  border: none;
  font-size: var(--font-size-xl);
  cursor: pointer;
  color: var(--gray-500);
  padding: var(--spacing-1);
}

.close-btn:hover {
  color: var(--gray-700);
}

.modal-body {
  padding: var(--spacing-6);
}

.modal-footer {
  padding: var(--spacing-4) var(--spacing-6);
  border-top: 1px solid var(--gray-200);
  display: flex;
  justify-content: flex-end;
  gap: var(--spacing-3);
}

/* レスポンシブデザイン */
@media (max-width: 768px) {
  .list-header {
    flex-direction: column;
    gap: var(--spacing-4);
    align-items: stretch;
  }

  .add-btn {
    justify-content: center;
  }

  .pet-card {
    flex-direction: column;
    text-align: center;
    gap: var(--spacing-3);
  }

  .pet-actions {
    justify-content: center;
  }

  .pet-details {
    flex-direction: column;
    gap: var(--spacing-2);
    align-items: center;
  }
}
</style>