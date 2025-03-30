<template>
    <div class="container">
      <h2>All Bookings</h2>
      <table>
        <thead>
          <tr>
            <th>ID</th>
            <th>Customer</th>
            <th>Professional</th>
            <th>Category</th>
            <th>Booking Date</th>
            <th>Time Slot</th>
            <th>Price</th>
            <th>Status</th>
            <th>Payment</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="booking in bookings" :key="booking.id">
            <td>{{ booking.id }}</td>
            <td>{{ booking.customer }}</td>
            <td>{{ booking.professional }}</td>
            <td>{{ booking.category }}</td>
            <td>{{ booking.booking_date }}</td>
            <td>{{ booking.time_slot }}</td>
            <td>₹{{ booking.price }}</td>
            <td :class="statusClass(booking.status)">{{ booking.status }}</td>
            <td :class="paymentClass(booking.payment_status)">{{ booking.payment_status }}</td>
          </tr>
        </tbody>
      </table>
      <!-- 🔙 Back Button -->
       <hr>
    <button class="btn btn-outline-primary back-button" @click="$router.go(-1)">
      <i class="bi bi-arrow-left"></i> Back
    </button>
    </div>
  </template>
  
  <script>
  import axios from "axios";
  
  export default {
    data() {
      return {
        bookings: [],
      };
    },
    async created() {
      try {
        const response = await axios.get("http://127.0.0.1:5000/api/admin/all-bookings-info", {
          headers: { Authorization: `Bearer ${localStorage.getItem("token")}` },
        });
        this.bookings = response.data.bookings;
      } catch (error) {
        console.error("Error fetching bookings:", error);
      }
    },
    methods: {
      statusClass(status) {
        return status === "completed"
          ? "completed"
          : status === "cancelled"
          ? "cancelled"
          : "pending";
      },
      paymentClass(status) {
        return status === "successful" ? "paid" : "unpaid";
      },
    },
  };
  </script>
  
  <style scoped>
  .container {
    background-color: #0b0f19;
    max-width: 90%;
    margin: 20px auto;
    text-align: center;
  }
  
  table {
    width: 100%;
    border-collapse: collapse;
  }
  
  th, td {
    color: white;
    border: 1px solid #ddd;
    padding: 8px;
  }
  
  th {
    background-color: #007bff;
    color: white;
  }
  
  .completed {
    color: green;
  }
  
  .cancelled {
    color: red;
  }
  
  .pending {
    color: orange;
  }
  
  .paid {
    color: green;
  }
  
  .unpaid {
    color: red;
  }
  </style>
  