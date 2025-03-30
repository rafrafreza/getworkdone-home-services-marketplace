<template>
  <footer class="footer bg-dark text-light py-4">
    <div class="container">
      <div class="row d-flex align-items-start justify-content-between">
        <!-- Left Side (Company Info) -->
        <div class="col-md-4 text-start">
          <h4>getworkdone.com</h4>
          <p>Your trusted home services partner.</p>
          <p><i class="fas fa-phone"></i> +91 9999999999</p>
          <p><i class="fas fa-envelope"></i> support@getworkdone.com</p>
          <p><i class="fas fa-map-marker-alt"></i> 123, New Delhi</p>
        </div>

        <!-- Center (Quick Links) -->
        <div class="col-md-4 text-center">
          <h5>Quick Links</h5>
          <ul class="list-unstyled">
            <li><a href="#" class="text-light text-decoration-none">Home</a></li>
            <li><a href="#" class="text-light text-decoration-none">Our Services</a></li>
            <li><a href="#" class="text-light text-decoration-none">Book a Service</a></li>
            <li><a href="#" class="text-light text-decoration-none">FAQs</a></li>
            <li><a href="#" class="text-light text-decoration-none">Contact Us</a></li>
          </ul>
        </div>

        <!-- Right Side (Social Media) -->
        <div class="col-md-4 text-end">
          
        </div>
      </div>

      <!-- Copyright -->
      <div class="text-center mt-3">
        <small>&copy; 2025 Getworkdone. All rights reserved.</small>
      </div>
    </div>
  </footer>
</template>

<style scoped>
.footer {
  border-top: 5px solid #28a745;
  background-color: #1b1b1b;
  padding: 3rem 0;
}

.footer h5 {
  font-size: 1.2rem;
  font-weight: 600;
  color: #28a745;
}

.footer h4 {
  font-size: 1.2rem;
  font-weight: 600;
  color: #19c741;
}

.footer p,
.footer a {
  font-size: 1rem;
  color: #ccc;
}

.footer a {
  text-decoration: none;
  transition: color 0.3s ease-in-out;
}

.footer a:hover {
  color: #28a745 !important;
  text-decoration: underline;
}

.footer i {
  font-size: 1.5rem;
  transition: transform 0.3s ease-in-out;
}

.footer i:hover {
  transform: scale(1.2);
  color: #28a745;
}

small {
  color: #bbb;
}
</style>
