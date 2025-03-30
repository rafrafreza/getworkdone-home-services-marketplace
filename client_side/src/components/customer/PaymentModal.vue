<template>
    <div class="modal-overlay">
      <div class="modal-content">
        <h4>Make Payment for {{ request?.service_name || booking?.category  }}</h4>
        <p><strong>Amount:</strong> ₹{{ request?.service_price || request?.package_price || booking?.price }}</p>

  
        <button class="btn btn-primary" @click="processPayment">
          Pay Now
        </button>
  
        <div v-if="paymentSuccess">
          <h4 class="mt-4">Submit a Review</h4>
          <textarea v-model="reviewText" placeholder="Write a review..." class="form-control"></textarea>
          <input type="number" v-model="rating" min="1" max="5" class="form-control mt-2" placeholder="Rate (1-5)">
          <button class="btn btn-success mt-3" @click="submitReview">Submit Review</button>
        </div>
  
        <button class="btn btn-secondary mt-2" @click="$emit('close')">Close</button>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    props: ["request", "booking"],
    data() {
      return {
        paymentSuccess: false,
        reviewText: "",
        rating: 0
      };
    },
    methods: {
      async processPayment() {
        alert("Payment Successful! You can now submit a review.");
        this.paymentSuccess = true;
      },
  
      async submitReview() {
  if (!this.reviewText || this.rating < 1 || this.rating > 5) {
    alert("Please provide a valid rating and review.");
    return;
  }

  try {
    const token = localStorage.getItem("token");
    let url = "";

    if (this.request) {
      // Submit review for service request
      url = `http://127.0.0.1:5000/api/customer/service-review/${this.request.id}`;
    } else if (this.booking) {
      // Submit review for booking
      url = `http://127.0.0.1:5000/api/customer/booking-review/${this.booking.id}`;
    } else {
      alert("Invalid request.");
      return;
    }

    await fetch(url, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify({
        review: this.reviewText,
        rating: this.rating,
      }),
    });

    alert("Review Submitted! Request marked as Completed.");
    // Emit event to notify parent component to refresh requests
    this.$emit("refresh-requests");
    this.$emit("payment-success", this.request?.id || this.booking?.id);
  } catch (error) {
    console.error("Error submitting review:", error);
  }
}

    }
  };
  </script>
  
  <style scoped>
  /* Modal Styling */
  .modal-overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100vw;
    height: 100vh;
    background: rgba(0, 0, 0, 0.5);
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 9999;
  }
  
  .modal-content {
    background: white;
    padding: 20px;
    border-radius: 10px;
    text-align: center;
    width: 400px;
    box-shadow: 0px 5px 15px rgba(0, 0, 0, 0.2);
  }
  </style>
  