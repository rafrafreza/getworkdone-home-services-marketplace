<template>
  <nav class="navbar navbar-expand-lg glass-navbar">
    <div class="container">
      <!-- Leftmost: Admin Panel -->
      <a class="navbar-brand fw-bold" href="#">Admin Panel</a>

      <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#adminNavbar">
        <span class="navbar-toggler-icon"></span>
      </button>

      <div class="collapse navbar-collapse justify-content-center" id="adminNavbar">
        <ul class="navbar-nav gap-4 mx-auto">
          <li class="nav-item">
            <a class="nav-link" href="/dashboard/admin">Home</a>
          </li>
          <li class="nav-item">
            <a class="nav-link" href="/admin/manage-services">Manage Services</a>
          </li>
          <li class="nav-item">
            <a class="nav-link" href="/admin/manage-users">Manage Users</a>
          </li>
          <li class="nav-item">
            <a class="nav-link" href="/admin/analytics">Stats</a>
          </li>
        </ul>
      </div>
      
      <!-- Rightmost: Logout Button -->
      <button class="btn logout-btn" @click="logout">Logout</button>
    </div>
  </nav>
</template>

<script>
export default {
  methods: {
    logout() {
      localStorage.removeItem("token");
      window.location.href = "/login"; // Redirect to login page
    }
  }
};
</script>

<style scoped>
/* Glassmorphism Navbar */
.glass-navbar {
  background: rgba(0, 0, 0, 0.3);
  backdrop-filter: blur(20px);
  border-radius: 20px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
  padding: 14px 30px;
  margin: 15px auto;
  width: 85%;
  border: 1px solid rgba(255, 255, 255, 0.2);
  transition: all 0.3s ease-in-out;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

/* Navbar Brand */
.navbar-brand {
  font-size: 1.7rem;
  font-weight: bold;
  color: #00f7ff;
  letter-spacing: 1px;
  transition: 0.3s;
}

.navbar-brand:hover {
  color: #14edf5;
}

/* Navigation Links */
.navbar-nav {
  display: flex;
  align-items: center;
}

.nav-link {
  font-weight: 600;
  color: white;
  font-size: 1.1rem;
  transition: all 0.3s;
  padding: 12px 20px;
  border-radius: 15px;
  position: relative;
  overflow: hidden;
}

.nav-link:hover {
  background: rgba(255, 255, 255, 0.15);
  color: #00f7ff;
  box-shadow: 0 0 8px rgba(0, 247, 255, 0.5);
}

/* Logout Button */
.logout-btn {
  background: linear-gradient(135deg, #ff6b6b, #ff4757);
  color: white;
  padding: 10px 18px;
  font-weight: 700;
  border: none;
  border-radius: 12px;
  transition: 0.3s;
  box-shadow: 0 0 10px rgba(255, 107, 107, 0.4);
}

.logout-btn:hover {
  background: linear-gradient(135deg, #ff4757, #e84118);
  box-shadow: 0 0 15px rgba(255, 71, 87, 0.8);
}

/* Responsive Design */
@media (max-width: 992px) {
  .glass-navbar {
    width: 95%;
    flex-direction: column;
    align-items: center;
  }
  .logout-btn {
    margin-top: 10px;
  }
}
</style>
