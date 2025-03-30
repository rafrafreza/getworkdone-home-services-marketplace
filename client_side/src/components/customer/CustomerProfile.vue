<template>
  <div class="container profile-container">
    <div class="row justify-content-center">
      <div class="col-lg-8">
        <div v-if="loading" class="text-center mt-4">
          <div class="spinner-border text-primary" role="status">
            <span class="visually-hidden">Loading...</span>
          </div>
        </div>

        <div v-else-if="errorMessage" class="alert alert-danger text-center">
          {{ errorMessage }}
        </div>

        <div v-else class="card profile-card shadow-lg">
          <div class="card-body text-center">
            <div class="profile-image-container">
              <img v-if="customer.profile_picture" :src="customer.profile_picture" class="profile-img" alt="Profile Picture" />
            </div>
            <h2 class="mt-3">{{ customer.name }}</h2>
            <p class="text-muted">{{ customer.city }}, {{ customer.pin_code }}</p>
            
            <hr />

            <div class="info-section">
              <p><strong>📞 Phone:</strong> {{ customer.phone }}</p>
              <p><strong>🏡 Address:</strong> {{ customer.address }}</p>
              <p><strong>📅 Joined:</strong> {{ formatDate(customer.created_at) }}</p>
            </div>

            <button class="btn btn-primary mt-3" @click="openEditModal">Edit Profile</button>
          </div>
        </div>
      </div>
    </div>
  </div>

  <!-- Edit Profile Modal -->
  <div v-if="showEditModal" class="modal fade show d-block" tabindex="-1" role="dialog">
    <div class="modal-dialog" role="document">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title">Update Profile</h5>
          <button type="button" class="btn-close" @click="closeEditModal"></button>
        </div>
        <div class="modal-body">
          <form @submit.prevent="updateProfile">
            <div class="mb-3">
              <label class="form-label">Name</label>
              <input type="text" class="form-control" v-model="updatedProfile.name" />
            </div>
            <div class="mb-3">
              <label class="form-label">Phone</label>
              <input type="text" class="form-control" v-model="updatedProfile.phone" />
            </div>
            <div class="mb-3">
              <label class="form-label">City</label>
              <input type="text" class="form-control" v-model="updatedProfile.city" />
            </div>
            <div class="mb-3">
              <label class="form-label">Pin Code</label>
              <input type="text" class="form-control" v-model="updatedProfile.pin_code" />
            </div>
            <div class="mb-3">
              <label class="form-label">Address</label>
              <textarea class="form-control" v-model="updatedProfile.address"></textarea>
            </div>
            <button type="submit" class="btn btn-success">Save Changes</button>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      customer: null,
      loading: true,
      errorMessage: null,
      showEditModal: false,
      updatedProfile: {
        name: "",
        phone: "",
        city: "",
        pin_code: "",
        address: ""
      }
    };
  },
  methods: {
    async fetchCustomerProfile() {
      try {
        const token = localStorage.getItem("token");
        const response = await fetch("http://127.0.0.1:5000/dashboard/customer", {
          headers: { Authorization: `Bearer ${token}` }
        });
        const data = await response.json();

        if (response.ok) {
          this.customer = data.customer_info;
        } else {
          this.errorMessage = data.message || "Failed to fetch profile.";
        }
      } catch (error) {
        this.errorMessage = "Error fetching profile. Please try again.";
        console.error(error);
      } finally {
        this.loading = false;
      }
    },
    formatDate(dateString) {
      return new Date(dateString).toLocaleDateString("en-US", { year: "numeric", month: "long", day: "numeric" });
    },
    openEditModal() {
      this.updatedProfile = { ...this.customer };
      this.showEditModal = true;
    },
    closeEditModal() {
      this.showEditModal = false;
    },
    async updateProfile() {
      try {
        const token = localStorage.getItem("token");
        const response = await fetch("http://127.0.0.1:5000/dashboard/customer/update", {
          method: "PUT",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`
          },
          body: JSON.stringify(this.updatedProfile)
        });
        const data = await response.json();
        if (response.ok) {
          this.customer = { ...this.updatedProfile };
          this.showEditModal = false;
        } else {
          alert(data.message || "Failed to update profile.");
        }
      } catch (error) {
        alert("Error updating profile. Please try again.");
        console.error(error);
      }
    }
  },
  mounted() {
    this.fetchCustomerProfile();
  }
};
</script>

<style scoped>
.profile-container {
  margin-top: 30px;
}
.profile-card {
  border-radius: 12px;
  padding: 20px;
  background: linear-gradient(to right, #f8f9fa, #e9ecef);
}
.profile-image-container {
  display: flex;
  justify-content: center;
}
.profile-img {
  width: 120px;
  height: 120px;
  border-radius: 50%;
  border: 4px solid #007bff;
}
.info-section p {
  font-size: 1.1rem;
  margin-bottom: 8px;
}
.modal {
  background: rgba(0, 0, 0, 0.5);
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
}
.modal-content {
  background: white;
  padding: 20px;
  border-radius: 8px;
}
</style>
