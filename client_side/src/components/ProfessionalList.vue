<template>
  <section class="top-professionals py-5">
    <div class="container">
      <h2 class="text-center section-title">Hire Professionals</h2>

      <div class="filter-bar d-flex flex-wrap justify-content-center mt-4">
        <input type="text" v-model="searchQuery" class="form-control search-box" placeholder="Search by name..." />
        <select v-model="selectedCategory" class="form-select filter-dropdown">
          <option value="">All Categories</option>
          <option v-for="category in uniqueCategories" :key="category" :value="category">{{ category }}</option>
        </select>
        <select v-model="sortOption" class="form-select filter-dropdown">
          <option value="price-desc">Sort by Price (High to Low)</option>
          <option value="price-asc">Sort by Price (Low to High)</option>
        </select>
        <!-- <select v-model="minRating" class="form-select filter-dropdown">
          <option value="">Filter by Rating</option>
          <option v-for="r in [3, 4, 4.5]" :key="r" :value="r">{{ r }} ⭐ & above</option>
        </select> -->
      </div>

      <div class="row justify-content-center mt-3">
        <div v-for="(pro, index) in filteredProfessionals" :key="index" class="col-12 col-sm-6 col-md-4 col-lg-3 col-xl-2 d-flex">
          <div class="card professional-card text-center flex-fill" @click="openModal(pro)">
            <div class="rating-badge">{{ pro.rating }} ⭐</div>
            <img :src="pro.profile_picture" alt="Professional" class="professional-img" />
            <div class="card-body">
              <h5 class="card-title profession">{{ pro.name }}</h5>
              <p class="category">{{ pro.service_type }}</p>
              <p class="price">₹{{ pro.base_price_per_hour }} / session</p>
            </div>
          </div>
        </div>
      </div>

      <div v-if="filteredProfessionals.length === 0" class="text-center mt-4">
        <p class="no-results">No professionals found matching your criteria.</p>
      </div>
    </div>

    <div v-if="showModal" class="modal-overlay" @click.self="closeModal">
      <div class="modal-content">
        <h3>{{ selectedPro.name }}</h3>
        <p><strong>Category:</strong> {{ selectedPro.service_type }}</p>
        <p><strong>Rating:</strong> {{ selectedPro.rating }} ⭐</p>
        <p><strong>Price:</strong> ₹{{ selectedPro.base_price_per_hour }} / session</p>
        <button class="btn hire-btn" @click="openBookingForm">Hire Now</button>
        <button class="btn close-btn" @click="closeModal">Close</button>
      </div>
    </div>

    <div v-if="showBookingForm" class="modal-overlay" @click.self="closeBookingForm">
      <div class="modal-content">
        <h3>Book {{ selectedPro.name }}</h3>
        <form @submit.prevent="bookProfessional">
          <!-- <input v-model="bookingData.customer_id" type="text" placeholder="Your ID" required /> -->
          <input v-model="bookingData.booking_date" type="date" required />
          <input v-model="bookingData.time_slot" type="text" placeholder="Time Slot" required />
          <input v-model="bookingData.price" type="number" readonly />
          <button type="submit" class="btn hire-btn">Confirm Booking</button>
          <button type="button" class="btn close-btn" @click="closeBookingForm">Cancel</button>
        </form>
      </div>
    </div>
  </section>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      searchQuery: "",
      selectedCategory: "",
      sortOption: "price-desc",
      minRating: "",
      professionals: [],
      showModal: false,
      showBookingForm: false,
      selectedPro: null,
      bookingData: {
        customer_id: "",
        professional_id: "",
        service_id: "",
        booking_date: "",
        time_slot: "",
        price: ""
      }
    };
  },
  computed: {
    uniqueCategories() {
      return [...new Set(this.professionals.map(pro => pro.service_type))];
    },
    filteredProfessionals() {
      let filtered = this.professionals.filter(pro =>
        pro.name.toLowerCase().includes(this.searchQuery.toLowerCase())
      );
      if (this.selectedCategory) filtered = filtered.filter(pro => pro.service_type === this.selectedCategory);
      if (this.minRating) filtered = filtered.filter(pro => pro.rating >= parseFloat(this.minRating));
      return this.sortOption === "price-desc"
        ? filtered.sort((a, b) => b.base_price_per_hour - a.base_price_per_hour)
        : filtered.sort((a, b) => a.base_price_per_hour - b.base_price_per_hour);
    }
  },
  methods: {
    async fetchProfessionals() {
      try {
        const response = await axios.get("http://127.0.0.1:5000/api/all_professionals");
        this.professionals = response.data;
      } catch (error) {
        console.error("Error fetching professionals:", error);
      }
    },
    openModal(pro) {
      this.selectedPro = pro;
      this.showModal = true;
    },
    closeModal() {
      this.showModal = false;
    },
    async openBookingForm() {
  const token = localStorage.getItem("token");
  if (!token) {
    alert("Please log in first.");
    window.location.href = "/login";
    return;
  }

  try {
    // Fetch customer ID
    const response = await axios.get("http://127.0.0.1:5000/dashboard/customer", {
      headers: { Authorization: `Bearer ${token}` }
    });

    const customerId = response.data.customer_id;
    if (!this.selectedPro) {
      console.error("No professional selected!");
      return;
    }

    console.log("Selected Professional:", this.selectedPro); // Debugging
    console.log("Category:", this.selectedPro.service_type); // Ensure this logs a valid category

    this.bookingData = {
      customer_id: customerId,
      professional_id: this.selectedPro.id,
      category: this.selectedPro.service_type || "", // Use category instead of service_id
      booking_date: "", 
      time_slot: "", 
      price: this.selectedPro.base_price_per_hour
    };

    this.showBookingForm = true;
    this.showModal = false;
  } catch (error) {
    console.error("Error fetching customer ID:", error);
    alert("Failed to fetch customer details. Please try again.");
  }
}

,
    closeBookingForm() {
      this.showBookingForm = false;
    },
    async bookProfessional() {
  const token = localStorage.getItem("token");
  if (!token) {
    alert("Please log in first.");
    window.location.href = "/login";
    return;
  }

  console.log("Booking Payload:", this.bookingData); // Debugging

  try {
    const response = await axios.post(
      "http://127.0.0.1:5000/api/customers/bookings/create",
      this.bookingData,
      {
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`
        }
      }
    );

    alert(response.data.message || "Booking successful!");
    this.closeBookingForm();
  } catch (error) {
    console.error("Error creating booking:", error);
    alert("Booking failed. Please try again.");
  }
}


  },
  mounted() {
    this.fetchProfessionals();
  }
};
</script>






<style scoped>
/* General Styling */
.top-professionals {
  /* background: #f8f9fa; */
  padding: 20px 0;
}

.section-title {
  font-size: 1.8rem;
  font-weight: bold;
  color: #333;
}

/* Filter Bar */
.filter-bar {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
}

.search-box,
.filter-dropdown {
  width: 180px;
  border-radius: 8px;
  padding: 8px;
  border: 1px solid #ccc;
}

/* Professional Card */
.professional-card {
  position: relative;
  border: 2px solid #ddd;
  border-radius: 15px;
  overflow: hidden;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s ease-in-out;
  /* padding: 10px; */
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  width: 100%;
  min-height: 270px;
  margin-bottom: 15px;
  background: white;
}

.professional-card:hover {
  transform: translateY(-5px);
}

/* Rating Badge */
.rating-badge {
  position: absolute;
  top: 8px;
  right: 8px;
  background: #ff4081;
  color: white;
  font-size: 0.9rem;
  font-weight: bold;
  padding: 5px 10px;
  border-radius: 50px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
}

/* Professional Image */
.professional-img {
  border-radius: 25px;
  margin-top: 5px;
  display: block;
  border: 3px solid #007bff;
  width: 120px;
  height: 120px;
  align-self: center;
}

/* Text Styling */
.profession {
  font-size: 1rem;
  font-weight: bold;
  color: #333;
  /* margin-top: 10px; */
}

.category {
  font-size: 1.5rem;
  color: #0a7513;
}

.price {
  font-size: 1rem;
  font-weight: bold;
  color: #007bff;
}

/* Hire Button */
.hire-btn {
  background-color: #007bff;
  color: white;
  font-size: 0.9rem;
  font-weight: bold;
  border-radius: 8px;
  padding: 6px 12px;
  transition: background 0.3s ease;
}

.hire-btn:hover {
  background-color: #0056b3;
}

/* No Results Message */
.no-results {
  font-size: 1.2rem;
  color: #777;
  font-weight: bold;
  margin-top: 10px;
}

/* Modal Overlay */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.6);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

/* Modal Content */
.modal-content {
  background: white;
  padding: 20px;
  border-radius: 12px;
  width: 90%;
  max-width: 450px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
  text-align: center;
  animation: fadeIn 0.3s ease-in-out;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(-20px); }
  to { opacity: 1; transform: translateY(0); }
}

/* Close Button */
.close-btn {
  background-color: #ff4d4d;
  color: white;
  font-size: 0.9rem;
  font-weight: bold;
  border-radius: 8px;
  padding: 8px 12px;
  margin-top: 10px;
  border: none;
  cursor: pointer;
  transition: background 0.3s;
}

.close-btn:hover {
  background-color: #cc0000;
}

/* Form Styling */
form {
  display: flex;
  flex-direction: column;
  gap: 10px;
  padding-top: 10px;
}

form input {
  width: 100%;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 8px;
  font-size: 1rem;
}

.hire-btn {
  background-color: #007bff;
  color: white;
  font-size: 1rem;
  font-weight: bold;
  border-radius: 8px;
  padding: 10px;
  transition: background 0.3s;
  border: none;
  cursor: pointer;
}

.hire-btn:hover {
  background-color: #0056b3;
}
</style>
