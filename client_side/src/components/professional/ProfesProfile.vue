<template>
    <div class="container">
      <!-- Professional Profile -->
      <transition name="fade">
        <div v-if="profile" class="profile-card">
          <div class="profile-header">
            <img :src="profile.profile_picture || defaultAvatar" alt="Profile Picture" class="profile-img" />
            <h4>{{ profile.name }}</h4>
            <p class="text-muted">{{ profile.email }}</p>
          </div>
          <div class="profile-details">
            <p><strong>Service Type:</strong> {{ profile.service_type }}</p>
            <p><strong>Experience:</strong> {{ profile.experience }} years</p>
            <p><strong>City:</strong> {{ profile.city }}</p>
            <p><strong>Base Price:</strong> ₹{{ profile.base_price }}/hr</p>
            <!-- <p><strong>Availability:</strong> {{ profile.availability }}</p> -->
            <span class="badge" :class="profile.profile_verified ? 'badge-success' : 'badge-warning'">
              {{ profile.profile_verified ? 'Verified' : 'Pending Verification' }}
            </span>
          </div>
          <button class="btn btn-edit" @click="editMode = true">Edit Profile</button>
        </div>
      </transition>

      <!-- Edit Profile Form -->
    <transition name="fade">
      <div v-if="editMode" class="edit-profile-form">
        <h5>Edit Profile</h5>
        <form @submit.prevent="updateProfile">
          <label>Name:</label>
          <input type="text" v-model="profile.name" required />
          
          <label>Service Type:</label>
          <input type="text" v-model="profile.service_type" required />
          
          <label>Experience (years):</label>
          <input type="number" v-model="profile.experience" required />
          
          <label>City:</label>
          <input type="text" v-model="profile.city" required />
          
          <label>Base Price (₹/hr):</label>
          <input type="number" v-model="profile.base_price" required />
          
          <button type="submit" class="btn btn-save">Save Changes</button>
          <button type="button" class="btn btn-cancel" @click="editMode = false">Cancel</button>
        </form>
      </div>
    </transition>
  
      <!-- Packages Section -->
      <div v-if="!loading">
        <h5 class="section-title">New Packages Available</h5>
        <ul class="list-group">
          <li v-for="pkg in availablePackages" :key="pkg.id" class="list-group-item">
            {{ pkg.name }}
            <button class="btn btn-apply" @click="applyForPackage(pkg.id)" :disabled="applyingPackageId === pkg.id">
              {{ applyingPackageId === pkg.id ? "Applying..." : "Apply" }}
            </button>
          </li>
        </ul>
  
        <h5 class="section-title">My Package Requests</h5>
        <ul class="list-group">
          <li v-for="req in appliedPackages" :key="req.id" class="list-group-item">
            {{ req.package_name }} - <span class="badge badge-pending">{{ req.status }}</span>
          </li>
        </ul>
  
        <h5 class="section-title">Joined Packages</h5>
        <ul class="list-group">
          <li v-for="joined in joinedPackages" :key="joined.id" class="list-group-item">
            {{ joined.name }} - <span class="badge badge-joined">Joined</span>
          </li>
        </ul>
      </div>
  
      <!-- Loading State -->
      <transition name="fade">
        <div v-if="loading" class="loading-container">
          <div class="spinner"></div>
          <p>Loading data, please wait...</p>
        </div>
      </transition>
    </div>
  </template>
  
  
  <script>
  import axios from 'axios';
  
  export default {
    data() {
      return {
        profile: null,
        editMode: false,
        availablePackages: [],
        appliedPackages: [],
        joinedPackages: [],
        applyingPackageId: null,
        loading: true,
        defaultAvatar: "https://via.placeholder.com/150", // Default avatar image
      };
    },
    methods: {
      async fetchProfessionalProfile() {
        try {
          const token = localStorage.getItem("token");
          if (!token) {
            alert("Authentication required. Please log in again.");
            return;
          }
  
          const headers = { Authorization: `Bearer ${token}` };
          const response = await axios.get('http://127.0.0.1:5000/dashboard/professional', { headers });
  
          this.profile = response.data.professional_info;
        } catch (error) {
          console.error("Error fetching professional profile:", error);
          alert(error.response?.data?.message || "Failed to load profile.");
        }
      },
      async updateProfile() {
        try {
          const token = localStorage.getItem("token");
          if (!token) {
            alert("Authentication required. Please log in again.");
            return;
          }
          const headers = { Authorization: `Bearer ${token}` };
          await axios.put('http://127.0.0.1:5000/dashboard/professional/update', this.profile, { headers });
          alert("Profile updated successfully!");
          this.editMode = false;
          await this.fetchProfessionalProfile();
        } catch (error) {
          console.error("Error updating profile:", error);
          alert("Failed to update profile.");
        }
      },
      async fetchPackages() {
        try {
          const token = localStorage.getItem("token");
          if (!token) {
            alert("Authentication required. Please log in again.");
            return;
          }
  
          const headers = { Authorization: `Bearer ${token}` };
  
          const [availableRes, appliedRes, joinedRes] = await Promise.all([
            axios.get('http://127.0.0.1:5000/api/professionals/packages/available', { headers }),
            axios.get('http://127.0.0.1:5000/api/professionals/packages/my-requests', { headers }),
            axios.get('http://127.0.0.1:5000/api/professionals/packages/joined', { headers })
          ]);
  
          this.availablePackages = availableRes.data;
          this.appliedPackages = appliedRes.data;
          this.joinedPackages = joinedRes.data;
        } catch (error) {
          console.error("Error fetching package data:", error);
          alert(error.response?.data?.message || "Failed to fetch packages.");
        }
      },
  
      async applyForPackage(packageId) {
        this.applyingPackageId = packageId;
  
        try {
          const token = localStorage.getItem("token");
          if (!token) {
            alert("Authentication required. Please log in again.");
            this.applyingPackageId = null;
            return;
          }
  
          await axios.post(
            'http://127.0.0.1:5000/api/professionals/packages/apply',
            { package_id: packageId },
            { headers: { Authorization: `Bearer ${token}` } }
          );
  
          alert("Package applied successfully!");
          await this.fetchPackages();
        } catch (error) {
          console.error("Error applying for package:", error);
          alert(error.response?.data?.message || "Failed to apply for package.");
        } finally {
          this.applyingPackageId = null;
        }
      }
    },
    async mounted() {
      await this.fetchProfessionalProfile();
      await this.fetchPackages();
      this.loading = false;
    }
  };
  </script>
  
  <style scoped>
  /* General Styling */
.container {
  max-width: 800px;
  margin: auto;
  padding: 20px;
  font-family: "Poppins", sans-serif;
}

/* Fade Animation */
.fade-enter-active, .fade-leave-active {
  transition: opacity 0.5s ease-in-out;
}
.fade-enter, .fade-leave-to {
  opacity: 0;
}

/* Profile Card */
.profile-card {
  background: linear-gradient(to right, #6a11cb, #2575fc);
  color: white;
  border-radius: 12px;
  padding: 20px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
  text-align: center;
  transition: transform 0.3s ease-in-out;
}
.profile-card:hover {
  transform: scale(1.02);
}

/* Profile Image */
.profile-img {
  width: 110px;
  height: 110px;
  border-radius: 50%;
  object-fit: cover;
  border: 4px solid white;
  transition: transform 0.3s ease-in-out;
}
.profile-img:hover {
  transform: rotate(5deg);
}

/* Profile Details */
.profile-details {
  text-align: left;
  margin-top: 15px;
}

/* Badges */
.badge {
  display: inline-block;
  padding: 6px 12px;
  font-size: 14px;
  border-radius: 20px;
  font-weight: bold;
  text-transform: uppercase;
}
.badge-success {
  background-color: #28a745;
  color: white;
}
.badge-warning {
  background-color: #ffc107;
  color: black;
}
.badge-pending {
  background: #ffcc00;
  color: black;
}
.badge-joined {
  background: #007bff;
  color: white;
}

/* Sections */
.section-title {
  margin-top: 25px;
  font-size: 20px;
  font-weight: 600;
  color: #444;
  text-transform: uppercase;
  border-bottom: 2px solid #ddd;
  padding-bottom: 5px;
}

/* List Group */
.list-group {
  list-style: none;
  padding: 0;
}
.list-group-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: #f8f9fa;
  padding: 12px;
  border-radius: 8px;
  margin-bottom: 8px;
  transition: all 0.3s ease-in-out;
}
.list-group-item:hover {
  background: #e9ecef;
  transform: translateX(5px);
}

/* Apply Button */
.btn-apply {
  background: linear-gradient(45deg, #ff416c, #ff4b2b);
  color: white;
  border: none;
  padding: 8px 12px;
  font-size: 14px;
  font-weight: bold;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.3s ease-in-out;
}
.btn-apply:hover {
  background: linear-gradient(45deg, #ff4b2b, #ff416c);
  transform: scale(1.1);
}

/* Loading Animation */
.loading-container {
  text-align: center;
  margin-top: 40px;
}
.spinner {
  width: 50px;
  height: 50px;
  border: 6px solid rgba(0, 0, 0, 0.1);
  border-top-color: #007bff;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: auto;
}
@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.edit-profile-form {
  background: #fff;
  padding: 20px;
  border-radius: 12px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
  margin-top: 20px;
}
.edit-profile-form h5 {
  margin-bottom: 15px;
}
.edit-profile-form input {
  width: 100%;
  padding: 8px;
  margin-bottom: 10px;
  border: 1px solid #ddd;
  border-radius: 6px;
}
.btn-save {
  background: #28a745;
  color: white;
  padding: 8px 12px;
  border: none;
  cursor: pointer;
  border-radius: 6px;
}
.btn-cancel {
  background: #dc3545;
  color: white;
  padding: 8px 12px;
  border: none;
  cursor: pointer;
  border-radius: 6px;
  margin-left: 10px;
}
.btn-edit {
  margin-top: 10px;
  background: #007bff;
  color: white;
  padding: 8px 12px;
  border: none;
  cursor: pointer;
  border-radius: 6px;
}
  </style>
  