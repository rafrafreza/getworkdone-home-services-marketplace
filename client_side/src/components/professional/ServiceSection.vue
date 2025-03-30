<template>
  <div class="container mt-5">
    <h2 class="text-center section-title">My Services & Bookings</h2>

    <!-- Assigned / Accepted Section -->
    <div class="section-container">
      <h3 class="section-header">Accepted</h3>

      <div class="row">
        <!-- Assigned Services -->
        <div class="col-md-6">
          <div class="custom-card">
            <div class="card-header bg-primary text-white">Assigned Services</div>
            <div class="card-body">
              <ul class="list-group">
                <li v-for="service in acceptedServices" :key="service.id" class="list-group-item d-flex justify-content-between align-items-center">
                  <div>
                    <h6>{{ service.name }}</h6>
                    <small class="text-muted">₹{{ service.price }} • {{ service.Scheduled_Date }}</small>
                  </div>
                  <span class="badge bg-warning">{{ service.status }}</span>
                </li>
              </ul>
            </div>
          </div>
        </div>

        <!-- Assigned Packages -->
        <div class="col-md-6">
          <div class="custom-card">
            <div class="card-header bg-info text-white">Assigned Packages</div>
            <div class="card-body">
              <ul class="list-group">
                <li v-for="packageItem in acceptedPackages" :key="packageItem.id" class="list-group-item d-flex justify-content-between align-items-center">
                  <div>
                    <h6>{{ packageItem.name }}</h6>
                    <small class="text-muted">₹{{ packageItem.price }} • {{ packageItem.Scheduled_Date }}</small>
                  </div>
                  <span class="badge bg-warning">{{ packageItem.status }}</span>
                </li>
              </ul>
            </div>
          </div>
        </div>
      </div>

      <!-- Assigned Bookings -->
      <div class="custom-card mt-3">
        <div class="card-header bg-success text-white">Assigned Bookings</div>
        <div class="card-body">
          <ul class="list-group">
            <li v-for="booking in acceptedBookings" :key="booking.id" class="list-group-item d-flex justify-content-between align-items-center">
              <div>
                <h6>Booking ID: {{ booking.id }}</h6>
                <small class="text-muted">📅 {{ booking.Scheduled_Date }} | ⏰ {{ booking.time_slot }}</small>
              </div>
              <span class="badge bg-primary">₹{{ booking.price }}</span>
              <span class="badge bg-warning">{{ booking.status }}</span>
            </li>
          </ul>
        </div>
      </div>
    </div>

    <!-- Completed Section -->
    <div class="section-container mt-5">
      <h3 class="section-header">Completed</h3>

      <div class="row">
        <!-- Completed Services -->
        <div class="col-md-6">
          <div class="custom-card">
            <div class="card-header bg-dark text-white">Completed Services</div>
            <div class="card-body">
              <ul class="list-group">
                <li v-for="service in completedServices" :key="service.id" class="list-group-item d-flex justify-content-between align-items-center">
                  <div>
                    <h6>{{ service.name }}</h6>
                    <small class="text-muted">₹{{ service.price }} • {{ service.Scheduled_Date }}</small>
                  </div>
                  <span class="badge bg-success">Completed</span>
                </li>
              </ul>
            </div>
          </div>
        </div>

        <!-- Completed Packages -->
        <div class="col-md-6">
          <div class="custom-card">
            <div class="card-header bg-dark text-white">Completed Packages</div>
            <div class="card-body">
              <ul class="list-group">
                <li v-for="packageItem in completedPackages" :key="packageItem.id" class="list-group-item d-flex justify-content-between align-items-center">
                  <div>
                    <h6>{{ packageItem.name }}</h6>
                    <small class="text-muted">₹{{ packageItem.price }} • {{ packageItem.Scheduled_Date }}</small>
                  </div>
                  <span class="badge bg-success">Completed</span>
                </li>
              </ul>
            </div>
          </div>
        </div>
      </div>

      <!-- Completed Bookings -->
      <div class="custom-card mt-3">
        <div class="card-header bg-dark text-white">Completed Bookings</div>
        <div class="card-body">
          <ul class="list-group">
            <li v-for="booking in completedBookings" :key="booking.id" class="list-group-item">
              <div>
                <h6>Booking ID: {{ booking.id }}</h6>
                <small class="text-muted">📅 {{ booking.Scheduled_Date }} | ⏰ {{ booking.time_slot }}</small>
                <p class="text-muted">💳 Payment: {{ booking.payment_status }}</p>
                <p class="text-muted">⭐ Rating: {{ booking.ratings || 'Not Rated' }}</p>
                <p class="text-muted">📝 Review: {{ booking.reviews || 'No Review' }}</p>
              </div>
              <span class="badge bg-success">₹{{ booking.price }}</span>
            </li>
          </ul>
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
      acceptedServices: [],
      completedServices: [],
      acceptedPackages: [],
      completedPackages: [],
      acceptedBookings: [],
      completedBookings: []
    };
  },
  async created() {
    await this.fetchAcceptedItems();
  },
  computed: {
    sections() {
      return [
        { title: 'Assigned Services', bgClass: 'bg-primary', data: this.acceptedServices },
        { title: 'Completed Services', bgClass: 'bg-dark', data: this.completedServices },
        { title: 'Assigned Packages', bgClass: 'bg-info', data: this.acceptedPackages },
        { title: 'Completed Packages', bgClass: 'bg-dark', data: this.completedPackages },
        { title: 'Assigned Bookings', bgClass: 'bg-success', data: this.acceptedBookings },
        { title: 'Completed Bookings', bgClass: 'bg-dark', data: this.completedBookings }
      ];
    }
  },
  methods: {
    async fetchAcceptedItems() {
      try {
        const token = localStorage.getItem("token");
        if (!token) {
          alert("Authentication required. Please log in again.");
          return;
        }

        const headers = { Authorization: `Bearer ${token}` };
        const [acceptedSer, completedSer, acceptedPack, completedPack, acceptedBook, completedBook] = await Promise.all([
          axios.get('http://127.0.0.1:5000/api/professionals/accepted-services', { headers }),
          axios.get('http://127.0.0.1:5000/api/professionals/completed-services', { headers }),
          axios.get('http://127.0.0.1:5000/api/professionals/accepted-packages', { headers }),
          axios.get('http://127.0.0.1:5000/api/professionals/completed-packages', { headers }),
          axios.get('http://127.0.0.1:5000/api/professionals/accepted-bookings', { headers }),
          axios.get('http://127.0.0.1:5000/api/professionals/completed-bookings', { headers })
        ]);

        this.acceptedServices = this.formatItems(acceptedSer.data, 'service_name');
        this.completedServices = this.formatItems(completedSer.data, 'service_name', true);
        this.acceptedPackages = this.formatItems(acceptedPack.data, 'package_name');
        this.completedPackages = this.formatItems(completedPack.data, 'package_name', true);
        this.acceptedBookings = this.formatItems(acceptedBook.data, 'id', false, true);
        this.completedBookings = this.formatItems(completedBook.data, 'id', true, true);
      } catch (error) {
        console.error("Error fetching accepted items:", error);
        alert(error.response?.data?.message || "Failed to load accepted items.");
      }
    },
    formatItems(data, nameField, isCompleted = false, isBooking = false) {
  return data.map(item => ({
    id: item.id,
    name: item[nameField],  // Corrected line to display actual service/package name
    price: item.price,
    Scheduled_Date: item.Scheduled_Date,
    statusText: isCompleted ? 'Completed' : item.status,
    badgeClass: isCompleted ? 'bg-success' : 'bg-secondary'
  }));
    }
  }
};
</script>

<style scoped>
.section-container {
  margin-bottom: 40px;
}
.section-header {
  font-size: 1.5rem;
  font-weight: bold;
  margin-bottom: 20px;
}
.custom-card {
  background: #fff;
  border-radius: 10px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  overflow: hidden;
  margin-bottom: 20px;
}
.card-header {
  font-weight: bold;
  padding: 15px;
}
.list-group-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px;
}
.badge {
  font-size: 0.9rem;
  padding: 5px 10px;
  border-radius: 5px;
}
</style>

