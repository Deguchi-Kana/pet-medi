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
.medicine-container {
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

.medicine-count {
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

.medicines-grid {
  display: grid;
  gap: var(--spacing-4);
}

.medicine-card {
  display: flex;
  align-items: center;
  gap: var(--spacing-4);
  background: var(--white);
  padding: var(--spacing-4);
  border-radius: var(--radius-lg);
  border: 1px solid var(--gray-200);
  transition: var(--transition);
}

.medicine-card:hover {
  border-color: var(--primary-green);
  box-shadow: var(--shadow-md);
  transform: translateY(-1px);
}

.medicine-icon {
  width: 60px;
  height: 60px;
  background: linear-gradient(135deg, var(--accent-green) 0%, var(--secondary-green) 100%);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.medicine-emoji {
  font-size: 2rem;
}

.medicine-info {
  flex: 1;
  min-width: 0;
}

.medicine-name {
  color: var(--gray-800);
  margin: 0 0 var(--spacing-2) 0;
  font-size: var(--font-size-lg);
  font-weight: 600;
}

.medicine-details {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-2);
  font-size: var(--font-size-sm);
  color: var(--gray-600);
}

.medicine-dosage {
  background: var(--gray-100);
  padding: var(--spacing-1) var(--spacing-2);
  border-radius: var(--radius);
  display: inline-block;
  width: fit-content;
}

.medicine-timing {
  display: flex;
  align-items: center;
  gap: var(--spacing-2);
}

.timing-label {
  color: var(--gray-500);
  font-size: var(--font-size-xs);
}

.timing-tags {
  display: flex;
  gap: var(--spacing-1);
  flex-wrap: wrap;
}

.timing-tag {
  background: var(--primary-green-light);
  color: var(--primary-green-dark);
  padding: var(--spacing-1) var(--spacing-2);
  border-radius: var(--radius);
  font-size: var(--font-size-xs);
  font-weight: 500;
}

.medicine-notify {
  padding: var(--spacing-1) var(--spacing-2);
  border-radius: var(--radius);
  font-size: var(--font-size-xs);
  font-weight: 500;
  width: fit-content;
}

.notify-on {
  background: var(--success);
  color: var(--white);
}

.notify-off {
  background: var(--gray-200);
  color: var(--gray-600);
}

.medicine-actions {
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

  .medicine-card {
    flex-direction: column;
    text-align: center;
    gap: var(--spacing-3);
  }

  .medicine-actions {
    justify-content: center;
  }

  .medicine-details {
    align-items: center;
  }

  .medicine-timing {
    flex-direction: column;
    gap: var(--spacing-1);
  }
}
</style>