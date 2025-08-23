<template>
  <div id="app">
    <!-- ヘッダー -->
    <header class="app-header">
      <div class="container">
        <div class="header-content">
          <div class="logo">
            <div class="logo-icon">🐾</div>
            <h1 class="logo-text">PetMedi</h1>
          </div>
          <nav class="main-nav">
            <router-link to="/" class="nav-link">
              <span class="nav-icon">🏠</span>
              ホーム
            </router-link>
            <router-link to="/calendar" class="nav-link">
              <span class="nav-icon">📅</span>
              カレンダー
            </router-link>
            <router-link to="/register" class="nav-link">
              <span class="nav-icon">➕</span>
              登録
            </router-link>
          </nav>
        </div>
      </div>
    </header>

    <!-- メインコンテンツ -->
    <main class="main-content">
      <div class="container">
        <router-view />
      </div>
    </main>

    <!-- フッター -->
    <footer class="app-footer">
      <div class="container">
        <p>&copy; 2025 PetMedi - ペットの投薬管理を簡単に</p>
      </div>
    </footer>
  </div>
</template>

<script>
export default {
  name: 'App',
};
</script>

<style scoped>
.app-header {
  background: linear-gradient(135deg, var(--primary-green) 0%, var(--primary-green-dark) 100%);
  box-shadow: var(--shadow-lg);
  position: sticky;
  top: 0;
  z-index: 100;
}

.header-content {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: var(--spacing-4) 0;
}

.logo {
  display: flex;
  align-items: center;
  gap: var(--spacing-3);
}

.logo-icon {
  font-size: 2rem;
  filter: drop-shadow(0 2px 4px rgba(0, 0, 0, 0.1));
}

.logo-text {
  color: var(--white);
  font-size: var(--font-size-2xl);
  font-weight: 700;
  margin: 0;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.main-nav {
  display: flex;
  gap: var(--spacing-6);
}

.nav-link {
  display: flex;
  align-items: center;
  gap: var(--spacing-2);
  color: var(--white);
  text-decoration: none;
  font-weight: 500;
  padding: var(--spacing-2) var(--spacing-4);
  border-radius: var(--radius-lg);
  transition: var(--transition);
  position: relative;
}

.nav-link:hover {
  background-color: rgba(255, 255, 255, 0.1);
  transform: translateY(-1px);
}

.nav-link.router-link-active {
  background-color: rgba(255, 255, 255, 0.2);
  box-shadow: var(--shadow-sm);
}

.nav-icon {
  font-size: var(--font-size-lg);
}

.main-content {
  min-height: calc(100vh - 140px);
  padding: var(--spacing-8) 0;
}

.app-footer {
  background-color: var(--gray-100);
  border-top: 1px solid var(--gray-200);
  padding: var(--spacing-6) 0;
  text-align: center;
  color: var(--gray-600);
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 var(--spacing-6);
}

/* レスポンシブデザイン */
@media (max-width: 768px) {
  .header-content {
    flex-direction: column;
    gap: var(--spacing-4);
    padding: var(--spacing-3) 0;
  }

  .main-nav {
    gap: var(--spacing-3);
  }

  .nav-link {
    padding: var(--spacing-2) var(--spacing-3);
    font-size: var(--font-size-sm);
  }

  .logo-text {
    font-size: var(--font-size-xl);
  }

  .container {
    padding: 0 var(--spacing-4);
  }
}

@media (max-width: 480px) {
  .main-nav {
    flex-direction: column;
    gap: var(--spacing-2);
  }

  .nav-link {
    justify-content: center;
  }
}
</style>
