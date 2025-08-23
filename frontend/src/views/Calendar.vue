<script setup>
import { ref, onMounted } from 'vue'
import CalendarView from "../components/CalendarView.vue";
import AiChat from "../components/AiChat.vue";

const todayMedicines = ref([])

// 今日の日付をフォーマット
const formatToday = () => {
  const today = new Date()
  return today.toLocaleDateString('ja-JP', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    weekday: 'long'
  })
}

// 今日の投薬予定を取得（サンプルデータ）
onMounted(() => {
  // 実際の実装では、APIから今日の投薬予定を取得
  todayMedicines.value = [
    {
      id: 1,
      medicine_name: 'フィラリア薬',
      timing: ['朝']
    },
    {
      id: 2,
      medicine_name: 'アモキシシリン',
      timing: ['夜']
    }
  ]
})
</script>

<template>
  <div class="calendar-container fade-in">
    <!-- ヘッダー -->
    <section class="calendar-header">
      <div class="header-content">
        <div class="header-info">
          <h2 class="calendar-title">📅 投薬スケジュール</h2>
          <p class="calendar-description">
            ペットの投薬スケジュールをカレンダーで確認できます
          </p>
        </div>
        <div class="header-actions">
          <router-link to="/register" class="btn btn-primary">
            <span class="btn-icon">➕</span>
            新規登録
          </router-link>
        </div>
      </div>
    </section>

    <!-- メインコンテンツ -->
    <div class="calendar-main">
      <!-- カレンダーセクション -->
      <section class="calendar-section">
        <div class="section-header">
          <h3 class="section-title">
            <span class="section-icon">📅</span>
            スケジュールカレンダー
          </h3>
          <p class="section-description">
            今日の投薬予定や今後のスケジュールを確認できます
          </p>
        </div>
        <div class="calendar-content">
          <calendar-view></calendar-view>
        </div>
      </section>

      <!-- AIチャットセクション -->
      <section class="chat-section">
        <div class="section-header">
          <h3 class="section-title">
            <span class="section-icon">🤖</span>
            AI アシスタント
          </h3>
          <p class="section-description">
            投薬についての質問や相談をAIに聞いてみましょう
          </p>
        </div>
        <div class="chat-content">
          <ai-chat></ai-chat>
        </div>
      </section>
    </div>

    <!-- 今日の投薬リマインダー -->
    <section class="today-reminder">
      <div class="reminder-header">
        <h3 class="reminder-title">
          <span class="reminder-icon">⏰</span>
          今日の投薬予定
        </h3>
        <span class="reminder-date">{{ formatToday() }}</span>
      </div>
      <div class="reminder-content">
        <div v-if="todayMedicines.length > 0" class="medicine-reminders">
          <div v-for="medicine in todayMedicines" :key="medicine.id" class="reminder-item">
            <div class="reminder-info">
              <span class="medicine-name">{{ medicine.medicine_name }}</span>
              <span class="timing-badge">{{ medicine.timing.join(', ') }}</span>
            </div>
            <div class="reminder-status">
              <span class="status-dot"></span>
              未完了
            </div>
          </div>
        </div>
        <div v-else class="no-reminders">
          <p>今日の投薬予定はありません</p>
        </div>
      </div>
    </section>
  </div>
</template>

<style scoped>
.calendar-container {
  max-width: 1200px;
  margin: 0 auto;
}

.calendar-header {
  background: linear-gradient(135deg, var(--accent-green) 0%, var(--secondary-green) 100%);
  border-radius: var(--radius-xl);
  padding: var(--spacing-8);
  margin-bottom: var(--spacing-8);
  box-shadow: var(--shadow-lg);
  border: 1px solid var(--border-green);
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.header-info {
  flex: 1;
}

.calendar-title {
  color: var(--gray-800);
  margin-bottom: var(--spacing-3);
  font-size: var(--font-size-3xl);
}

.calendar-description {
  color: var(--gray-600);
  font-size: var(--font-size-lg);
  line-height: 1.6;
  margin: 0;
}

.header-actions {
  flex-shrink: 0;
}

.btn-icon {
  margin-right: var(--spacing-2);
}

.calendar-main {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: var(--spacing-8);
  margin-bottom: var(--spacing-8);
}

.calendar-section,
.chat-section {
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

.calendar-content,
.chat-content {
  padding: var(--spacing-6);
  min-height: 400px;
}

/* 今日の投薬リマインダー */
.today-reminder {
  background: var(--white);
  border-radius: var(--radius-xl);
  box-shadow: var(--shadow);
  border: 1px solid var(--border-green);
  overflow: hidden;
}

.reminder-header {
  background: linear-gradient(135deg, var(--warning) 0%, #fbbf24 100%);
  padding: var(--spacing-6);
  border-bottom: 1px solid var(--border-green);
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.reminder-title {
  display: flex;
  align-items: center;
  gap: var(--spacing-3);
  color: var(--white);
  margin: 0;
  font-size: var(--font-size-xl);
}

.reminder-icon {
  font-size: var(--font-size-2xl);
}

.reminder-date {
  color: var(--white);
  font-weight: 500;
  background: rgba(255, 255, 255, 0.2);
  padding: var(--spacing-2) var(--spacing-4);
  border-radius: var(--radius-xl);
}

.reminder-content {
  padding: var(--spacing-6);
}

.medicine-reminders {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-4);
}

.reminder-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: var(--spacing-4);
  background: var(--gray-50);
  border-radius: var(--radius-lg);
  border: 1px solid var(--gray-200);
}

.reminder-info {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-2);
}

.medicine-name {
  font-weight: 600;
  color: var(--gray-800);
}

.timing-badge {
  background: var(--primary-green);
  color: var(--white);
  padding: var(--spacing-1) var(--spacing-3);
  border-radius: var(--radius);
  font-size: var(--font-size-sm);
  font-weight: 500;
}

.reminder-status {
  display: flex;
  align-items: center;
  gap: var(--spacing-2);
  color: var(--warning);
  font-weight: 500;
}

.status-dot {
  width: 8px;
  height: 8px;
  background: var(--warning);
  border-radius: 50%;
  animation: pulse 2s infinite;
}

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.5; }
}

.no-reminders {
  text-align: center;
  color: var(--gray-500);
  padding: var(--spacing-8);
}

/* レスポンシブデザイン */
@media (max-width: 1024px) {
  .calendar-main {
    grid-template-columns: 1fr;
    gap: var(--spacing-6);
  }
}

@media (max-width: 768px) {
  .header-content {
    flex-direction: column;
    gap: var(--spacing-4);
    text-align: center;
  }

  .calendar-title {
    font-size: var(--font-size-2xl);
  }

  .reminder-header {
    flex-direction: column;
    gap: var(--spacing-3);
    text-align: center;
  }

  .section-header,
  .calendar-content,
  .chat-content,
  .reminder-content {
    padding: var(--spacing-4);
  }
}

@media (max-width: 480px) {
  .calendar-container {
    padding: 0 var(--spacing-4);
  }

  .calendar-header {
    padding: var(--spacing-6);
  }
}
</style>