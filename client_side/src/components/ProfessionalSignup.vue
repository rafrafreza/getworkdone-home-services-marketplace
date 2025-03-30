<template>
  <div class="card form-card mt-4 p-4">
    <div class="steps d-flex justify-content-between mb-3">
      <div v-for="(s, index) in steps" :key="index" class="step" :class="{ active: step === index + 1 }">
        <span class="step-number">{{ index + 1 }}</span>
      </div>
    </div>

    <form @submit.prevent="handleSignup">
      <transition name="fade">
        <div v-if="step === 1">
          <label class="form-label">Full Name</label>
          <input v-model="formData.fname" type="text" class="form-control mb-3" required />

          <label class="form-label">Phone</label>
          <input v-model="formData.phone" type="text" class="form-control mb-3" required />

          <label class="form-label">Email</label>
          <input v-model="formData.email" type="email" class="form-control mb-3" required />

          <label class="form-label">Password</label>
          <input v-model="formData.password" type="password" class="form-control mb-3" required />
        </div>
      </transition>

      <transition name="fade">
        <div v-if="step === 2">
          <label class="form-label">City</label>
          <input v-model="formData.city" type="text" class="form-control mb-3" required />

          <label class="form-label">Pin Code</label>
          <input v-model="formData.pin_code" type="number" class="form-control mb-3" required />

          <label class="form-label">Base Price/hour</label>
          <input v-model="formData.base_price_per_hour" type="number" class="form-control mb-3" required />

          <label class="form-label">Experience (Years)</label>
          <input v-model="formData.experience" type="number" class="form-control mb-3" required />
        </div>
      </transition>

      <transition name="fade">
        <div v-if="step === 3">
          <label class="form-label">Service Type</label>
          <select v-model="formData.service_type" class="form-control mb-3" required>
            <option value="" disabled>Select a Service Type</option>
            <option v-for="category in serviceCategories" :key="category.id" :value="category.name">
              {{ category.name }}
            </option>
          </select>

          <label class="form-label">Profile Picture</label>
          <input type="file" class="form-control mb-3" @change="handleFileUpload" accept="image/*" />

          <label class="form-label">Upload Resume (PDF)</label>
          <input type="file" class="form-control mb-3" @change="handlePdfUpload" accept="application/pdf" />
        </div>
      </transition>

      <div class="d-flex justify-content-between mt-3">
        <button v-if="step > 1" type="button" class="btn btn-outline-secondary" @click="prevStep">Back</button>
        <button v-if="step < 3" type="button" class="btn btn-primary ms-auto" @click="nextStep">Next</button>
        <button v-if="step === 3" type="submit" class="btn btn-success ms-auto" :disabled="loading">
          {{ loading ? "Signing Up..." : "Sign Up" }}
        </button>
      </div>
    </form>
    <router-link to="/login" class="btn mt-3">Already have an account? Login here</router-link>
  </div>
</template>

<script>
import axios from 'axios';
import { ref, onMounted } from 'vue';

export default {
  setup() {
    const step = ref(1);
    const steps = ["Personal", "Location", "Uploads"];
    const formData = ref({
      fname: '', phone: '', email: '', password: '',
      city: '', pin_code: '', base_price_per_hour: '',
      experience: '', service_type: '', profile_picture: '', resume: ''
    });
    const serviceCategories = ref([]); // Define correctly
    const loading = ref(false);

    // Fetch service categories from backend
    const fetchCategories = async () => {
      try {
        const response = await axios.get('http://127.0.0.1:5000/api/service-categories');
        serviceCategories.value = response.data.categories;
      } catch (error) {
        console.error('Error fetching categories:', error);
      }
    };

    const nextStep = () => { if (step.value < 3) step.value++; };
    const prevStep = () => { if (step.value > 1) step.value--; };

    const handleFileUpload = (event) => {
      const file = event.target.files[0];
      if (file) {
        const reader = new FileReader();
        reader.readAsDataURL(file);
        reader.onload = () => { formData.value.profile_picture = reader.result; };
      }
    };

    const handlePdfUpload = (event) => {
      const file = event.target.files[0];
      if (file) {
        const reader = new FileReader();
        reader.readAsDataURL(file);
        reader.onload = () => { formData.value.resume = reader.result; };
      }
    };

    const handleSignup = async () => {
      try {
        loading.value = true;
        const response = await axios.post('http://127.0.0.1:5000/auth/signup/professional', formData.value, {
          headers: { "Content-Type": "application/json" }
        });

        alert("You have successfully registered! You can login once Admin verifies your submission and approves you.");
        console.log(response.data.message);
      } catch (error) {
        alert(error.response?.data?.message || 'Signup failed.');
      } finally {
        loading.value = false;
      }
    };

    onMounted(fetchCategories); // Correct function call

    return { step, steps, formData, serviceCategories, nextStep, prevStep, handleSignup, handleFileUpload, handlePdfUpload, loading };
  }
};
</script>

<style scoped>
.container {
  background: linear-gradient(135deg, #eef2f3, #dce3e6);
}

.form-card {
  width: 100%;
  max-width: 400px;
  border-radius: 12px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
  background: white;
}

.steps {
  display: flex;
  justify-content: center;
  gap: 10px;
}

.step {
  width: 30px;
  height: 30px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  background: lightgray;
  font-weight: bold;
  color: white;
}

.step.active {
  background: #007bff;
}

.fade-enter-active, .fade-leave-active {
  transition: opacity 0.4s;
}

.fade-enter, .fade-leave-to {
  opacity: 0;
}
</style>
