<template>
  <div class="container my-4">
    <h2 class="text-center text-dark fw-bold">Professional Hirings</h2>

    <!-- Loading Spinner -->
    <div v-if="loading" class="text-center">
      <div class="spinner-border text-primary" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
    </div>

    <!-- No Bookings Found -->
    <div v-else-if="bookings.length === 0" class="alert alert-warning text-center">
      No bookings found.
    </div>

    <!-- Bookings List -->
    <div v-else>
      <div v-for="(group, status) in groupedBookings" :key="status">
        <h3 class="status-title" :class="statusClass(status)">{{ formatStatus(status) }}</h3>
        <div class="row">
          <div v-for="booking in group" :key="booking.id" class="col-md-6 col-lg-4">
            <div class="card booking-card shadow">
              <div class="card-body">
                <h5 class="card-title">
                  <span class="badge" :class="badgeClass(status)">{{ formatStatus(status) }}</span>
                </h5>
                <p><strong>Booking ID:</strong> {{ booking.id }}</p>
                <p><strong>Service Category:</strong> {{ booking.category || "Unknown" }}</p>
                <p><strong>Professional Name:</strong> {{ booking.professional?.user?.fname || "Unknown" }}</p>
                <p><strong>Scheduled Date:</strong> {{ booking.date }}</p>
                <p><strong>Time Slot:</strong> {{ booking.time_slot }}</p>
                <p><strong>Price:</strong> ₹{{ booking.price }}</p>
                <div v-if="booking.status === 'completed'">
                  <p><strong>Payment Status:</strong> {{ booking.payment_status }}</p>
                  <p><strong>Rating:</strong> {{ booking.ratings }}</p>
                  <p><strong>Review:</strong> {{ booking.reviews }}</p>
                </div>

                <button v-if="booking.status === 'pending'" class="btn btn-outline-danger mt-2" @click="cancelBooking(booking.id)">
                  Cancel Booking
                </button>
                <!-- Make Payment Button for Accepted Requests -->
                <button v-if="booking.status === 'accepted'" class="btn btn-success mt-3" @click="openPaymentModal(booking)">
                  Make Payment
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Payment Modal -->
    <PaymentModal v-if="selectedRequest" :booking="selectedRequest" @refresh-requests="fetchRequests" @close="selectedRequest = null" @payment-success="markAsCompleted" />
  </div>
</template>

<script>
import PaymentModal from "./PaymentModal.vue";

export default {
  components: { PaymentModal },
  data() {
    return {
      bookings: [],
      loading: true,
      selectedRequest: null
    };
  },
  computed: {
    groupedBookings() {
      return this.bookings.reduce((acc, booking) => {
        (acc[booking.status] = acc[booking.status] || []).push(booking);
        return acc;
      }, {});
    }
  },
  methods: {
  async getBookings() {
    try {
      const token = localStorage.getItem("token");
      const response = await fetch("http://127.0.0.1:5000/api/customer/bookings", {
        headers: { Authorization: `Bearer ${token}` }
      });

      if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
      }

      const data = await response.json();
      console.log("📌 Bookings fetched:", data); // Debugging

      this.bookings = data.map(booking => ({
        ...booking,
        category: booking.category || "Unknown",
        professional: booking.professional || { user: { fname: "Unknown" } },
        payment_status: booking.payment_status || "Not Available",
        ratings: booking.ratings !== "Not Rated" ? `${booking.ratings} ⭐` : "Not Rated",
        reviews: booking.reviews || "No Review"
      }));
    } catch (error) {
      console.error("❌ Error fetching bookings:", error);
    } finally {
      this.loading = false;
    }
  },

  async fetchBookings() {
    this.loading = true;
    await this.getBookings();
  },

  async refreshBookings() {
    await this.getBookings();
  },
    
    openPaymentModal(request) {
      this.selectedRequest = request;
    },
    markAsCompleted(requestId) {
      this.bookings = this.bookings.map(booking => 
        booking.id === requestId ? { ...booking, status: "completed" } : booking
      );
    },
    formatStatus(status) {
      return status.replace("_", " ").toUpperCase();
    },
    statusClass(status) {
      return {
        upcoming: "text-primary",
        ongoing: "text-warning",
        completed: "text-success",
        accepted: "text-info",
        canceled: "text-danger"
      }[status] || "text-dark";
    },
    badgeClass(status) {
      return {
        upcoming: "bg-primary",
        ongoing: "bg-warning",
        completed: "bg-success",
        accepted: "bg-info",
        canceled: "bg-danger"
      }[status] || "bg-secondary";
    },
    async cancelBooking(requestId) {
  if (!confirm("Are you sure you want to cancel this Booking?")) return;

  try {
    const token = localStorage.getItem("token");
    const response = await fetch(`http://127.0.0.1:5000/api/customer/bookings/${requestId}`, {
      method: "DELETE",
      headers: {
        "Authorization": `Bearer ${token}`,
        "Content-Type": "application/json",
      },
    });

    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status}`);
    }

    // Update the UI by removing the cancelled booking
    this.bookings = this.bookings.map(booking =>
      booking.id === requestId ? { ...booking, status: "cancelled" } : booking
    );

    alert("Booking cancelled successfully.");
  } catch (error) {
    console.error("❌ Error canceling booking:", error);
    alert("Failed to cancel booking.");
  }
}

  },
  mounted() {
    this.fetchBookings();
  }
};
</script>

<style scoped>
.container {
  max-width: 1100px;
  margin: auto;
  padding: 20px;
}
.status-title {
  margin-top: 30px;
  font-size: 1.5rem;
  font-weight: bold;
  border-bottom: 3px solid;
  padding-bottom: 5px;
}
.booking-card {
  border-radius: 10px;
  transition: transform 0.3s ease-in-out, box-shadow 0.3s ease-in-out;
  background: linear-gradient(to right, #f8f9fa, #e9ecef);
  padding: 15px;
}
.booking-card:hover {
  transform: scale(1.05);
  box-shadow: 0px 5px 15px rgba(0, 0, 0, 0.2);
}
.badge {
  font-size: 1rem;
  padding: 8px 12px;
  border-radius: 10px;
}
</style>
