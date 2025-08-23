<script setup>
import { ref } from 'vue'
import MedicineForm from "../components/MedicineForm.vue";
import PetForm from "../components/PetForm.vue";

const activeTab = ref('pet')
const showSuccessMessage = ref(false)

// 登録完了時の処理
const handleRegistrationSuccess = () => {
  showSuccessMessage.value = true
  // 3秒後に自動で非表示
  setTimeout(() => {
    showSuccessMessage.value = false
  }, 5000)
}

// コンポーネントにイベントリスナーを追加
// 実際の実装では、各フォームコンポーネントからイベントを発火させる
</script>

<template>
  <div class="register-container fade-in">
    <!-- ヘッダー -->
    <section class="register-header">
      <h2 class="register-title">📝 新規登録</h2>
      <p class="register-description">
        ペットや薬の情報を登録して、投薬管理を始めましょう
      </p>
    </section>

    <!-- タブナビゲーション -->
    <div class="tab-navigation">
      <button 
        @click="activeTab = 'pet'" 
        :class="['tab-button', { 'active': activeTab === 'pet' }]"
      >
        <span class="tab-icon">🐕</span>
        ペット登録
      </button>
      <button 
        @click="activeTab = 'medicine'" 
        :class="['tab-button', { 'active': activeTab === 'medicine' }]"
      >
        <span class="tab-icon">💊</span>
        薬登録
      </button>
    </div>

    <!-- タブコンテンツ -->
    <div class="tab-content">
      <!-- ペット登録タブ -->
      <div v-if="activeTab === 'pet'" class="tab-panel slide-in">
        <div class="form-section">
          <div class="section-header">
            <h3 class="section-title">
              <span class="section-icon">🐕</span>
              新しいペットを登録
            </h3>
            <p class="section-description">
              大切な家族の一員の情報を登録してください
            </p>
          </div>
          <div class="form-container">
            <pet-form></pet-form>
          </div>
        </div>
      </div>

      <!-- 薬登録タブ -->
      <div v-if="activeTab === 'medicine'" class="tab-panel slide-in">
        <div class="form-section">
          <div class="section-header">
            <h3 class="section-title">
              <span class="section-icon">💊</span>
              新しい薬を登録
            </h3>
            <p class="section-description">
              投薬スケジュールに必要な薬の情報を登録してください
            </p>
          </div>
          <div class="form-container">
            <medicine-form></medicine-form>
          </div>
        </div>
      </div>
    </div>

    <!-- 登録完了メッセージ -->
    <div v-if="showSuccessMessage" class="success-message">
      <div class="success-icon">✅</div>
      <h4 class="success-title">登録が完了しました！</h4>
      <p class="success-description">
        {{ activeTab === 'pet' ? 'ペット' : '薬' }}の情報が正常に登録されました。
        ホーム画面で確認できます。
      </p>
      <div class="success-actions">
        <router-link to="/" class="btn btn-primary">ホームに戻る</router-link>
        <button @click="showSuccessMessage = false" class="btn btn-secondary">続けて登録</button>
      </div>
    </div>
  </div>
</template>

<style scoped>
.register-container {
  max-width: 800px;
  margin: 0 auto;
}

.register-header {
  text-align: center;
  margin-bottom: var(--spacing-8);
}

.register-title {
  color: var(--gray-800);
  margin-bottom: var(--spacing-4);
  font-size: var(--font-size-3xl);
}

.register-description {
  color: var(--gray-600);
  font-size: var(--font-size-lg);
  line-height: 1.6;
}

.tab-navigation {
  display: flex;
  gap: var(--spacing-2);
  margin-bottom: var(--spacing-8);
  background: var(--white);
  padding: var(--spacing-2);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow);
  border: 1px solid var(--border-green);
}

.tab-button {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: var(--spacing-2);
  padding: var(--spacing-4) var(--spacing-6);
  border: none;
  background: transparent;
  color: var(--gray-600);
  font-weight: 500;
  border-radius: var(--radius-md);
  cursor: pointer;
  transition: var(--transition);
}

.tab-button:hover {
  background: var(--gray-100);
  color: var(--gray-700);
}

.tab-button.active {
  background: var(--primary-green);
  color: var(--white);
  box-shadow: var(--shadow-sm);
}

.tab-icon {
  font-size: var(--font-size-lg);
}

.tab-content {
  min-height: 400px;
}

.tab-panel {
  animation: fadeIn 0.3s ease-out;
}

.form-section {
  background: var(--white);
  border-radius: var(--radius-xl);
  box-shadow: var(--shadow);
  border: 1px solid var(--border-green);
  overflow: hidden;
}

.section-header {
  background: linear-gradient(135deg, var(--accent-green) 0%, var(--secondary-green) 100%);
  padding: var(--spacing-6);
  border-bottom: 1px solid var(--border-green);
}

.section-title {
  display: flex;
  align-items: center;
  gap: var(--spacing-3);
  color: var(--gray-800);
  margin-bottom: var(--spacing-2);
  font-size: var(--font-size-xl);
}

.section-icon {
  font-size: var(--font-size-2xl);
}

.section-description {
  color: var(--gray-600);
  font-size: var(--font-size-sm);
  margin: 0;
}

.form-container {
  padding: var(--spacing-6);
}

/* 成功メッセージ */
.success-message {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  background: var(--white);
  border-radius: var(--radius-xl);
  padding: var(--spacing-8);
  box-shadow: var(--shadow-xl);
  border: 1px solid var(--border-green);
  text-align: center;
  max-width: 500px;
  width: 90%;
  z-index: 1000;
  animation: fadeIn 0.3s ease-out;
}

.success-icon {
  font-size: 4rem;
  margin-bottom: var(--spacing-4);
}

.success-title {
  color: var(--success);
  margin-bottom: var(--spacing-3);
  font-size: var(--font-size-xl);
}

.success-description {
  color: var(--gray-600);
  margin-bottom: var(--spacing-6);
  line-height: 1.6;
}

.success-actions {
  display: flex;
  gap: var(--spacing-3);
  justify-content: center;
  flex-wrap: wrap;
}

/* アニメーション */
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

@keyframes slideIn {
  from { transform: translateX(20px); opacity: 0; }
  to { transform: translateX(0); opacity: 1; }
}

.slide-in {
  animation: slideIn 0.3s ease-out;
}

/* レスポンシブデザイン */
@media (max-width: 768px) {
  .register-title {
    font-size: var(--font-size-2xl);
  }

  .tab-navigation {
    flex-direction: column;
    gap: var(--spacing-1);
  }

  .tab-button {
    justify-content: flex-start;
    padding: var(--spacing-3) var(--spacing-4);
  }

  .section-header,
  .form-container {
    padding: var(--spacing-4);
  }

  .success-actions {
    flex-direction: column;
    align-items: center;
  }

  .success-actions .btn {
    width: 100%;
    max-width: 200px;
  }
}

@media (max-width: 480px) {
  .register-container {
    padding: 0 var(--spacing-4);
  }

  .success-message {
    padding: var(--spacing-6);
  }
}
</style>