<template>
    <aside class="sidebar">
        <p class="header">Previous Tasks</p>
        <div class="history">
            <div class="history-item" v-for="n in 30" :key="n">Conversation {{ n }}</div>
        </div>
        <button class="new-task-button">+ New Task</button>
    </aside>
</template>

<script setup>
</script>

<style scoped>
.sidebar {
  width: 15%;
  min-width: 200px;
  padding: 0px 10px 0px 10px;
  max-width: calc(20% - 20px);
  text-align: left;
  background-color: #f1f1f2;
  color: #2a2a2a;
  position: relative;
  z-index: 10;
  box-shadow: 5px 0px 10px rgba(42, 42, 42, 0.25);
}

.history {
  height: calc(85vh - 120px); /* Adjust based on banner height */
  overflow-y: auto;
  padding-right: 5px; /* To avoid content being hidden behind scrollbar */
  padding-left: 5px;
  background-color: #e1dfe3;
  border-radius: 10px;
  box-shadow:inset 0 0 10px rgba(42, 42, 42, 0.25);
  z-index: 9;
}

.history-item {
  position: relative;
  background-color: #f1f1f200;
  padding:10px;
  margin:5px 0;
  border-radius: 5px;
  overflow:hidden;
  white-space: nowrap;
  text-overflow: ellipsis;
  z-index: 8;
  transition: background-color 0.2s ease, box-shadow 0.2s ease;
}

.history-item:hover {
  background-color: #f1f1f2;
  box-shadow: 0px 2px 5px rgba(42, 42, 42, 0.25);
  cursor: pointer;
}

.new-task-button {
  width: 100%;
  padding: 10px;
  margin-top: 20px;
  background-color: #2a2a2a;
  color: #f1f1f2;
  border: none;
  border-radius: 10px;
  box-shadow: 0px 5px 10px rgba(42, 42, 42, 0.25);
}
</style>