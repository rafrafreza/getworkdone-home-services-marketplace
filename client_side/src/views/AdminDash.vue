<template>
  <div class="admin-panel">
    <AdminNavbar />
    
    <div class="main-container">
      <!-- Profile Section -->
      <div class="profile-section">
        <div class="profile-card">
          <!-- <img v-if="user.profile_picture" :src="user.profile_picture" alt="Admin Profile" class="profile-pic"> -->
          <img src="/images/gwd.webp" alt="Admin Profile" class="profile-pic">
          <p class="profile-name">{{ user.fname }}</p>
          <p class="profile-info">{{ user.email }}</p>
          <p class="profile-info">{{ user.phone }}</p>
        </div>

        <NewCatSerPack />
      </div>
      
      <!-- Professional Pending Registration -->
      <div class="requests-section">
        <h3>Professional’s Verification</h3>
        <div class="table-container">
          <table>
            <thead>
              <tr>
                <th>Professional Name</th>
                <th>Service Type</th>
                <th>Experience</th>
                <th>City</th>
                <th>Price</th>
                <th>Resume</th>
                <th>Action</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(request, index) in pendingRequests" :key="request.id">
                <td>{{ request.name }}</td>
                <td>{{ request.service_type }}</td>
                <td>{{ request.experience }} years</td>
                <td>{{ request.city }}</td>
                <td>₹{{ request.price }}/hr</td>
                <td>
                  <a :href="`http://127.0.0.1:5000/api/admin/resume/${request.id}`" target="_blank" rel="noopener noreferrer">
                    <button>Download Resume</button>
                  </a>
                </td>
                <td>
                  <button class="approve-btn" @click="approveRequest(request.id, index)">Approve</button>
                  <button class="reject-btn" @click="rejectRequest(request.id, index)">Reject</button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
      
      <!-- Service Package Joining Requests -->
      <div class="requests-section">
        <h3>Service Package Joining Requests</h3>
        <div class="table-container">
          <table>
            <thead>
              <tr>
                <th>Professional Name</th>
                <th>Service Type</th>
                <th>Experience</th>
                <th>City</th>
                <th>Package Name</th>
                <th>Status</th>
                <th>Action</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(request, index) in packageRequests" :key="request.id">
                <td>{{ request.prof_name }}</td>
                <td>{{ request.service_type }}</td>
                <td>{{ request.experience }} years</td>
                <td>{{ request.city }}</td>
                <td>{{ request.package_name }}</td>
                <td>{{ request.status }}</td>
                <td>
                  <button class="approve-btn" @click="approvePackage(request.id, index)">Approve</button>
                  <button class="reject-btn" @click="rejectPackage(request.id, index)">Reject</button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>
</template>


<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';
import AdminNavbar from '@/components/admin/AdminNavbar.vue';
import NewCatSerPack from '@/components/admin/NewCatSerPack.vue';

// User Profile Data
const user = ref({
//   name: "Admin User",
//   email: "admin@example.com",
//   phone: "+1234567890"
});

// Pending Requests Data
const pendingRequests = ref([]);
const packageRequests = ref([]);


// Fetch Admin Profile
const fetchAdminProfile = async () => {
  try {
    const token = localStorage.getItem("token"); // Assuming JWT is stored in localStorage
    const response = await axios.get("http://127.0.0.1:5000/dashboard/admin", {
      headers: { Authorization: `Bearer ${token}` }
    });

    user.value = {
      fname: response.data.admin_info.fname,
      email: response.data.admin_info.email,
      phone: response.data.admin_info.phone,
      profile_picture: response.data.admin_info.profile_picture
    };
  } catch (error) {
    console.error("Error fetching admin profile", error);
  }
};


// Fetch Pending Requests
const fetchPendingRequests = async () => {
  try {
    const response = await axios.get('http://127.0.0.1:5000/api/admin/professionals/pending-requests');
    pendingRequests.value = response.data;
  } catch (error) {
    console.error("Error fetching pending requests", error);
  }
};

// Fetch Package Requests
const fetchPackageRequests = async () => {
  try {
    const response = await axios.get('http://127.0.0.1:5000/api/admin/professionals/package-requests/pending');
    packageRequests.value = response.data;
  } catch (error) {
    console.error("Error fetching package requests", error);
  }
};



// Approve Request
const approveRequest = async (id, index) => {
  try {
    await axios.put(`http://127.0.0.1:5000/api/admin/professionals/approve/${id}`);
    pendingRequests.value.splice(index, 1);
  } catch (error) {
    console.error("Error approving request", error);
  }
};

// Reject Request
const rejectRequest = async (id, index) => {
  try {
    await axios.put(`http://127.0.0.1:5000/api/admin/professionals/reject/${id}`);
    pendingRequests.value.splice(index, 1);
  } catch (error) {
    console.error("Error rejecting request", error);
  }
};

// Approve Package Request
const approvePackage = async (id, index) => {
  try {
    await axios.put(`http://127.0.0.1:5000/api/admin/professionals/package-requests/approve/${id}`);
    packageRequests.value.splice(index, 1);
  } catch (error) {
    console.error("Error approving package request", error);
  }
};

// Reject Package Request
const rejectPackage = async (id, index) => {
  try {
    await axios.put(`http://127.0.0.1:5000/api/admin/professionals/package-requests/reject/${id}`);
    packageRequests.value.splice(index, 1);
  } catch (error) {
    console.error("Error rejecting package request", error);
  }
};

onMounted(() => {
  fetchAdminProfile();
  fetchPendingRequests();
  fetchPackageRequests();
});
</script>

<style scoped>
.admin-panel {
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  background: #0b0f19;
  min-height: 100vh;
  padding: 10px;
  color: #fff;
  font-family: 'Poppins', sans-serif;
}

.main-container {
  width: 90%;
  display: flex;
  flex-direction: column;
  gap: 30px;
}

.profile-section {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-left: 120px;
}

.profile-card {
  background: linear-gradient(135deg, #1e3c72, #2a5298);
  padding: 20px;
  border-radius: 12px;
  text-align: center;
  width: 300px;
  box-shadow: 0 4px 10px rgba(255, 255, 255, 0.1);
}

.profile-pic {
  width: 100px;
  height: 100px;
  border-radius: 50%;
  object-fit: cover;
  border: 3px solid #fff;
  margin-bottom: 10px;
}

.profile-name {
  font-size: 20px;
  font-weight: bold;
}

.profile-info {
  font-size: 14px;
  color: #ddd;
}

.requests-section {
  background: #1a1d29;
  padding: 25px;
  border-radius: 12px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.3);
}

h3 {
  color: #00c6ff;
  margin-bottom: 15px;
}

.table-container {
  overflow-x: auto;
}

table {
  width: 100%;
  border-collapse: collapse;
  background: #252a3f;
  border-radius: 8px;
  overflow: hidden;
}

thead {
  background: #00c6ff;
  color: #fff;
}

td, th {
  padding: 12px;
  text-align: left;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.view-btn {
  background: #0d8091;
  color: white;
  padding: 8px 16px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background 0.3s;
  margin: 3px
}

.view-btn:hover {
  background: #0f8f88;
}

.approve-btn {
  background: #28a745;
  color: white;
  padding: 8px 16px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background 0.3s;
  margin: 3px
}

.approve-btn:hover {
  background: #218838;
}

.reject-btn {
  background: #dc3545;
  color: white;
  padding: 8px 16px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background 0.3s;
  margin: 3px
}

.reject-btn:hover {
  background: #c82333;
}
</style>
