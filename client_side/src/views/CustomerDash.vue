<template>
  <div class="container mt-2">
    <!-- 🔙 Back Button -->
    <button class="btn btn-outline-primary back-button" @click="$router.go(-1)">
      <i class="bi bi-arrow-left"></i> Back
    </button>

    <div v-if="isAuthenticated" class="card shadow-sm">
      <CustomerProfile />
      <ServiceRequests />
      <PackageRequests />
      <ProfessionalBookings />
    </div>
  </div>
</template>

<script>
import axios from "axios";
import CustomerProfile from "@/components/customer/CustomerProfile.vue";
import ServiceRequests from "@/components/customer/ServiceRequests.vue";
import PackageRequests from "@/components/customer/PackageRequests.vue";
import ProfessionalBookings from "@/components/customer/ProfessionalBookings.vue";

export default {
  components: { CustomerProfile, ServiceRequests, PackageRequests, ProfessionalBookings },
  data() {
    return {
      isAuthenticated: false, // Track authentication status
      customer: {},
      requestedServices: [],
      requestedPackages: [],
      ongoingServices: [],
      ongoingPackages: [],
      completedServices: [],
      completedPackages: [],
      bookings: [],
      activeAccordion: "requested", // Default to show first section
    };
  },
  methods: {
    toggleAccordion(section) {
      this.activeAccordion = this.activeAccordion === section ? null : section;
    },
    redirectToLogin() {
      this.$router.push("/login"); // Redirect to login page
    },
    async refreshRequests() {
      try {
        const token = localStorage.getItem("token");
        const requestsRes = await axios.get("http://127.0.0.1:5000/api/customer/service-requests", {
          headers: { Authorization: `Bearer ${token}` },
        });

        // Reset arrays
        this.requestedServices = [];
        this.requestedPackages = [];
        this.ongoingServices = [];
        this.ongoingPackages = [];
        this.completedServices = [];
        this.completedPackages = [];

        // Categorize Service Requests
        requestsRes.data.forEach((request) => {
          if (request.status === "requested") {
            request.package_id ? this.requestedPackages.push(request) : this.requestedServices.push(request);
          } else if (request.status === "ongoing") {
            request.package_id ? this.ongoingPackages.push(request) : this.ongoingServices.push(request);
          } else if (request.status === "completed") {
            request.package_id ? this.completedPackages.push(request) : this.completedServices.push(request);
          }
        });
      } catch (error) {
        console.error("Error refreshing requests:", error);
        this.$toast.error("Failed to refresh service requests");
      }
    },
    async refreshBookings() {
      try {
        const token = localStorage.getItem("token");
        const bookingsRes = await axios.get("http://127.0.0.1:5000/api/customer/bookings", {
          headers: { Authorization: `Bearer ${token}` },
        });
        this.bookings = bookingsRes.data;
      } catch (error) {
        console.error("Error refreshing bookings:", error);
        this.$toast.error("Failed to refresh bookings");
      }
    }
  },
  async created() {
    try {
      const token = localStorage.getItem("token");

      // 🔴 If token doesn't exist, redirect to login
      if (!token) {
        this.redirectToLogin();
        return;
      }

      // ✅ Fetch Customer Profile FIRST
      const customerRes = await axios.get("http://127.0.0.1:5000/dashboard/customer", {
        headers: { Authorization: `Bearer ${token}` },
      });

      this.customer = customerRes.data;
      this.isAuthenticated = true; // Mark user as authenticated

      // Initial data fetch
      await this.refreshRequests();
      await this.refreshBookings();
    } catch (error) {
      console.error("Error fetching data:", error.response?.data || error.message);

      // 🔴 Handle Unauthorized Errors (401 or 403)
      if (error.response?.status === 401 || error.response?.status === 403) {
        localStorage.removeItem("token"); // Remove invalid token
        this.redirectToLogin();
      }
    }
  }
};
</script>

<style scoped>
/* 🔙 Back Button Styling */
.back-button {
  font-size: 1rem;
  font-weight: bold;
  display: flex;
  align-items: center;
}

.back-button i {
  font-size: 1.2rem;
  margin-right: 5px;
}

/* 🎨 Beautify the Design */
.accordion-button {
  font-size: 1.2rem;
  font-weight: bold;
  background-color: #f8f9fa;
  color: #007bff;
  transition: background 0.3s ease-in-out, transform 0.2s;
}

.accordion-button:hover {
  background-color: #e9ecef;
  transform: scale(1.02);
}

.accordion-item {
  border: 1px solid #dee2e6;
  border-radius: 8px;
  margin-bottom: 8px;
}

.accordion-body {
  background: #ffffff;
  border-radius: 0 0 8px 8px;
}

.card {
  border-radius: 10px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  margin-top: 10px;
}

.card-title {
  font-size: 1.5rem;
  font-weight: bold;
}

.bi {
  font-size: 1.4rem;
  margin-right: 5px;
}
</style>
