<template>
  <div class="pet-form-container">
    <form @submit.prevent="submitForm" class="pet-form">
      <div class="form-group">
        <label for="pet-name" class="form-label">
          <span class="label-icon">🐕</span>
          ペットの名前
        </label>
        <input 
          id="pet-name"
          v-model="form.name" 
          type="text"
          placeholder="例: ポチ、タマ" 
          class="form-input"
          required
        />
      </div>

      <div class="form-group">
        <label for="pet-species" class="form-label">
          <span class="label-icon">🐾</span>
          種類
        </label>
        <select id="pet-species" v-model="form.species" class="form-select" required>
          <option value="">種類を選択してください</option>
          <option value="dog">犬</option>
          <option value="cat">猫</option>
          <option value="bird">鳥</option>
          <option value="rabbit">うさぎ</option>
          <option value="hamster">ハムスター</option>
          <option value="fish">魚</option>
          <option value="turtle">カメ</option>
          <option value="snake">ヘビ</option>
          <option value="other">その他</option>
        </select>
      </div>

      <div class="form-group">
        <label for="pet-birthdate" class="form-label">
          <span class="label-icon">🎂</span>
          誕生日
        </label>
        <input 
          id="pet-birthdate"
          type="date" 
          v-model="form.birthdate" 
          class="form-input"
          required
        />
        <small class="form-help">正確な日付がわからない場合は、推定日付を入力してください</small>
      </div>

      <div class="form-group">
        <label for="pet-weight" class="form-label">
          <span class="label-icon">⚖️</span>
          体重 (kg)
        </label>
        <input 
          id="pet-weight"
          v-model="form.weight" 
          type="number"
          step="0.1"
          min="0"
          placeholder="例: 5.2" 
          class="form-input"
        />
        <small class="form-help">投薬量の計算に使用されます</small>
      </div>

      <div class="form-group">
        <label for="pet-notes" class="form-label">
          <span class="label-icon">📝</span>
          メモ
        </label>
        <textarea 
          id="pet-notes"
          v-model="form.notes" 
          placeholder="特記事項があれば入力してください" 
          class="form-textarea"
          rows="3"
        ></textarea>
      </div>

      <div class="form-actions">
        <button type="submit" class="btn btn-primary submit-btn" :disabled="isSubmitting">
          <span v-if="isSubmitting" class="loading-spinner"></span>
          <span v-else class="submit-icon">✅</span>
          {{ isSubmitting ? '登録中...' : 'ペットを登録' }}
        </button>
        <button type="button" @click="resetForm" class="btn btn-secondary">
          <span class="reset-icon">🔄</span>
          リセット
        </button>
      </div>
    </form>

    <!-- 成功メッセージ -->
    <div v-if="showSuccess" class="success-message">
      <div class="success-icon">🎉</div>
      <h4 class="success-title">登録完了！</h4>
      <p class="success-text">{{ form.name }}ちゃんの登録が完了しました</p>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const form = ref({
  name: '',
  species: '',
  birthdate: '',
  weight: '',
  notes: ''
})

const isSubmitting = ref(false)
const showSuccess = ref(false)

// ペットの登録
const submitForm = async () => {
  if (isSubmitting.value) return
  
  isSubmitting.value = true
  
  try {
    const response = await fetch('http://localhost:8000/pets', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(form.value)
    })

    if (!response.ok) throw new Error('登録に失敗しました')

    const data = await response.json()
    console.log('登録成功:', data)
    
    // 成功メッセージを表示
    showSuccess.value = true
    
    // フォームをリセット
    resetForm()
    
    // 3秒後に成功メッセージを非表示
    setTimeout(() => {
      showSuccess.value = false
    }, 3000)
    
  } catch (error) {
    console.error(error)
    alert('登録に失敗しました')
  } finally {
    isSubmitting.value = false
  }
}

// フォームをリセット
const resetForm = () => {
  form.value = {
    name: '',
    species: '',
    birthdate: '',
    weight: '',
    notes: ''
  }
}
</script>

<style scoped>
.pet-form-container {
  width: 100%;
}

.pet-form {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-6);
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-2);
}

.form-label {
  display: flex;
  align-items: center;
  gap: var(--spacing-2);
  font-weight: 600;
  color: var(--gray-700);
  font-size: var(--font-size-base);
}

.label-icon {
  font-size: var(--font-size-lg);
}

.form-input,
.form-select,
.form-textarea {
  padding: var(--spacing-3);
  border: 2px solid var(--gray-200);
  border-radius: var(--radius);
  font-size: var(--font-size-base);
  transition: var(--transition);
  background: var(--white);
}

.form-input:focus,
.form-select:focus,
.form-textarea:focus {
  outline: none;
  border-color: var(--primary-green);
  box-shadow: 0 0 0 3px rgb(74 222 128 / 0.1);
}

.form-textarea {
  resize: vertical;
  min-height: 80px;
  font-family: inherit;
}

.form-help {
  color: var(--gray-500);
  font-size: var(--font-size-sm);
  margin-top: var(--spacing-1);
}

.form-actions {
  display: flex;
  gap: var(--spacing-4);
  margin-top: var(--spacing-6);
  padding-top: var(--spacing-6);
  border-top: 1px solid var(--gray-200);
}

.submit-btn {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: var(--spacing-2);
  padding: var(--spacing-4);
  font-size: var(--font-size-base);
  font-weight: 600;
}

.submit-btn:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.submit-icon,
.reset-icon {
  font-size: var(--font-size-lg);
}

.loading-spinner {
  width: 20px;
  height: 20px;
  border: 2px solid transparent;
  border-top: 2px solid currentColor;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

/* 成功メッセージ */
.success-message {
  background: linear-gradient(135deg, var(--success) 0%, #059669 100%);
  color: var(--white);
  padding: var(--spacing-6);
  border-radius: var(--radius-lg);
  text-align: center;
  margin-top: var(--spacing-6);
  animation: slideIn 0.3s ease-out;
}

.success-icon {
  font-size: 3rem;
  margin-bottom: var(--spacing-3);
}

.success-title {
  font-size: var(--font-size-xl);
  margin-bottom: var(--spacing-2);
  font-weight: 600;
}

.success-text {
  font-size: var(--font-size-base);
  opacity: 0.9;
}

@keyframes slideIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

/* レスポンシブデザイン */
@media (max-width: 768px) {
  .form-actions {
    flex-direction: column;
    gap: var(--spacing-3);
  }

  .submit-btn {
    order: 1;
  }
}

@media (max-width: 480px) {
  .pet-form {
    gap: var(--spacing-4);
  }

  .form-actions {
    margin-top: var(--spacing-4);
    padding-top: var(--spacing-4);
  }
}
</style>