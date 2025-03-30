<template>
  <header class="header">
    <div class="logo">
      <span class="icon">GWD</span>
      <span class="title">GetWorkDone</span>
    </div>
    <nav class="nav-links">
      <router-link v-if="(hideServicesButton || hideProfileButton) " to="/" class="btn services-btn">Home</router-link>
      <router-link v-if="!hideServicesButton" to="/services" class="btn services-btn">Services</router-link>
      <router-link v-if="!isCustomerLoggedIn" to="/login" class="btn login-btn">Login</router-link>
      <!-- Hide Profile button when hideProfileButton is true -->
      <router-link 
          v-if="isCustomerLoggedIn" 
          to="/dashboard/customer" 
          class="btn profile-btn">
          Profile
      </router-link>
      <router-link 
          v-if="isCustomerLoggedIn" 
          to="#" 
          class="btn profile-btn" 
          v-on:click.native.prevent="logoutUser">
          Logout
      </router-link>
    </nav>

  </header>
</template>

<script>
export default {
  props: {
    hideServicesButton: {
      type: Boolean,
      default: false
    },
    hideProfileButton: {
      type: Boolean,
      default: false, // Default is false (show button)
    },
  },
  data() {
    return {
      isCustomerLoggedIn: false,
    };
  },
  mounted() {
    const token = localStorage.getItem("token");
    if (token) {
      try {
        const claims = JSON.parse(atob(token.split(".")[1])); // Decode JWT payload
        this.isCustomerLoggedIn = claims.role === 0; // Check if role is customer
        
      } catch (error) {
        console.error("Error decoding token", error);
      }
    }
  },
  methods: {
    logoutUser() {
      fetch("http://127.0.0.1:5000/auth/logout", { 
        method: "POST", 
        headers: { Authorization: `Bearer ${localStorage.getItem("token")}` } 
      })
      .then(response => response.json())
      .then(() => {
        localStorage.removeItem("token"); // Remove JWT
        this.isCustomerLoggedIn = false; // Update state
        this.$router.push("/login"); // Redirect to login page
      })
      .catch(error => console.error("Logout failed", error));
    }
  }
};
</script>


  
<style scoped>
/* 🌟 Modern Glassmorphic Navbar */
.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem 2rem;
  background: rgba(255, 255, 255, 0.15);
  backdrop-filter: blur(10px);
  box-shadow: 0px 8px 20px rgba(0, 0, 0, 0.1);
  border-radius: 15px;
  margin: 10px auto;
  width: 95%;
  transition: all 0.3s ease-in-out;
}

/* 🚀 Logo Styling */
.logo {
  display: flex;
  align-items: center;
  font-size: 1.7rem;
  font-weight: 700;
  color: #1d3b24;
  cursor: pointer;
  transition: transform 0.3s ease-in-out;
}

.logo:hover {
  transform: scale(1.05);
}

/* 🔥 Icon Styling */
.icon {
  background: linear-gradient(135deg, #28a745, #20c997);
  color: white;
  border-radius: 50%;
  padding: 12px 18px;
  margin-right: 12px;
  font-size: 1.3rem;
  font-weight: bold;
  box-shadow: 0px 5px 15px rgba(0, 0, 0, 0.15);
  transition: all 0.3s ease-in-out;
}

.icon:hover {
  background: linear-gradient(135deg, #20c997, #28a745);
  transform: rotate(360deg);
}

/* 🎨 Navigation Links */
.nav-links {
  display: flex;
  gap: 15px;
}

/* 🖌️ Modern Buttons */
.btn {
  position: relative;
  display: inline-block;
  padding: 12px 30px;
  font-size: 1rem;
  font-weight: 600;
  text-transform: uppercase;
  text-decoration: none;
  border-radius: 50px;
  overflow: hidden;
  transition: all 0.4s ease-in-out;
  cursor: pointer;
  border: none;
  box-shadow: 0px 5px 15px rgba(0, 0, 0, 0.2);
}

/* 🌿 Services Button */
.services-btn {
  background: linear-gradient(135deg, #28a745, #20c997);
  color: white;
}

/* 🔵 Login Button */
.login-btn {
  background: linear-gradient(135deg, #007bff, #6610f2);
  color: white;
}

/* 🏆 Profile Button */
.profile-btn {
  background: linear-gradient(135deg, #1d3b24, #20c997);
  color: white;
}

/* ⚡ Hover Effects */
.btn:hover {
  transform: translateY(-3px);
  box-shadow: 0px 8px 20px rgba(0, 0, 0, 0.3);
}

/* 🏄‍♂️ Water Flow Effect */
.btn::before {
  content: "";
  position: absolute;
  top: 0;
  left: -100%;
  width: 300%;
  height: 100%;
  background: linear-gradient(120deg, transparent, rgba(255, 255, 255, 0.4), transparent);
  transition: all 0.6s ease-in-out;
}

.btn:hover::before {
  left: 100%;
}

/* 📱 Mobile Responsive */
@media (max-width: 768px) {
  .header {
    flex-direction: column;
    align-items: center;
    padding: 1rem;
  }

  .nav-links {
    flex-direction: column;
    gap: 10px;
  }

  .btn {
    font-size: 0.9rem;
    padding: 10px 25px;
  }
}

  </style>
  