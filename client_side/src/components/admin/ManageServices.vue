<template>
  
  <div class="admin-container">
    <AdminNavbar />

    <h5 class="text-center">Update/Delete Categories, Services and Packages.</h5>

    <div v-if="loading" class="text-center mt-4">
      <span class="spinner-border"></span> Loading...
    </div>

    <div v-if="!loading">
      <!-- Categories Section -->
      <section class="section">
        <h4>Categories</h4>
        <ul class="list-group">
          <li v-for="category in categories" :key="category.id" class="list-item">
            <img v-if="category.picture" :src="category.picture" alt="Category Image" class="thumbnail" />
            <span>{{ category.name }}</span>
            <div class="action-buttons">
              <button class="btn btn-warning" @click="openEditModal('category', category)">Edit</button>
              <button class="btn btn-danger" @click="deleteItem('service-categories', category.id)">Delete</button>
            </div>
          </li>
        </ul>
      </section>

      <!-- Services Section -->
      <section class="section">
        <h4>Services</h4>
        <ul class="list-group">
          <li v-for="service in services" :key="service.id" class="list-item">
            <span>{{ service.name }} </span><span>{{ service.category || 'No Category' }}</span> <span>₹{{ service.base_price }}</span>
            <div class="action-buttons">
              <button class="btn btn-warning" @click="openEditModal('service', service)">Edit</button>
              <button class="btn btn-danger" @click="deleteItem('services', service.id)">Delete</button>
            </div>
          </li>
        </ul>
      </section>

      <!-- Packages Section -->
      <section class="section">
        <h4>Packages</h4>
        <ul class="list-group">
          <li v-for="pkg in packages" :key="pkg.id" class="list-item">
            <img v-if="pkg.picture" :src="pkg.picture" alt="Package Image" class="thumbnail" />
            <p>{{ pkg.name }} - ₹{{ pkg.base_price }} ({{ pkg.package_type }})</p> <br>
            <p>{{ pkg.description }}</p>
            <div class="action-buttons">
              <button class="btn btn-warning" @click="openEditModal('package', pkg)">Edit</button>
              <button class="btn btn-danger" @click="deleteItem('packages', pkg.id)">Delete</button>
            </div>
          </li>
        </ul>
      </section>
    </div>

    <!-- Edit Modal -->
<div v-if="showEditModal" class="modal-overlay">
  <div class="modal-content">
    <h4>Edit {{ editType }}</h4>

    <!-- Name (Common for all types) -->
    <input v-model="editData.name" class="form-control" placeholder="Name" />

    <!-- Category Dropdown (For Service & Package) -->
    <select v-if="editType === 'service' || editType === 'package'" v-model="editData.category_id" class="form-control">
      <option disabled value="">Select Category</option>
      <option v-for="category in categories" :key="category.id" :value="category.id">
        {{ category.name }}
      </option>
    </select>

    <!-- Base Price & Time Required (For Service & Package) -->
    <input v-if="editType === 'service' || editType === 'package'" v-model="editData.base_price" class="form-control" placeholder="Base Price" />
    <input v-if="editType === 'service' || editType === 'package'" v-model="editData.time_required" class="form-control" placeholder="Time Required" />

    <!-- Package Type Dropdown (For Packages Only) -->
    <select v-if="editType === 'package'" v-model="editData.package_type" class="form-control">
      <option disabled value="">Select Package Type</option>
      <option value="Basic">Basic</option>
      <option value="Premium">Premium</option>
      <option value="Deep">Deep</option>
    </select>

    <!-- Description (For Packages Only) -->
    <textarea v-if="editType === 'package'" v-model="editData.description" class="form-control" placeholder="Description"></textarea>

    <!-- Save & Cancel Buttons -->
    <button class="btn btn-primary" @click="updateItem">Save</button>
    <button class="btn btn-secondary" @click="closeEditModal">Cancel</button>
  </div>
</div>

  </div>
</template>

<script>
import axios from "axios";
import AdminNavbar from "./AdminNavbar.vue";

export default {
  components: {
    AdminNavbar,  // Make sure it's listed here
  },
  data() {
    return {
      categories: [],
      services: [],
      packages: [],
      loading: true,
      showEditModal: false,
      editType: "",
      editData: {},
    };
  },
  methods: {
    async fetchData() {
      try {
        const token = localStorage.getItem("token");
        const headers = { Authorization: `Bearer ${token}` };

        const [categoriesRes, servicesRes, packagesRes] = await Promise.all([
          axios.get("http://127.0.0.1:5000/api/service-categories", { headers }),
          axios.get("http://127.0.0.1:5000/api/services", { headers }),
          axios.get("http://127.0.0.1:5000/api/packages", { headers }),
        ]);

        this.categories = categoriesRes.data.categories;
        this.services = servicesRes.data.services;
        this.packages = packagesRes.data.packages;
      } catch (error) {
        console.error("Error fetching data:", error);
        alert("Failed to fetch data.");
      } finally {
        this.loading = false;
      }
    },

    async deleteItem(type, itemId) {
      if (!confirm("Are you sure you want to delete this item?")) return;
      try {
        const token = localStorage.getItem("token");
        const headers = { Authorization: `Bearer ${token}` };
        await axios.delete(`http://127.0.0.1:5000/api/${type}/${itemId}`, { headers });
        alert(`${type} deleted successfully.`);
        this.fetchData();
      } catch (error) {
        console.error("Error deleting item:", error);
        alert("Failed to delete.");
      }
    },
    openEditModal(type, item) {
    this.editType = type;
    this.editData = { ...item };  // Load existing data into modal
    
    if (type === 'service' || type === 'package') {
      this.fetchCategories();  // Load categories only if editing service or package
    }

    this.showEditModal = true;
  },

  fetchCategories() {
    axios.get('http://127.0.0.1:5000/api/service-categories')  // Fetch categories dynamically
      .then(response => {
        this.categories = response.data.categories;
      })
      .catch(error => {
        console.error('Error fetching categories:', error);
      });
  },

    closeEditModal() {
      this.showEditModal = false;
      this.editData = {};
    },

    async updateItem() {
      try {
        const token = localStorage.getItem("token");
        const headers = { Authorization: `Bearer ${token}` };
        await axios.put(`http://127.0.0.1:5000/api/${this.editType}s/${this.editData.id}`, this.editData, { headers });
        alert(`${this.editType} updated successfully.`);
        this.fetchData();
        this.closeEditModal();
      } catch (error) {
        console.error("Error updating item:", error);
        alert("Failed to update.");
      }
    },
  },
  mounted() {
    this.fetchData();
  },
};
</script>

<style scoped>
.admin-container {
  margin: auto;
  padding: 20px;
  background: #0b0f19;
  border-radius: 8px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
}

.section {
  margin: 30px;
  /* max-width: 94%; */
  padding: 15px;
  background: #0b0f19;
  border-radius: 8px;
  box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
}

h4 {
  color: #ffffff;
  font-weight: bold;
  margin-bottom: 10px;
}
h5 {
  margin-top: 3rem;
  color: #fff;
  margin-bottom: 1rem;
}

.list-group {
  list-style: none;
  padding: 0;
}

.list-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: #1a1f2b;  /* Dark background */
  color: #fff; 
  padding: 12px;
  margin-bottom: 8px;
  border-radius: 6px;
  transition: transform 0.3s ease-in-out, box-shadow 0.3s ease-in-out;
}

.list-item:hover {
  transform: scale(1.02);
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.15);
}

.thumbnail {
  width: 50px;
  height: 50px;
  border-radius: 6px;
  margin-right: 10px;
}

.action-buttons {
  display: flex;
  gap: 10px;
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
}

.modal-content {
  background: #1a1f2b;  /* Dark background */
  color: #fff;
  padding: 20px;
  border-radius: 8px;
  width: 400px;
  text-align: center;
}

.btn {
  padding: 6px 12px;
  font-size: 14px;
  border-radius: 5px;
}
</style>
