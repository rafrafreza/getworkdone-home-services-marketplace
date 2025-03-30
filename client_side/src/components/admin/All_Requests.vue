<template>
  <div class="admin-dashboard">
    <!-- 🔙 Back Button -->
    <button class="btn btn-outline-primary back-button" @click="$router.go(-1)">
      <i class="bi bi-arrow-left"></i> Back
    </button>
    <div class="export-button-container">
      <button class="export-btn" @click="exportcsv">Export as CSV</button>
    </div>
    <h2>📌 All Service Requests</h2>

    <table v-if="serviceRequests.length > 0" class="table">
      <thead>
        <tr>
          <th>ID</th>
          <th>Service Name</th>
          <th>Customer</th>
          <th>Professional</th>
          <th>Requested On</th>
          <th>Service Date</th>
          <th>Completion Date</th>
          <th>Status</th>
          <th>Payment</th>
          <th>Rating</th>
          <th>Review</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="request in serviceRequests" :key="request.id">
          <td>{{ request.id }}</td>
          <td>{{ request.service_name }}</td>
          <td>{{ request.customer_name }}</td>
          <td>{{ request.professional_name }}</td>
          <td>{{ request.date_of_request }}</td>
          <td>{{ request.service_dateTime }}</td>
          <td>{{ request.date_of_completion }}</td>
          <td :class="getStatusClass(request.service_status)">
            {{ request.service_status }}
          </td>
          <td :class="getPaymentClass(request.payment_status)">
            {{ request.payment_status }}
          </td>
          <td>{{ request.ratings }}</td>
          <td>{{ request.reviews }}</td>
        </tr>
      </tbody>
    </table>

    <p v-else>No service requests found.</p>
  </div>
</template>

<script>
export default {
  data() {
    return {
      serviceRequests: [],
    };
  },
  mounted() {
    this.fetchServiceRequests();
  },
  methods: {
    async fetchServiceRequests() {
      try {
        const response = await fetch("http://127.0.0.1:5000/api/admin/serv_pack_req");
        const data = await response.json();
        if (data.success) {
          this.serviceRequests = data.service_requests;
        } else {
          console.error("Error fetching service requests:", data.error);
        }
      } catch (error) {
        console.error("Error fetching service requests:", error);
      }
    },
    getStatusClass(status) {
      return {
        requested: "status-requested",
        assigned: "status-assigned",
        closed: "status-closed",
        cancelled: "status-cancelled",
      }[status] || "status-default";
    },
    getPaymentClass(status) {
      return {
        pending: "payment-pending",
        successful: "payment-successful",
        failed: "payment-failed",
      }[status] || "payment-default";
    },
    async exportcsv() {
    try {
        const response = await fetch('http://127.0.0.1:5000/api/export_csv');
        if (!response.ok) {
            throw new Error(`Error: ${response.status} - ${response.statusText}`);
        }

        const data = await response.json();
        const taskId = data.id;

        if (!taskId) {
            throw new Error("No task ID received from the server.");
        }

        let fileName = null;
        for (let i = 0; i < 10; i++) {  // Retry 10 times
            await new Promise(r => setTimeout(r, 2000));  // Wait 2 seconds before retrying
            
            const statusResponse = await fetch(`http://127.0.0.1:5000/api/csv_report/${taskId}`);
            const statusData = await statusResponse.json();

            if (statusData.status === "ready" && statusData.file) {  
                fileName = statusData.file;
                break;
            }
        }

        if (fileName) {
            const fileUrl = `http://127.0.0.1:5000/api/download_csv/${fileName}`;
            window.location.href = fileUrl;  // Start download
        } else {
            alert("CSV generation took too long. Please try again.");
        }

    } catch (error) {
        console.error("Error exporting CSV:", error);
        alert("Failed to export CSV. Please try again.");
    }
}


  },
};
</script>

<style scoped>
/* Full-page background */
body {
  background-color: #0b0f19;
  color: #ffffff;
  margin: 0;
  font-family: Arial, sans-serif;
}

/* Dashboard container */
.admin-dashboard {
  max-width: 95%;
  margin: 30px auto;
  padding: 20px;
  background: #121826;
  box-shadow: 0px 5px 15px rgba(0, 0, 0, 0.3);
  border-radius: 8px;
  position: relative;
}

/* Export Button */
.export-button-container {
  text-align: right;
  margin-bottom: 15px;
}

.export-btn {
  background-color: #007bff;
  color: white;
  padding: 10px 20px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-size: 14px;
  transition: background 0.3s ease;
}

.export-btn:hover {
  background-color: #0056b3;
}

/* Table Styling */
.table {
  width: 100%;
  border-collapse: collapse;
  background: #1a1f2e;
  border-radius: 8px;
  overflow: hidden;
}

.table th {
  background: #2b3247;
  padding: 12px;
  text-align: center;
  color: #ffffff;
}
h2 {
  color: #ffffff;
}
.table td {
  padding: 12px;
  border: 1px solid #3c4359;
  text-align: center;
}

.table tr:nth-child(even) {
  background: #22293e;
}

.table tr:hover {
  background: #323b54;
}

/* Status Colors */
.status-requested {
  color: #00bfff;
}

.status-assigned {
  color: #ffbf00;
}

.status-closed {
  color: #28a745;
}

.status-cancelled {
  color: #dc3545;
}

/* Payment Status */
.payment-pending {
  color: #ffbf00;
}

.payment-successful {
  color: #28a745;
}

.payment-failed {
  color: #dc3545;
}

/* Message if no requests */
p {
  text-align: center;
  font-size: 16px;
  margin-top: 20px;
}
</style>
