<template>
  <div class="dashboard-container">
    <h1 class="title">GWD Analytics</h1>

    <!-- Stats Cards -->
    <div class="stats-grid">
      <div class="stats-card" v-for="(value, key) in stats" :key="key">
        <h2 class="stats-title">{{ key.replace('_', ' ').toUpperCase() }}</h2>
        <p class="stats-value">{{ value || 0 }}</p>
      </div>
    </div>

    <!-- Charts Section -->
    <div class="charts-grid">
      <div class="chart-card">
        <h2 class="chart-title">Bookings Per Category</h2>
        <Pie v-if="Object.keys(bookingsPerCategory).length" :data="{
          labels: Object.keys(bookingsPerCategory),
          datasets: [{ data: Object.values(bookingsPerCategory), backgroundColor: ['#FF6384', '#36A2EB', '#FFCE56'] }]
        }" />
      </div>

      <div class="chart-card">
        <h2 class="chart-title">Service Requests Status</h2>
        <Doughnut v-if="Object.keys(serviceStatus).length" :data="{
          labels: Object.keys(serviceStatus),
          datasets: [{ data: Object.values(serviceStatus), backgroundColor: ['#FF6384', '#36A2EB', '#FFCE56', '#4CAF50'] }]
        }" />
      </div>
    </div>

    <!-- Recent Bookings Table -->
    <div class="table-card">
      <h2 class="chart-title">Recent Bookings</h2>
      <table>
        <thead>
          <tr>
            <th>ID</th>
            <th>Customer</th>
            <th>Professional</th>
            <th>Category</th>
            <th>Date</th>
            <th>Price</th>
            <th>Status</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="booking in recentBookings" :key="booking.id">
            <td>{{ booking.id }}</td>
            <td>{{ booking.customer }}</td>
            <td>{{ booking.professional }}</td>
            <td>{{ booking.category }}</td>
            <td>{{ booking.date }}</td>
            <td>{{ booking.price }}</td>
            <td>{{ booking.status }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import axios from "axios";
import { Pie, Doughnut } from "vue-chartjs";
import { Chart as ChartJS, Title, Tooltip, Legend, ArcElement, CategoryScale, LinearScale } from "chart.js";

ChartJS.register(Title, Tooltip, Legend, ArcElement, CategoryScale, LinearScale);

const stats = ref({});
const bookingsPerCategory = ref({});
const serviceStatus = ref({});
const recentBookings = ref([]);

const fetchData = async () => {
  try {
    const statsResponse = await axios.get("http://127.0.0.1:5000/api/admin/stats");
    const bookingsResponse = await axios.get("http://127.0.0.1:5000/api/admin/bookings-per-category");
    const statusResponse = await axios.get("http://127.0.0.1:5000/api/admin/service-request-status");
    const recentResponse = await axios.get("http://127.0.0.1:5000/api/admin/recent-bookings");

    stats.value = statsResponse.data;
    bookingsPerCategory.value = bookingsResponse.data;
    serviceStatus.value = statusResponse.data;
    recentBookings.value = recentResponse.data;
  } catch (error) {
    console.error("Error fetching data:", error);
  }
};

onMounted(fetchData);
</script>

<style scoped>
.dashboard-container {
  width: 100%;
  padding: 20px;
  background: #0b0f19;
  min-height: 100vh;
  color: #ffffff;
}

.title {
  font-size: 24px;
  font-weight: bold;
  margin-bottom: 20px;
  text-align: center;
  color: #ffffff;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
  margin-bottom: 30px;
}

.stats-card {
  background: #161b2e;
  padding: 15px;
  border-radius: 10px;
  box-shadow: 0 4px 8px rgba(255, 255, 255, 0.1);
  text-align: center;
  color: #ffffff;
}

.stats-title {
  font-size: 16px;
  font-weight: 600;
  color: #ffffff;
}

.stats-value {
  font-size: 28px;
  font-weight: bold;
  color: #1e90ff;
}

.charts-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
  gap: 20px;
  margin-bottom: 30px;
}

.chart-card, .table-card {
  background: #161b2e;
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 4px 8px rgba(255, 255, 255, 0.1);
  color: #ffffff;
}

.chart-title {
  font-size: 18px;
  font-weight: 600;
  margin-bottom: 15px;
  color: #ffffff;
}

.table-card table {
  width: 100%;
  border-collapse: collapse;
  color: #ffffff;
}

.table-card th, .table-card td {
  padding: 10px;
  text-align: left;
  border-bottom: 1px solid #555;
}

.table-card th {
  background: #1c2235;
  font-weight: 600;
  color: #ffffff;
}
</style>
