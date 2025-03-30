<template>
  <div class="container mt-5">
    <h3 class="text-center mb-4 text-primary fw-bold">Available Jobs</h3>

    <div class="row g-4">
      <!-- Service Requests -->
      <div class="col-md-4">
        <div class="card border-primary shadow-lg">
          <div class="card-header bg-primary text-white text-center fw-bold">
            Service Requests
          </div>
          <div class="card-body p-0">
            <ul v-if="serviceRequests.length" class="list-group list-group-flush">
              <li v-for="req in serviceRequests" :key="req.id" class="list-group-item d-flex justify-content-between align-items-center">
                <div>
                  <h6 class="mb-1 text-dark">{{ req.service.name }}</h6>
                  <small class="text-muted">₹{{ req.service.service_price }} | {{ formatDate(req.service.service_dateTime) }}</small>
                </div>
                <div class="btn-group">
                  <button class="btn btn-outline-info btn-sm" @click="viewDetails(req)" title="View Details">👁</button>
                  <button class="btn btn-outline-primary btn-sm" @click="acceptService(req.id)" title="Accept Service">✔</button>
                </div>
              </li>
            </ul>
            <p v-else class="text-muted text-center py-3">No service requests available</p>
          </div>
        </div>
      </div>

      <!-- Package Requests -->
      <div class="col-md-4">
        <div class="card border-info shadow-lg">
          <div class="card-header bg-info text-white text-center fw-bold">
            Package Requests
          </div>
          <div class="card-body p-0">
            <ul v-if="packageRequests.length" class="list-group list-group-flush">
              <li v-for="pkg in packageRequests" :key="pkg.id" class="list-group-item d-flex justify-content-between align-items-center">
                <div>
                  <h6 class="mb-1 text-dark">{{ pkg.package.name }}</h6>
                  <h6 class="text small">{{ pkg.package.description }}</h6>
                  <small class="text-muted">₹{{ pkg.package.package_price }} | {{ formatDate(pkg.package.service_dateTime) }}</small>
                </div>
                <div class="btn-group">
                  <button class="btn btn-outline-info btn-sm" @click="viewDetails(pkg)" title="View Details">👁</button>
                  <button class="btn btn-outline-primary btn-sm" @click="acceptPackage(pkg.id)" title="Accept Package">✔</button>
                </div>
              </li>
            </ul>
            <p v-else class="text-muted text-center py-3">No package requests available</p>
          </div>
        </div>
      </div>

      <!-- Exclusive Bookings -->
      <div class="col-md-4">
        <div class="card border-success shadow-lg">
          <div class="card-header bg-success text-white text-center fw-bold">
            Exclusive Bookings (Only for You)
          </div>
          <div class="card-body p-0">
            <ul v-if="directBookings.length" class="list-group list-group-flush">
              <li v-for="booking in directBookings" :key="booking.id" class="list-group-item d-flex justify-content-between align-items-center">
                <div>
                  <h6 class="mb-1 text-dark">{{ booking.customer.fname }}</h6>
                  <small class="text-muted">{{ formatDate(booking.service.date) }} | {{ booking.service.time_slot }} | ₹{{ booking.service.price }}</small>
                </div>
                <div class="btn-group">
                  <button class="btn btn-outline-info btn-sm" @click="viewDetails(booking)" title="View Details">👁</button>
                  <button class="btn btn-outline-success btn-sm" @click="acceptBooking(booking.id)" title="Accept Booking">✔</button>
                  <button class="btn btn-outline-danger btn-sm" @click="rejectBooking(booking.id)" title="Reject Booking">✖</button>
                </div>
              </li>
            </ul>
            <p v-else class="text-muted text-center py-3">No exclusive bookings available</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      serviceRequests: [],
      packageRequests: [],
      directBookings: [],
    };
  },
  methods: {
    async fetchData() {
      try {
        const token = localStorage.getItem("token");
        if (!token) return console.error("No token found");

        const headers = { Authorization: `Bearer ${token}` };
        const [services, packages, bookings] = await Promise.all([
          axios.get("http://127.0.0.1:5000/api/professional/service-requests", { headers }),
          axios.get("http://127.0.0.1:5000/api/professional/package-requests", { headers }),
          axios.get("http://127.0.0.1:5000/api/professional/direct-bookings", { headers }),
        ]);

        this.serviceRequests = services.data;
        this.packageRequests = packages.data;
        this.directBookings = bookings.data;
      } catch (error) {
        console.error("Error fetching data:", error);
      }
    },
    async handleRequest(id, action) {
      try {
        const token = localStorage.getItem("token");
        if (!token) return console.error("No token found");

        await axios.post(`http://127.0.0.1:5000/api/professional/${action}/${id}`, {}, {
          headers: { Authorization: `Bearer ${token}` },
        });

        this.fetchData();
      } catch (error) {
        console.error(`Error processing ${action}:`, error.response?.data || error);
      }
    },
    acceptService(id) { this.handleRequest(id, "accept-service"); },
    acceptPackage(id) { this.handleRequest(id, "accept-package"); },
    acceptBooking(id) { this.handleRequest(id, "accept-booking"); },
    rejectBooking(id) { this.handleRequest(id, "reject-booking"); },
    viewDetails(item) {
      alert(`Viewing details for ${item.customer?.fname || item.service?.name}`);
    },
    formatDate(dateStr) {
      return new Date(dateStr).toLocaleDateString();
    }
  },
  mounted() {
    this.fetchData();
  },
};
</script>

<style>
.card {
  border-radius: 10px;
  overflow: hidden;
}
.card-header {
  font-size: 1.2rem;
}
.list-group-item {
  transition: all 0.3s ease-in-out;
  padding: 15px;
}
.list-group-item:hover {
  background-color: #f8f9fa;
}
.btn-group button {
  margin-left: 5px;
}
.text-muted {
  font-size: 0.9rem;
}
</style>
