<template>
    <div class="container mt-4">
      <h2 class="mb-3">Add New Entries</h2>
      <ul class="nav nav-tabs">
        <li class="nav-item">
          <a class="nav-link" :class="{ active: activeTab === 'category' }" @click="activeTab = 'category'">Add Category</a>
        </li>
        <li class="nav-item">
          <a class="nav-link" :class="{ active: activeTab === 'service' }" @click="activeTab = 'service'">Add Service</a>
        </li>
        <li class="nav-item">
          <a class="nav-link" :class="{ active: activeTab === 'package' }" @click="activeTab = 'package'">Add Package</a>
        </li>
      </ul>
      
      <div class="tab-content mt-3">
        <div v-if="activeTab === 'category'">
            <h4>Add New Category</h4>
            <input type="text" class="form-control" v-model="categoryName" placeholder="Enter category name" required />
            <input type="file" class="form-control mt-2" @change="handleCategoryFileUpload" />
            <button class="btn btn-primary mt-2" @click="addCategory" :disabled="!categoryName">
              Add Category
            </button>
        </div>


        <div v-if="activeTab === 'service'">
          <h4>Add New Service</h4>
          <input type="text" class="form-control" v-model="serviceName" placeholder="Service Name" required />
          <input type="number" class="form-control mt-2" v-model="basePrice" placeholder="Base Price" required />
          <input type="text" class="form-control mt-2" v-model="timeRequired" placeholder="Time Required" required />
          <input type="text" class="form-control mt-2" v-model="description" placeholder="Description..." />
          <select class="form-control mt-2" v-model="categoryId" required>
            <option value="" disabled>Select a category</option>
            <option v-for="category in categories" :key="category.id" :value="category.id">
              {{ category.name }}
            </option>
          </select>
          <button class="btn btn-primary mt-2" @click="addService" :disabled="!serviceName || !basePrice || !timeRequired || !categoryId">
            Add Service
          </button>
        </div>

      <div v-if="activeTab === 'package'">
        <h4>Add New Package</h4>
        <input type="text" class="form-control" v-model="packageName" placeholder="Package Name" required />
        <input type="text" class="form-control mt-2" v-model="description" placeholder="Description" required />
        <input type="number" class="form-control mt-2" v-model="packagePrice" placeholder="Base Price" required />
        <input type="text" class="form-control mt-2" v-model="packageTime" placeholder="Time Required" required />
        <select class="form-control mt-2" v-model="categoryId" required>
          <option value="" disabled>Select a category</option>
          <option v-for="category in categories" :key="category.id" :value="category.id">
            {{ category.name }}
          </option>
        </select>
        <select class="form-control mt-2" v-model="packageType" required>
          <option value="" disabled>Select Package Type</option>
          <option value="Basic">Basic</option>
          <option value="Premium">Premium</option>
          <option value="Deep">Deep</option>
        </select>
        <input type="file" class="form-control mt-2" @change="handleFileUpload" />
        <button class="btn btn-primary mt-2" @click="addPackage"
          :disabled="!packageName || !description || !packagePrice || !packageTime || !categoryId || !packageType">
          Add Package
        </button>
      </div>
    </div>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  export default {
    data() {
      return {
        activeTab: 'category',
        categoryName: '',
        serviceName: '',
        basePrice: '',
        timeRequired: '',
        categoryId: '',
        packageName: '',
        description: '',
        packagePrice: '',
        packageTime: '',
        packageType: '',
        pictureBase64: '',
        categoryPictureBase64: '',  // Store category image as Base64
        categories: []
      };
    },
    mounted() {
      this.fetchCategories();
    },
    methods: {
  getAuthHeaders() {
    const token = localStorage.getItem("token");
    return {
      headers: { Authorization: `Bearer ${token}` }
    };
  },

  fetchCategories() {
  axios.get('http://127.0.0.1:5000/api/service-categories', {
    headers: { Authorization: `Bearer ${localStorage.getItem("token")}` }
  })
  .then(response => {
    this.categories = response.data.categories; // Access the "categories" array from response
    console.log(this.categories)
  })
  .catch(error => console.error(error));
},
handleCategoryFileUpload(event) {
    const file = event.target.files[0];
    if (file) {
      const reader = new FileReader();
      reader.onload = () => {
        this.categoryPictureBase64 = reader.result;  // Store Base64 image
      };
      reader.readAsDataURL(file);
    }
  },
  addCategory() {
  axios.post(
    'http://127.0.0.1:5000/api/service-categories',
    {
      name: this.categoryName,
      picture: this.categoryPictureBase64  // Sending picture as Base64
    },
    this.getAuthHeaders()
  )
  .then(() => {
    alert('Category added successfully');
    this.categoryName = '';
    this.categoryPictureBase64 = '';  // Reset image input
    this.fetchCategories();
  })
  .catch(error => console.error(error));
}
,

  addService() {
    axios.post(
      'http://127.0.0.1:5000/api/services',
      {
        name: this.serviceName,
        base_price: this.basePrice,
        time_required: this.timeRequired,
        description: this.description,
        category_id: this.categoryId
      },
      this.getAuthHeaders()
    )
    .then(() => {
      alert('Service added successfully');
      this.serviceName = this.basePrice = this.timeRequired = this.categoryId = '';
    })
    .catch(error => console.error(error));
  },
  handleFileUpload(event) {
      const file = event.target.files[0];
      if (file) {
        const reader = new FileReader();
        reader.onload = () => {
          this.pictureBase64 = reader.result;
        };
        reader.readAsDataURL(file);
      }
    },
  addPackage() {
    const payload = {
    name: this.packageName,
    description: this.description,
    base_price: this.packagePrice,
    time_required: this.packageTime,
    category_id: this.categoryId,
    package_type: this.packageType,
    picture: this.pictureBase64  // Sending picture as Base64
  };

  console.log("Sending Package Data:", payload); // Debugging log

    axios.post(
      'http://127.0.0.1:5000/api/packages',
      payload,
      this.getAuthHeaders()
    )
    .then(() => {
      alert('Package added successfully');
      this.packageName = this.packagePrice = this.packageTime = this.packageType = this.pictureBase64 = '';
    })
    .catch(error => {
      console.error("Error adding package:", error.response?.data || error.message);
    });
  }
}

  };
  </script>
  
<style scoped>
  .container {
    max-width: 600px;
  }
</style>
  