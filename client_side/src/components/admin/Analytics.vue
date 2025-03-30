<template>
  <div class="analytics-container">
    <AdminNavbar />
    <!-- Header Buttons for Navigation -->
    <div class="nav-buttons">
      <router-link to="/admin/all-requests">
        <button class="nav-btn">📌 View All Requests</button>
      </router-link>
      <router-link to="/admin/all-bookings">
        <button class="nav-btn">📌 View All Bookings</button>
      </router-link>
    </div>

    <!-- Admin Charts Component -->
    <div class="charts-section">
      <AdminCharts />
    </div>
  </div>
</template>

<script>
import AdminCharts from './AdminCharts.vue';
import AdminNavbar from './AdminNavbar.vue';

export default {
components: {
  AdminNavbar,
  AdminCharts
}
};
</script>

<style scoped>
.analytics-container {
background-color: #0b0f19;
margin: auto;
text-align: center;
padding: 20px;
}

.charts-section {
width: 85%; /* Set width to 80% */
margin: auto; /* Center it */
display: flex;
justify-content: center;
align-items: center;
}

.nav-buttons {
display: flex;
justify-content: center;
gap: 20px;
margin-bottom: 20px;
}

.nav-btn {
background-color: #007bff;
color: white;
padding: 10px 20px;
font-size: 16px;
border: none;
cursor: pointer;
transition: 0.3s;
border-radius: 5px;
}

.nav-btn:hover {
background-color: #0056b3;
}
</style>
