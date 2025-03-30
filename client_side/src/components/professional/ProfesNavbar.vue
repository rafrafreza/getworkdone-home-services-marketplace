<template>
  <nav class="navbar">
    <div class="container">
      <!-- Brand Logo -->
      <a class="navbar-brand" href="#">
        <span class="icon">PD</span> Professional Dashboard
      </a>

      <!-- Navigation Links -->
      <div class="nav-links">
        <a 
          class="nav-item" 
          :class="{ active: currentPage === 'jobs' }" 
          @click="$emit('change-page', 'jobs')">
          Jobs
        </a>
        <a 
          class="nav-item" 
          :class="{ active: currentPage === 'services' }" 
          @click="$emit('change-page', 'services')">
          Services
        </a>

        <!-- Profile Dropdown -->
        <div class="dropdown">
          <button class="nav-item profile-btn">
            <span>Account</span> ▼
          </button>
          <div class="dropdown-menu">
            <a @click="$emit('change-page', 'profile')">Profile</a>
            <a @click="logoutUser">Logout</a>
          </div>
        </div>
      </div>
    </div>
  </nav>
</template>

<script>
export default {
  props: ['currentPage'],
  methods: {
    logoutUser() {
      localStorage.removeItem("token"); // Clear token
      this.$router.push('/login'); // Redirect to login page
    }
  }
};
</script>

<style scoped>
/* 🌟 Glassmorphic Navbar */
.navbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: rgba(0, 0, 0, 0.6);
  backdrop-filter: blur(10px);
  padding: 1rem 2rem;
  border-radius: 10px;
  width: 95%;
  margin: 10px auto;
  box-shadow: 0px 8px 20px rgba(0, 0, 0, 0.2);
}

/* 🚀 Brand Logo */
.navbar-brand {
  font-size: 1.5rem;
  font-weight: bold;
  color: white;
  display: flex;
  align-items: center;
  gap: 10px;
}

.icon {
  background: linear-gradient(135deg, #f8d210, #ff8300);
  color: white;
  border-radius: 50%;
  padding: 10px 15px;
  font-size: 1.2rem;
  font-weight: bold;
  box-shadow: 0px 5px 15px rgba(0, 0, 0, 0.3);
}

/* 🎨 Navigation Links */
.nav-links {
  display: flex;
  gap: 20px;
}

/* 🖌️ Nav Items */
.nav-item {
  font-size: 1rem;
  font-weight: 600;
  color: white;
  text-decoration: none;
  padding: 10px 15px;
  border-radius: 5px;
  transition: all 0.3s ease-in-out;
  cursor: pointer;
}

.nav-item:hover {
  background: rgba(255, 255, 255, 0.2);
  transform: translateY(-2px);
}

/* 🔥 Active Link */
.active {
  color: #f8d210;
  font-weight: bold;
}

/* 🔽 Profile Dropdown */
.dropdown {
  position: relative;
}

.profile-btn {
  background: transparent;
  color: white;
  font-size: 1rem;
  font-weight: 600;
  border: none;
  cursor: pointer;
  padding: 10px 15px;
  border-radius: 5px;
  transition: all 0.3s ease-in-out;
}

.profile-btn:hover {
  background: rgba(255, 255, 255, 0.2);
}

/* 🔽 Dropdown Menu */
.dropdown-menu {
  position: absolute;
  right: 0;
  top: 40px;
  background: rgba(0, 0, 0, 0.8);
  border-radius: 8px;
  box-shadow: 0px 5px 15px rgba(0, 0, 0, 0.3);
  overflow: hidden;
  display: none;
  flex-direction: column;
  min-width: 150px;
}

.dropdown:hover .dropdown-menu {
  display: flex;
}

.dropdown-menu a {
  padding: 10px 15px;
  color: white;
  text-decoration: none;
  transition: background 0.3s;
}

.dropdown-menu a:hover {
  background: rgba(255, 255, 255, 0.2);
}

/* 📱 Mobile Responsive */
@media (max-width: 768px) {
  .navbar {
    flex-direction: column;
    align-items: center;
  }

  .nav-links {
    flex-direction: column;
    gap: 10px;
  }
}
</style>
