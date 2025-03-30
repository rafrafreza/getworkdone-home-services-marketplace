<template>
  <div class="package-requests container">
    <h2 class="text-center mb-4 text-primary fw-bold">Your Package Requests</h2>

    <div v-if="loading" class="text-center">
      <div class="spinner-border text-primary" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
    </div>

    <div v-else>
      <div v-if="packageRequests.length === 0" class="alert alert-warning text-center">
        No Package requests found.
      </div>

      <div v-else>
        <!-- Requested Packages -->
        <h3 class="status-title requested">Requested</h3>
        <div class="row">
          <div v-for="request in requestedPackages" :key="request.id" class="col-md-6 col-lg-4">
            <div class="card package-card border-warning shadow-sm">
              <div class="card-body">
                <h5 class="card-title text-warning">Package Request ID: {{ request.id }}</h5>
                <p><strong>Package Name:</strong> {{ request.package_name }}</p>
                <p><strong>Category:</strong> {{ request.category_name }}</p>
                <p><strong>Price:</strong> ₹{{ request.package_price }}</p>
                <p><strong>Requested On:</strong> {{ request.request_date }}</p>
                <p><strong>Scheduled Date:</strong> {{ request.service_dateTime }}</p>

                <button class="btn btn-outline-danger mt-2" @click="cancelRequest(request.id)">
                  Cancel Package Request
                </button>
              </div>
            </div>
          </div>
        </div>

        <!-- Ongoing Services -->
        <h3 class="status-title ongoing">Ongoing</h3>
        <div class="row">
          <div v-for="request in ongoingPackages" :key="request.id" class="col-md-6 col-lg-4">
            <div class="card service-card border-primary shadow-sm">
              <div class="card-body">
                <h5 class="card-title text-primary">Request ID: {{ request.id }}</h5>
                <p><strong>Package Name:</strong> {{ request.package_name }}</p>
                <p><strong>Service Category:</strong> {{ request.category_name }}</p>
                <p><strong>Price:</strong> ₹{{ request.package_price }}</p>
                <p><strong>Professional Assigned:</strong> {{ request.professional_name }}</p>
                <p><strong>Scheduled Date:</strong> {{ request.service_dateTime }}</p>

                <!-- Payment Button -->
                <button class="btn btn-success mt-3" @click="openPaymentModal(request)">
                  Make Payment
                </button>
              </div>
            </div>
          </div>
        </div>

        <!-- Completed Packages -->
        <h3 class="status-title completed">Completed</h3>
        <div class="row">
          <div v-for="request in completedPackages" :key="request.id" class="col-md-6 col-lg-4">
            <div class="card package-card border-success shadow-sm">
              <div class="card-body">
                <h5 class="card-title text-success">Package Request ID: {{ request.id }}</h5>
                <p><strong>Package Name:</strong> {{ request.package_name }}</p>
                <p><strong>Category:</strong> {{ request.category_name }}</p>
                <p><strong>Price:</strong> ₹{{ request.package_price }}</p>
                <p><strong>Professional Assigned:</strong> {{ request.professional_name }}</p>
                <p><strong>Requested On:</strong> {{ request.request_date }}</p>
                <p><strong>Scheduled Date:</strong> {{ request.service_dateTime }}</p>
                <p><strong>Payment Status:</strong> {{ request.payment }}</p>
                <p><strong>Rating:</strong> {{ request.ratings }}</p>
                <p><strong>Review:</strong> {{ request.reviews }}</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Payment Modal Component -->
    <PaymentModal 
      v-if="showPaymentModal" 
      :request="selectedRequest" 
      @refresh-requests="fetchRequests" 
      @close="showPaymentModal = false" 
      @payment-success="markAsCompleted"
    />
  </div>
</template>

---

### **Vue Script:**
```vue
<script>
import PaymentModal from './PaymentModal.vue'; // Import Payment Component

export default {
  components: {
    PaymentModal,
  },
  data() {
    return {
      packageRequests: [],
      loading: true,
      showPaymentModal: false,
      selectedRequest: null,
    };
  },
  computed: {
    requestedPackages() {
      return this.packageRequests.filter(req => req.status === "requested");
    },
    ongoingPackages() {
      return this.packageRequests.filter(req => req.status === "assigned");
    },
    completedPackages() {
      return this.packageRequests.filter(req => req.status === "completed");
    }
  },
  methods: {
    async fetchPackageRequests() {
      try {
        const token = localStorage.getItem("token");
        const response = await fetch("http://127.0.0.1:5000/api/customer/package-requests", {
          headers: {
            Authorization: `Bearer ${token}`,
            "Content-Type": "application/json"
          }
        });

        if (!response.ok) {
          throw new Error(`HTTP error! Status: ${response.status}`);
        }

        const data = await response.json();
        console.log("✅ API Response:", data);

        this.packageRequests = data.map(req => ({
          id: req.id,
          service_id: req.service_id,
          package_name: req.package_name || "N/A",
          category_name: req.category_name || "N/A",
          package_price: req.package_price || "N/A",
          package_id: req.package_id,
          professional_name: req.professional_name || "Not Assigned",
          status: req.status,
          request_date: req.request_date,
          service_dateTime: req.service_dateTime,
          completion_date: req.completion_date || null,
          payment: req.payment_status || "N/A",
          ratings: req.ratings || "Not Rated",
          reviews: req.reviews || "Not Reviewed"
        }));
      } catch (error) {
        console.error("❌ Error fetching service requests:", error);
      } finally {
        this.loading = false;
      }
    },

    openPaymentModal(request) {
      this.selectedRequest = request;
      this.showPaymentModal = true;
    },

    markAsCompleted(requestId) {
      const index = this.packageRequests.findIndex(req => req.id === requestId);
      if (index !== -1) {
        this.packageRequests[index].status = "completed";
      }
      this.showPaymentModal = false;
      fetchPackageRequests()
    },
    async cancelRequest(requestId) {
      if (!confirm("Are you sure you want to cancel this package request?")) return;

      try {
        const token = localStorage.getItem("token");
        const response = await fetch(`http://127.0.0.1:5000/api/customer/service-requests/${requestId}`, {
          method: "DELETE",
          headers: {
            "Authorization": `Bearer ${token}`,
            "Content-Type": "application/json",
          },
        });

        if (!response.ok) {
          throw new Error(`HTTP error! Status: ${response.status}`);
        }

        this.packageRequests = this.packageRequests.filter(req => req.id !== requestId);
        alert("Service request cancelled successfully.");
      } catch (error) {
        console.error("❌ Error canceling request:", error);
        alert("Failed to cancel request.");
      }
    }
  },
  mounted() {
    this.fetchPackageRequests();
  }
};
</script>


<style scoped>
.package-requests {
  max-width: 1100px;
  margin: auto;
  padding: 20px;
}

/* Section Titles */
.status-title {
  margin-top: 20px;
  font-size: 1.5rem;
  font-weight: bold;
  padding: 10px;
  border-bottom: 3px solid;
}

.requested {
  color: orange;
  border-color: orange;
}

.ongoing {
  color: blue;
  border-color: blue;
}

.completed {
  color: green;
  border-color: green;
}

/* Package Card Design */
.package-card {
  border-radius: 10px;
  transition: transform 0.3s ease-in-out, box-shadow 0.3s ease-in-out;
}

.package-card:hover {
  transform: scale(1.05);
  box-shadow: 0px 5px 15px rgba(0, 0, 0, 0.2);
}

/* Spinner for Loading */
.spinner-border {
  width: 3rem;
  height: 3rem;
  margin-top: 20px;
}
</style>
