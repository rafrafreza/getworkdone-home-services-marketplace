<template>
  <div class="admin-container">
    <AdminNavbar />
    <div class="container mt-4">
      <h2 class="text-center mb-4">👥 User Management</h2>

      <!-- Professionals Table -->
      <div v-if="professionals.length" class="card mb-4 custom-card">
        <div class="card-header bg-primary text-white">📌 Professionals</div>
        <div class="card-body table-responsive">
          <table class="table table-hover custom-table">
            <thead class="table-dark">
              <tr>
                <th>Profile</th>
                <th>Name</th>
                <th>Phone</th>
                <th>Email</th>
                <th>Service Type</th>
                <th>Experience</th>
                <th>Status</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="professional in professionals" :key="professional.id">
                <td><img :src="professional.profile_picture" class="profile-pic" /></td>
                <td>{{ professional.fname }}</td>
                <td>{{ professional.phone }}</td>
                <td>{{ professional.email }}</td>
                <td>{{ professional.service_type }}</td>
                <td>{{ professional.experience }} yrs</td>
                <td :class="{'text-danger fw-bold': professional.blocked}">
                  {{ professional.blocked ? 'Blocked' : 'Active' }}
                </td>
                <td>
                  <button @click="toggleBlock(professional)" class="btn" :class="professional.blocked ? 'btn-success' : 'btn-danger'">
                    {{ professional.blocked ? 'Unblock' : 'Block' }}
                  </button>
                  <button @click="deleteUser(professional.id)" class="btn btn-dark ms-2">🗑 Delete</button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- Customers Table -->
      <div v-if="customers.length" class="card custom-card">
        <div class="card-header bg-success text-white">🛒 Customers</div>
        <div class="card-body table-responsive">
          <table class="table table-hover custom-table">
            <thead class="table-dark">
              <tr>
                <th>Profile</th>
                <th>Name</th>
                <th>Phone</th>
                <th>City</th>
                <th>Pin Code</th>
                <th>Status</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="customer in customers" :key="customer.id">
                <td><img :src="customer.profile_picture" class="profile-pic" /></td>
                <td>{{ customer.fname }}</td>
                <td>{{ customer.phone }}</td>
                <td>{{ customer.city }}</td>
                <td>{{ customer.pin_code }}</td>
                <td :class="{'text-danger fw-bold': customer.blocked}">
                  {{ customer.blocked ? 'Blocked' : 'Active' }}
                </td>
                <td>
                  <button @click="toggleBlock(customer)" class="btn" :class="customer.blocked ? 'btn-success' : 'btn-danger'">
                    {{ customer.blocked ? 'Unblock' : 'Block' }}
                  </button>
                  <button @click="deleteUser(customer.id)" class="btn btn-dark ms-2">🗑 Delete</button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import AdminNavbar from './AdminNavbar.vue';

export default {
  components: {
    AdminNavbar,
  },
  data() {
    return {
      users: [],
      professionals: [],
      customers: [],
    };
  },
  methods: {
    async fetchUsers() {
      try {
        const response = await axios.get('http://127.0.0.1:5000/api/admin/users');
        this.users = response.data;
        this.professionals = this.users.filter(user => user.role === 'Professional');
        this.customers = this.users.filter(user => user.role === 'Customer');
      } catch (error) {
        console.error("Error fetching users", error);
      }
    },
    async toggleBlock(user) {
      try {
        await axios.put(`http://127.0.0.1:5000/api/admin/users/block/${user.id}`);
        user.blocked = !user.blocked;
      } catch (error) {
        console.error("Error blocking user", error);
      }
    },
    async deleteUser(id) {
      if (!confirm("Are you sure you want to delete this user?")) return;
      try {
        await axios.delete(`http://127.0.0.1:5000/api/admin/users/delete/${id}`);
        this.professionals = this.professionals.filter(user => user.id !== id);
        this.customers = this.customers.filter(user => user.id !== id);
      } catch (error) {
        console.error("Error deleting user", error);
      }
    },
  },
  mounted() {
    this.fetchUsers();
  }
};
</script>

<style scoped>
.admin-container {
  padding: 20px;
  background: #0b0f19; /* Consistent Dark Background */
  border-radius: 8px;
  min-height: 100vh;
  color: white;
}

.custom-card {
  background: #1a1f2e !important;
  color: white;
  border: none;
}

.custom-table {
  background: #121826;
  color: white;
}

.table-dark th {
  background: #0d1117;
  color: white;
}

.profile-pic {
  width: 40px;
  height: 40px;
  border-radius: 50%;
}
</style>
