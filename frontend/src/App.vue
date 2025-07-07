<template>
  <div id="app">
    <h1>ペットの投薬管理アプリ</h1>
    <nav>
      <router-link to="/">ホーム</router-link> |
      <router-link to="/calendar">カレンダー</router-link> |
      <router-link to="/register">登録</router-link>
    </nav>
    <router-view />
  </div>
</template>

<script>
export default {
  name: 'App',
};
</script>

<style scoped>
h1 {
  text-align: center;
  margin-top: 2rem;
  color: #42b983;
}
</style>
