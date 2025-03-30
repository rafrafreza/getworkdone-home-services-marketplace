<template>
    <section class="services-section">
      <div class="container">
        <div class="row justify-content-center align-items-center position-relative">
  
          <!-- Service Cards -->
          <div
            v-for="(service, index) in services"
            :key="index"
            class="service-box"
            :class="[{ active: index === activeIndex }, getBoxClass(index)]"
            @click="rotateCards"
          >
            <img :src="service.image" :alt="service.name" />
          </div>
          <!-- Large Center Card -->
          <div class="large-service-box" @click="openServicePage">
            <img :src="services[activeIndex].image" alt="Active Service" />
            <div class="overlay">
              <p>{{ services[activeIndex].name }}</p>
            </div>
          </div>
        </div>
      </div>
    </section>
  </template>
  
  <script>
  export default {
    data() {
      return {
        services: [
          { name: "Cleaning", image: "/images/cleaning.jpg" },
          { name: "AC Servicing", image: "/images/ac_servicing.jpg" },
          { name: "Plumbing", image: "/images/plumbing.jpg" },
          { name: "Cooking", image: "/images/cooking.jpg" },
        ],
        activeIndex: 0,
      };
    },
    methods: {
      rotateCards() {
        this.activeIndex = (this.activeIndex + 1) % this.services.length;
      },
      openServicePage() {
        const selectedService = this.services[this.activeIndex].name;
        window.location.href = `/services?filter=${selectedService}`;
      },
      getBoxClass(index) {
        const positions = ["left", "left-center", "right-center", "right"];
        return positions[index];
      },
    },
  };
  </script>
  
  <style scoped>
  /* General Styling */
  .services-section {
    /* background: #174d9e; */
    padding: 10rem 0;
    position: relative;
    text-align: center;
    margin-bottom: 7rem;
    /* margin-top: 7rem; */
    /* overflow: hidden; Prevents content overflow */
  }
  
  /* Service Boxes */
  .service-box {
    width: 200px;
    height: 250px;
    position: absolute;
    border-radius: 20px;
    border: 1px solid #014f86;
    transition: transform 0.6s ease-in-out, box-shadow 0.3s ease-in-out;
    box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
    cursor: pointer;
    background: white;
    overflow: hidden; /* Ensures images stay inside the box */
  }
  
  /* Positions */
  .left {
    left: 18%;
    top: 50%;
    transform: translateY(-50%) rotate(-10deg);
  }
  .left-center {
    left: 35%;
    top: 50%;
    transform: translateY(-50%) rotate(5deg);
  }
  .right-center {
    right: 35%;
    top: 50%;
    transform: translateY(-50%) rotate(-5deg);
  }
  .right {
    right: 18%;
    top: 50%;
    transform: translateY(-50%) rotate(10deg);
  }
  
  /* Hover Effects */
  .service-box:hover {
    transform: scale(1.1) rotate(0deg);
    box-shadow: 0 8px 20px rgba(0, 0, 0, 0.2);
  }
  
  /* Large Service Box */
  .large-service-box {
    width: 400px;
    height: 300px;
    border-radius: 25px;
    border: 2px solid #014f86;
    background: white;
    position: absolute;
    left: 50%;
    top: 60%;
    transform: translateX(-50%);
    cursor: pointer;
    transition: transform 0.4s ease-in-out, box-shadow 0.3s ease-in-out;
    overflow: hidden; /* Ensures content does not overflow */
    box-shadow: 0 8px 25px rgba(0, 0, 0, 0.2);
  }
  
  /* Hover Animation */
  .large-service-box:hover {
    transform: translateX(-50%) scale(1.05);
  }
  
  /* Image Styling */
  .service-box img,
  .large-service-box img {
    width: 100%;
    height: 100%;
    border-radius: 20px;
    object-fit: cover;
    display: block; /* Removes any unwanted space */
  }
  
  /* Overlay on Large Card */
  .overlay {
    position: absolute;
    bottom: 0;
    width: 100%;
    height: 50px;
    background: rgba(1, 79, 134, 0.85);
    color: white;
    text-align: center;
    font-size: 1.5rem;
    font-weight: bold;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: height 0.4s ease-in-out;
    overflow: hidden; /* Prevents text from overflowing */
  }
  
  /* Show More Text on Hover */
  .large-service-box:hover .overlay {
    height: 80px;
    font-size: 1.8rem;
  }

  .service-box, 
  .large-service-box {
    padding: 0;
    /* border: none; */
  }

  </style>
