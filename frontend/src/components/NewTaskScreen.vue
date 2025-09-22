<template>
  <div class="container">
    <p class="header">Create a New Task</p>
    <div class="task-form">
      <p class="section-header"><u>Task Details</u></p>

      <div class="task-section">
        <div class="task-item">
          <!-- Task Name -->
          <p class="section-header">Enter Task Name</p>
          <input
            type="text"
            v-model="taskTitle"
            placeholder="Task name"
            class="text-input"
          />
        </div>
        <div class="task-item">
          <!-- Task Description -->
          <p class="section-header">Enter Task Description</p>
          <textarea
            v-model="taskDescription"
            placeholder="Describe your task..."
            class="textarea"
          ></textarea>
        </div>
      </div>

      <p class="section-header"><u>Upload Task Files</u></p>

      <p class="section-header">Select Modeling Language</p>

      <select v-model="selectedModelLanguage" class="dropdown">
        <option disabled value="">Select Model Language</option>
        <option>UML</option>
        <option>Petri-Net</option>
      </select>

      <div class="upload-section">
        <!-- Upload Model File -->
        <div class="upload-item">
          <p class="section-header">Upload Model File</p>
          <input type="file" @change="e => handleFileUpload(e, 'model')" class="file-input" />
        </div>

        <!-- Upload Error File -->
        <div class="upload-item">
          <p class="section-header">Upload Error File</p>
          <input type="file" @change="e => handleFileUpload(e, 'error')" class="file-input" />
        </div>
      </div>

      <p class="section-header"><u>Conversation Options</u></p>

      <div class="conversation-section">
        <div class = "conversation-item">
        <p class="section-header">Select LLM</p>
        <select v-model="selectedLLM" class="dropdown">
            <option disabled value="">Select LLM</option>
            <option>GPT-3.5</option>
            <option>GPT-4</option>
        </select>
        </div>
        <div class = "conversation-item">
            <p class="section-header">Select Language</p>
            <select v-model="selectedLanguage" class="dropdown">
                <option disabled value="">Select Language</option>
                <option>English</option>
                <option>German</option>
            </select>
        </div>
      </div>
      <button @click="createTask" class="submit-button">Create Task</button>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import axios from 'axios';

const taskTitle = ref('');
const taskDescription = ref('');
const selectedModelLanguage = ref('');
const modelFile = ref(null);
const errorFile = ref(null);
const selectedLLM = ref('');
const selectedLanguage = ref('');

function handleFileUpload(event, type) {
  const file = event.target.files[0];
  if (type === 'model') {
    modelFile.value = file;
  } else if (type === 'error') {
    errorFile.value = file;
  }
}

async function createTask() {
  if (!taskTitle.value || !taskDescription.value || !selectedModelLanguage.value || !modelFile.value || !errorFile.value || !selectedLLM.value || !selectedLanguage.value) {
    alert('Please fill in all fields and upload both files.' + modelFile.value);
    return;
  }

  const formData = new FormData();
  formData.append('title', taskTitle.value);
  formData.append('description', taskDescription.value);
  formData.append('model_language', selectedModelLanguage.value);
  formData.append('model_file', modelFile.value);
  formData.append('error_file', errorFile.value);
  formData.append('llm', selectedLLM.value);
  formData.append('language', selectedLanguage.value);

  try {
    const response = await axios.post('http://localhost:8000/tasks/', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    });
    alert('Task created successfully!');
    // Reset form
    taskTitle.value = '';
    taskDescription.value = '';
    selectedModelLanguage.value = '';
    modelFile.value = null;
    errorFile.value = null;
    selectedLLM.value = '';
    selectedLanguage.value = '';
  } catch (error) {
    console.error('Error creating task:', error);
    alert('Failed to create task. Please try again.');
  }
}

</script>

<style scoped>
.container {
  padding: 0px 100px;
  color: #2a2a2a;
  background-color: #00000000;
  height: 100%;
  display:flex;
  flex-direction:column;
}

.task-form {
  width: 100%; /* no auto-centering */
  display: flex;
  align-items: flex-start;
  flex-direction: column;
  align-items: flex-start; /* everything aligns left */
  /* make it scrollable if content exceeds viewport on the bottm */
  height: calc(85vh - 120px);
}

.text-input,
.file-input,
.textarea {
  width: calc(100% - 24px); /* keeps inputs a reasonable size */
  padding: 8px 12px;
  border-radius: 8px;
  border: none;
  font-size: 1rem;
  background-color: #f1f1f2;
  color: #2a2a2a;
  box-shadow: 0px 2px 5px rgba(42, 42, 42, 0.25)
}

.section-header {
  font-weight: bold;
}

.textarea {
  height: 120px;
  resize: none;
}

.upload-section,
.task-section,
.conversation-section {
  display: flex;
  flex-direction: row;
  gap: 20px;
  width: 100%;
  justify-content: space-between;
  padding-bottom: 20px;
  border-bottom: 1px solid #000000;
}

.upload-item,
.task-item,
.conversation-item {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 8px;
  align-items: flex-start;
}

.submit-button {
  width: calc(25% - 20px);
  min-width: 200px;
  padding: 10px;
  margin-top: 20px;
  background-color: #2a2a2a;
  color: #f1f1f2;
  border: none;
  border-radius: 10px;
  box-shadow: 0px 5px 10px rgba(42, 42, 42, 0.25);
}

.file-input {
  background-color: #f1f1f2;
  color: #2a2a2a;
  box-shadow: 0px 2px 5px rgba(42, 42, 42, 0.25)
}

.dropdown {
  background-color: #f1f1f2;
  color: #2a2a2a;
  box-shadow: 0px 2px 5px rgba(42, 42, 42, 0.25)
}

</style>
