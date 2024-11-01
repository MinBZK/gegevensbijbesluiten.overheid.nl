<template>
  <div class="error-page">
    <h1 class="error-title">Pagina niet gevonden</h1>
    <a class="error-button" href="/">Ga terug naar hoofdpagina</a>
  </div>
</template>

<script lang="ts">
export default {
  methods: {
    goHome() {
      // this.$router.push({ name: 'Dashboard' })
    }
  }
}
</script>

<style>
.error-page {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100vh;
  background-color: #f8f8f8;
}

.error-title {
  font-size: 48px;
  color: #ff0000;
  margin-bottom: 16px;
}

.error-message {
  font-size: 24px;
  color: #333333;
  margin-bottom: 16px;
}

.error-button {
  padding: 12px 24px;
  font-size: 18px;
  color: #ffffff;
  background-color: #01689b;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.error-button:hover {
  background-color: #007bff;
}
</style>
