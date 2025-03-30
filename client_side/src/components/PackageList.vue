<template>
  <div class="card package-card">
    <h5 class="title">Available Packages</h5>

    <!-- 🔍 Search, Category & Sorting Section -->
    <div class="controls">
      <input 
        type="text" 
        v-model="searchPackage" 
        class="form-control search-box" 
        placeholder="Search packages..."
      />
      <select v-model="selectedCategory" class="form-select filter-box">
        <option value="">All Categories</option>
        <option v-for="category in categories" :key="category.id" :value="category.id">
          {{ category.name }}
        </option>
      </select>
      <select v-model="selectedFilter" class="form-select filter-box">
        <option value="">Filter By</option>
        <option value="Basic">Basic</option>
        <option value="Deep">Deep</option>
        <option value="Premium">Premium</option>
      </select>
      <button class="btn btn-primary sort-btn" @click="sortByPrice">
        Sort by Price 
        <i class="fas" :class="sortOrder === 'asc' ? 'fa-arrow-up' : 'fa-arrow-down'"></i>
      </button>
      <button class="btn btn-secondary reset-btn" @click="resetFilters">Reset Filters</button>
    </div>

    <!-- 📦 Package List -->
    <div class="list-group package-list">
      <div 
        v-for="(packageItem, index) in filteredPackages" 
        :key="index" 
        class="list-group-item package-item"
        @click="openModal(packageItem)"
      >
        <img :src="packageItem.picture || `https://picsum.photos/80/80?random=${index + 10}`" class="package-img" />
        <div class="package-details">
          <span class="package-name">{{ packageItem.name }}</span>
          <span class="package-category">Category: {{ packageItem.category_name }}</span>
          <span class="package-price">₹{{ packageItem.base_price }}</span>
          <span class="package-description">{{ packageItem.description }}</span>
        </div>
        <button class="btn btn-success book-btn" >Book Now</button>
      </div>

      <div v-if="filteredPackages.length === 0" class="text-center mt-4">
        <p class="no-results">No packages found matching your criteria.</p>
      </div>
    </div>

    <!-- 📌 Package Details Modal -->
    <div v-if="showModal" class="modal-overlay">
      <div class="modal-content">
        <span class="close-btn" @click="closeModal">&times;</span>
        <h3>{{ selectedPackage.name }}</h3>
        <img :src="selectedPackage.picture || `https://picsum.photos/200/200?random=5`" class="modal-img" />
        <p><strong>Category:</strong> {{ selectedPackage.category_id }}</p>
        <p><strong>Price:</strong> ₹{{ selectedPackage.base_price }}</p>
        <p><strong>Description:</strong> {{ selectedPackage.description }}</p>

        <button class="btn btn-primary book-now-btn" @click="openBookingForm">
          Book Now
        </button>

        <!-- 📋 Booking Form -->
        <div v-if="showBookingForm" class="booking-form">
          <h4>Book Package</h4>
          <input type="datetime-local" v-model="bookingDateTime" class="form-control mt-2" required />
          <button class="btn btn-success mt-2" @click="submitBooking">Submit Booking</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      searchPackage: "",
      selectedCategory: "",
      selectedFilter: "",
      sortOrder: "asc",
      packages: [],
      categories: [],
      showModal: false,
      selectedPackage: {},
      showBookingForm: false,
      customerName: "",
      customerEmail: "",
      bookingDateTime: "",
    };
  },
  computed: {
    filteredPackages() {
      let result = this.packages.filter(pkg => 
        pkg.name.toLowerCase().includes(this.searchPackage.toLowerCase())
      );

      if (this.selectedCategory) {
        result = result.filter(pkg => pkg.category_id === this.selectedCategory);
      }

      if (this.selectedFilter) {
        result = result.filter(pkg => pkg.package_type === this.selectedFilter);
      }

      return result.map(pkg => ({
        ...pkg,
        category_name: this.categories.find(cat => cat.id === pkg.category_id)?.name || "Unknown"
      }));
    }
  },
  methods: {
    async fetchPackages() {
      try {
        const [packagesResponse, categoriesResponse] = await Promise.all([
          axios.get('http://127.0.0.1:5000/api/packages'),
          axios.get('http://127.0.0.1:5000/api/service-categories') // Fetch category data
        ]);

        this.packages = packagesResponse.data.packages;
        console.log(this.packages)
        this.categories = categoriesResponse.data.categories;
        console.log(this.categories)
      } catch (error) {
        console.error("Error fetching data:", error);
      }
    },
    sortByPrice() {
      this.sortOrder = this.sortOrder === "asc" ? "desc" : "asc";
      this.packages.sort((a, b) => 
        this.sortOrder === "asc" ? a.base_price - b.base_price : b.base_price - a.base_price
      );
    },
    resetFilters() {
      this.searchPackage = "";
      this.selectedCategory = "";
      this.selectedFilter = "";
    },
    openModal(packageItem) {
      this.selectedPackage = packageItem;
      this.showModal = true;
      this.showBookingForm = false;
    },
    closeModal() {
      this.showModal = false;
    },
    openBookingForm() {
      const token = localStorage.getItem("token");
      if (!token) {
        alert("Please log in to book a package.");
        return;
      }
      this.showBookingForm = true;
    },
    async submitBooking() {
      const token = localStorage.getItem("token");
      if (!token) {
        alert("Please log in to book a package.");
        return;
      }
      if (!this.bookingDateTime) {
        alert("Please select a date and time.");
        return;
      }

      // const requestData = {
      //   service_id: this.selectedPackage.id, // Assuming 'id' is the service_id
      //   customer_id: customerId,
      //   service_dateTime: this.bookingDateTime.replace("T", " "), // Formatting for API
      // };
      

      try {
          const response = await axios.get("http://127.0.0.1:5000/dashboard/customer", {
              headers: { Authorization: `Bearer ${token}` }
          });
          const customerId = response.data.customer_id;
          
          await axios.post('http://127.0.0.1:5000/api/customers/service-requests/create', {
              package_id: this.selectedPackage.id,
              customer_id: customerId,
              service_dateTime: this.bookingDateTime.replace("T", " "), // Formatting for API
          }, {
              headers: { Authorization: `Bearer ${token}` }
          });

        alert("Service request created successfully!");

        this.showModal = false; // Close modal after successful booking
        this.showBookingForm = false;
      } catch (error) {
        console.error("Error submitting booking:", error.response?.data || error);
        alert(error.response?.data?.error || "Something went wrong. Please try again.");
      }
    },
    closeModal() {
      this.showModal = false;
      this.showBookingForm = false;
    },
  },
  mounted() {
    this.fetchPackages();
  }
};
</script>



<style scoped>
/* 📦 Package Card */
.package-card {
  background: #ffffff;
  border-radius: 12px;
  padding: 1.5rem;
  box-shadow: 0px 6px 15px rgba(0, 0, 0, 0.1);
  max-width: 1400px;
  margin: 30px auto;
}

/* 🏆 Title */
.title {
  text-align: center;
  font-size: 1.3rem;
  color: #28a745;
  font-weight: bold;
  margin-bottom: 1rem;
}

/* 🔍 Controls (Search + Category + Filter + Sort) */
.controls {
  display: flex;
  gap: 10px;
  justify-content: center;
  flex-wrap: wrap;
}

.search-box, .filter-box {
  flex: 1;
  min-width: 160px;
}

.sort-btn, .reset-btn {
  white-space: nowrap;
}

/* 📦 Package List */
.package-list {
  margin-top: 20px;
}

/* 🎭 Package Item */
.package-item {
  display: flex;
  align-items: center;
  margin-bottom: 4px;
  padding: 15px;
  border-radius: 8px;
  transition: transform 0.2s ease-in-out;
}

.package-item:hover {
  transform: translateY(-3px);
}

/* 🖼️ Package Image */
.package-img {
  border-radius: 50%;
  width: 70px;
  height: 70px;
  object-fit: cover;
  margin-right: 15px;
}

/* 📑 Package Details */
.package-details {
  flex: 1;
}

.package-name {
  font-size: 16px;
  font-weight: bold;
  color: #333;
  display: block;
}

.package-category {
  font-size: 14px;
  color: #666;
  display: block;
}

.package-price {
  font-size: 14px;
  font-weight: bold;
  color: #dc3545;
}

.package-description {
  font-size: 14px;
  color: #444;
  display: block;
  margin-top: 5px;
}

/* 🎟️ Book Now Button */
.book-btn {
  padding: 8px 15px;
  font-size: 14px;
}

/* 📌 Modal Styles */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  z-index: 1050; /* Ensure it's higher than other components */
  display: flex;
  justify-content: center;
  align-items: center;
}

.modal-content {
  background: white;
  padding: 20px;
  border-radius: 8px;
  max-width: 600px;
  width: 100%;
  z-index: 1051; /* Higher than the overlay */
  position: relative;
}

.modal-img {
  width: 100%;
  max-height: 200px;
  object-fit: cover;
  border-radius: 8px;
  margin-bottom: 10px;
}

.close-btn {
  position: absolute;
  top: 10px;
  right: 10px;
  font-size: 24px;
  cursor: pointer;
}

.book-now-btn {
  width: 100%;
  margin-top: 10px;
}

.booking-form {
  margin-top: 15px;
}
</style>
