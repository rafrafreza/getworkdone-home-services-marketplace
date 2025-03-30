<template>
  <div class="d-flex align-items-center justify-content-center vh-100 bg-image">
    <div class="glassmorphism-container text-center p-4">
      <h2 class="text-white fw-bold mb-3">Welcome Back!</h2>

      <div class="text-start">
        <label for="phone" class="text-white mb-1">Phone</label>
        <input 
          type="text"
          id="phone" 
          class="form-control bg-transparent text-white border-light"
          v-model="phone"
          placeholder="Enter your registered Phone No."
        />
        <small v-if="errors.phone" class="text-danger">{{ errors.phone }}</small>

        <label for="password" class="text-white mb-1 mt-2">Password</label>
        <input 
          type="password" 
          id="password" 
          class="form-control bg-transparent text-white border-light"
          v-model="password"
          placeholder="Enter your password"
        />
        <small v-if="errors.password" class="text-danger">{{ errors.password }}</small>
      </div>

      <!-- Login Button -->
      <button class="btn btn-primary w-100 mt-3" @click="handleLogin" :disabled="loading">
        <span v-if="loading">Logging in...</span>
        <span v-else>Login</span>
      </button>

      <small v-if="errors.api" class="text-danger d-block mt-2">{{ errors.api }}</small>

      <p  class="text-white mt-4 mb-1">Are you new here? Please SignUp.</p>

      <!-- Sign Up Button -->
      <router-link to="/signup" class="btn signup-btn w-100 mt-3">Create an Account</router-link>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      phone: '',
      password: '',
      loading: false,
      errors: {},
    };
  },
  methods: {
    async handleLogin() {
      this.errors = {}; // Reset previous errors

      // Basic validation
      if (!this.phone.match(/^\d{10}$/)) {
        this.errors.phone = "Enter a valid 10-digit phone number";
      }
      if (!this.password) {
        this.errors.password = "Password is required";
      }
      if (Object.keys(this.errors).length) return;

      this.loading = true;
      
      try {
        const response = await axios.post('http://127.0.0.1:5000/auth/login', {
          phone: this.phone,
          password: this.password
        });

        const token = response.data.access_token;
        const role = response.data.role; // Ensure the backend sends role in the response

        // Store token in local storage or Vuex for future API calls
        localStorage.setItem('token', token);

        // Redirect based on user role
        if (role === 0) {
          this.$router.push('/');
        } else if (role === 1) {
          this.$router.push('/dashboard/professional');
        } else if (role === 2) {
          this.$router.push('/dashboard/admin');
        } else {
          alert("Please contact support.");
        }
      } catch (error) {
        this.errors.api = error.response?.data?.message || "Login failed. Please try again.";
      } finally {
        this.loading = false;
      }
    }
  }
};
</script>

<style scoped>
/* Background Image */
.bg-image {
  background: url('/images/login_background.jpg') center/cover no-repeat;
}

/* Glassmorphism Container */
.glassmorphism-container {
  background: rgba(255, 255, 255, 0.12);
  backdrop-filter: blur(15px);
  border-radius: 15px;
  padding: 2rem;
  width: 350px;
  box-shadow: 0 5px 20px rgba(0, 0, 0, 0.4);
}

/* Input Fields */
.form-control {
  background: rgba(255, 255, 255, 0.2) !important;
  color: white !important;
  border: 1px solid rgba(255, 255, 255, 0.7);
}

.form-control::placeholder {
  color: rgba(255, 255, 255, 0.85) !important;
}

.form-control:focus {
  border-color: #ffcc00;
  box-shadow: 0 0 8px rgba(255, 204, 0, 0.8);
}

/* Signup Button */
.signup-btn {
  background: linear-gradient(135deg, #ffcc00, #ff5733);
  color: white;
  font-weight: bold;
  padding: 10px;
  border: none;
  border-radius: 30px;
  transition: all 0.3s ease-in-out;
}

.signup-btn:hover {
  background: linear-gradient(135deg, #ff5733, #ffcc00);
  transform: scale(1.05);
  box-shadow: 0 0 10px rgba(255, 87, 51, 0.8);
}
</style>
