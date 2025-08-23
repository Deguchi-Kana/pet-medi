<template>
  <div class="medicine-container">
    <!-- ヘッダー -->
    <div class="list-header">
      <div class="header-info">
        <h4 class="list-title">薬一覧</h4>
        <span class="medicine-count">{{ medicines.length }}種類</span>
      </div>
      <button @click="showAddMedicineModal = true" class="add-btn">
        <span class="add-icon">➕</span>
        追加
      </button>
    </div>

    <!-- 薬一覧 -->
    <div v-if="medicines.length > 0" class="medicines-grid">
      <div v-for="(medicine, index) in medicines" :key="index" class="medicine-card">
        <div class="medicine-icon">
          <span class="medicine-emoji">💊</span>
        </div>
        <div class="medicine-info">
          <h5 class="medicine-name">{{ medicine.name }}</h5>
          <div class="medicine-details">
            <span class="medicine-dosage">{{ medicine.dosage }}</span>
            <div class="medicine-timing">
              <span class="timing-label">タイミング:</span>
              <div class="timing-tags">
                <span v-for="time in medicine.timing" :key="time" class="timing-tag">
                  {{ time }}
                </span>
              </div>
            </div>
            <span class="medicine-notify" :class="{ 'notify-on': medicine.notify, 'notify-off': !medicine.notify }">
              {{ medicine.notify ? '通知ON' : '通知OFF' }}
            </span>
          </div>
        </div>
        <div class="medicine-actions">
          <button @click="editMedicine(medicine)" class="action-btn edit-btn" title="編集">
            <span class="action-icon">✏️</span>
          </button>
          <button @click="deleteMedicine(medicine.id)" class="action-btn delete-btn" title="削除">
            <span class="action-icon">🗑️</span>
          </button>
        </div>
      </div>
    </div>

    <!-- 空の状態 -->
    <div v-else class="empty-state">
      <div class="empty-icon">💊</div>
      <h5 class="empty-title">薬が登録されていません</h5>
      <p class="empty-description">新しい薬を追加して、投薬管理を始めましょう</p>
      <button @click="showAddMedicineModal = true" class="empty-action-btn">
        薬を追加
      </button>
    </div>

    <!-- 編集モーダル -->
    <edit-medicine-modal
      v-if="showModal"
      :visible="showModal"
      :medicine="selectedMedicine"
      @close="closeModal"
      @update="updateMedicine"
    />

    <!-- 追加モーダル（簡易版） -->
    <div v-if="showAddMedicineModal" class="modal-overlay" @click="showAddMedicineModal = false">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h4>新しい薬を追加</h4>
          <button @click="showAddMedicineModal = false" class="close-btn">✕</button>
        </div>
        <div class="modal-body">
          <p>薬の追加機能は準備中です。登録画面から追加してください。</p>
        </div>
        <div class="modal-footer">
          <button @click="showAddMedicineModal = false" class="btn btn-primary">閉じる</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import EditMedicineModal from './EditMedicineModal.vue'

const medicines = ref([])
const showModal = ref(false)
const showAddMedicineModal = ref(false)
const selectedMedicine = ref(null)

// 薬の一覧取得
const fetchMedicines = async () => {
  try {
    const response = await fetch('http://localhost:8000/medicines')
    if (response.ok) {
      medicines.value = await response.json()
    }
  } catch (error) {
    console.error('薬の取得に失敗しました:', error)
  }
}

onMounted(fetchMedicines)

// 薬の削除
const deleteMedicine = async (id) => {
  if (!confirm('この薬を削除しますか？')) return
  
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
@import '../styles/MedicineList.scss';
</style>