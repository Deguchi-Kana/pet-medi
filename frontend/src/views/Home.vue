<script setup>
import MedicineList from "../components/MedicineList.vue";
import PetList from "../components/PetList.vue";
</script>

<template>
  <div class="home-container fade-in">
    <!-- ウェルカムセクション -->
    <section class="welcome-section">
      <div class="welcome-content">
        <h2 class="welcome-title">🐾 ペットの健康管理を簡単に</h2>
        <p class="welcome-description">
          大切な家族の一員であるペットの投薬スケジュールを管理し、健康な生活をサポートします
        </p>
      </div>
    </section>

    <!-- ダッシュボードグリッド -->
    <div class="dashboard-grid">
      <!-- ペット情報セクション -->
      <section class="dashboard-section">
        <div class="section-header">
          <h3 class="section-title">
            <span class="section-icon">🐕</span>
            ペット情報
          </h3>
          <p class="section-description">登録されているペットの一覧です</p>
        </div>
        <div class="section-content">
          <pet-list></pet-list>
        </div>
      </section>

      <!-- 薬情報セクション -->
      <section class="dashboard-section">
        <div class="section-header">
          <h3 class="section-title">
            <span class="section-icon">💊</span>
            投薬情報
          </h3>
          <p class="section-description">登録されている薬の一覧です</p>
        </div>
        <div class="section-content">
          <medicine-list></medicine-list>
        </div>
      </section>
    </div>

    <!-- クイックアクション -->
    <section class="quick-actions">
      <h3 class="quick-actions-title">クイックアクション</h3>
      <div class="action-buttons">
        <router-link to="/register" class="action-btn action-btn-primary">
          <span class="action-icon">➕</span>
          新しいペットを登録
        </router-link>
        <router-link to="/register" class="action-btn action-btn-secondary">
          <span class="action-icon">💊</span>
          新しい薬を登録
        </router-link>
        <router-link to="/calendar" class="action-btn action-btn-info">
          <span class="action-icon">📅</span>
          スケジュールを確認
        </router-link>
      </div>
    </section>
  </div>
</template>

<style scoped>
.home-container {
  max-width: 1200px;
  margin: 0 auto;
}

.welcome-section {
  background: linear-gradient(135deg, var(--accent-green) 0%, var(--secondary-green) 100%);
  border-radius: var(--radius-xl);
  padding: var(--spacing-12);
  margin-bottom: var(--spacing-8);
  text-align: center;
  box-shadow: var(--shadow-lg);
  border: 1px solid var(--border-green);
}

.welcome-title {
  color: var(--gray-800);
  margin-bottom: var(--spacing-4);
  font-size: var(--font-size-3xl);
}

.welcome-description {
  color: var(--gray-600);
  font-size: var(--font-size-lg);
  max-width: 600px;
  margin: 0 auto;
  line-height: 1.6;
}

.dashboard-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: var(--spacing-8);
  margin-bottom: var(--spacing-8);
}

.dashboard-section {
  background: var(--white);
  border-radius: var(--radius-xl);
  box-shadow: var(--shadow);
  border: 1px solid var(--border-green);
  overflow: hidden;
  transition: var(--transition);
}

.dashboard-section:hover {
  box-shadow: var(--shadow-lg);
  transform: translateY(-2px);
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

.section-content {
  padding: var(--spacing-6);
}

.quick-actions {
  background: var(--white);
  border-radius: var(--radius-xl);
  padding: var(--spacing-8);
  box-shadow: var(--shadow);
  border: 1px solid var(--border-green);
  text-align: center;
}

.quick-actions-title {
  color: var(--gray-800);
  margin-bottom: var(--spacing-6);
  font-size: var(--font-size-2xl);
}

.action-buttons {
  display: flex;
  gap: var(--spacing-4);
  justify-content: center;
  flex-wrap: wrap;
}

.action-btn {
  display: flex;
  align-items: center;
  gap: var(--spacing-3);
  padding: var(--spacing-4) var(--spacing-6);
  border-radius: var(--radius-lg);
  text-decoration: none;
  font-weight: 500;
  transition: var(--transition);
  min-width: 200px;
  justify-content: center;
}

.action-btn-primary {
  background: var(--primary-green);
  color: var(--white);
}

.action-btn-primary:hover {
  background: var(--primary-green-dark);
  transform: translateY(-2px);
  box-shadow: var(--shadow-lg);
}

.action-btn-secondary {
  background: var(--white);
  color: var(--gray-700);
  border: 2px solid var(--primary-green);
}

.action-btn-secondary:hover {
  background: var(--primary-green);
  color: var(--white);
  transform: translateY(-2px);
  box-shadow: var(--shadow-lg);
}

.action-btn-info {
  background: var(--info);
  color: var(--white);
}

.action-btn-info:hover {
  background: #2563eb;
  transform: translateY(-2px);
  box-shadow: var(--shadow-lg);
}

.action-icon {
  font-size: var(--font-size-xl);
}

/* レスポンシブデザイン */
@media (max-width: 768px) {
  .dashboard-grid {
    grid-template-columns: 1fr;
    gap: var(--spacing-6);
  }

  .welcome-section {
    padding: var(--spacing-8);
  }

  .welcome-title {
    font-size: var(--font-size-2xl);
  }

  .action-buttons {
    flex-direction: column;
    align-items: center;
  }

  .action-btn {
    width: 100%;
    max-width: 300px;
  }
}

@media (max-width: 480px) {
  .welcome-section {
    padding: var(--spacing-6);
  }

  .section-header,
  .section-content {
    padding: var(--spacing-4);
  }

  .quick-actions {
    padding: var(--spacing-6);
  }
}
</style>