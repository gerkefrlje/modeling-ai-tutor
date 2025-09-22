<template>
  <div class="app-container">
    <!-- Banner -->
    <header class="banner">
      <p class="header">Banner (put text/info here)</p>
    </header>

    <div class="content">
      <!-- Sidebar -->
      <Sidebar/>

      <!-- Main Window -->
      <main class="main-window">
        <NewTaskScreen/>
      </main>
    </div>
  </div>
</template>

<script setup>
import Sidebar from './components/Sidebar.vue';
import NewTaskScreen from './components/NewTaskScreen.vue';
</script>

<style scoped>

.app-container {
  display: flex;
  flex-direction: column;
  height: 100vh;
  width: 100vw;
  max-width: 100%;
  max-height: 100%;
  scrollbar-color: #2a2a2a #ffffff00; /* thumb and track color */
}

.content {
  display: flex;
  flex-direction: row;
  flex: 1;
  overflow: hidden;
  max-width:100%;
  height: calc(100vh - 70px); /* Adjust based on banner height */
}

.banner {
  width: 100%;
  background-color: #f25b86;
  text-align: center;  
  position: relative;
  z-index: 11;
  box-shadow: 0px 5px 10px rgba(42, 42, 42, 0.25);
  height: 70px
}

.main-window {
  flex: 1;
  background-color: 	#e1dfe3;
  overflow:auto;
  min-width: 600px;
}
</style>
