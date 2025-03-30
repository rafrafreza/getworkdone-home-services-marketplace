<template>
  <div>
    <form @submit.prevent="handleSignup" class="mt-4">
      <div class="mb-3">
        <label class="form-label fw-bold">Full Name:</label>
        <input v-model="formData.fname" type="text" class="form-control" required />
      </div>
      <div class="mb-3">
        <label class="form-label fw-bold">Phone:</label>
        <input v-model="formData.phone" type="text" class="form-control" required />
      </div>
      <div class="mb-3">
        <label class="form-label fw-bold">Password:</label>
        <input v-model="formData.password" type="password" class="form-control" required />
      </div>
      <div class="mb-3">
        <label class="form-label fw-bold">Profile Picture:</label>
        <input type="file" class="form-control mt-2" @change="handleFileUpload" accept="image/*" />
      </div>
      <div class="row">
        <div class="col-md-6 mb-3">
          <label class="form-label fw-bold">City:</label>
          <input v-model="formData.city" type="text" class="form-control" required />
        </div>
        <div class="col-md-6 mb-3">
          <label class="form-label fw-bold">Pin Code:</label>
          <input v-model="formData.pin_code" type="text" class="form-control" required />
        </div>
      </div>
      <button type="submit" class="btn btn-primary w-100 fw-bold">Sign Up</button>
    </form>
    <router-link to="/login" class="btn signup-btn w-100 mt-3">Already have an account? Login here</router-link>
  </div>
  </template>
  
  <script>
  import axios from 'axios';
  import { ref } from 'vue';
  
  export default {
    setup() {
      const formData = ref({
        fname: '',
        phone: '',
        password: '',
        city: '',
        pin_code: '',
        profile_picture: ''
      });
  
      const handleFileUpload = (event) => {
    const file = event.target.files[0];
    if (file) {
        const reader = new FileReader();
        reader.readAsDataURL(file);
        reader.onload = () => {
            formData.value.profile_picture = reader.result; // Convert image to Base64
        };
    }
};
  
      const handleSignup = async () => {
        try {
          const formDataObject = new FormData();
          for (const key in formData.value) {
            formDataObject.append(key, formData.value[key]);
          }
  
          const response = await axios.post('http://127.0.0.1:5000/auth/signup/customer', formDataObject, {
            headers: { 'Content-Type': 'multipart/form-data' }
          });
  
          alert(response.data.message);
        } catch (error) {
          console.error('Signup failed:', error.response ? error.response.data : error);
          alert(error.response?.data?.message || 'Signup failed. Please check your input.');
        }
      };
  
      return { formData, handleSignup, handleFileUpload };
    }
  };
  </script>
  