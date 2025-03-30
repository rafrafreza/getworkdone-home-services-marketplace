<template>
  <div class="container vh-100 d-flex align-items-center justify-content-center">
    <div class="row shadow-lg rounded p-4 bg-white form-container">
      <div class="col-md-6 d-none d-md-flex align-items-center justify-content-center">
        <img :src="imageUrl" alt="Signup Image" class="img-fluid rounded shadow-lg" />
      </div>

      <div class="col-md-6 d-flex flex-column justify-content-center px-4">
        <h2 class="text-center text-primary fw-bold">Sign Up as {{ userType }}</h2>
        
        <div class="d-flex gap-3 justify-content-center mt-3">
          <button class="btn btn-outline-primary" :class="{ 'active-btn': isProfessional }" @click="setUserType('Professional')">
            Professional
          </button>
          <button class="btn btn-outline-success" :class="{ 'active-btn': !isProfessional }" @click="setUserType('Customer')">
            Customer
          </button>
        </div>

        <ProfessionalSignup v-if="isProfessional" />
        <CustomerSignup v-else />
      </div>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue';
import ProfessionalSignup from '@/components/ProfessionalSignup.vue';
import CustomerSignup from '@/components/CustomerSignup.vue';

export default {
  components: { ProfessionalSignup, CustomerSignup },
  setup() {
    const userType = ref('Customer');
    const isProfessional = ref(false);
    const imageUrl = ref(`https://picsum.photos/500/500?random=${Date.now()}`);

    const setUserType = (type) => {
      userType.value = type;
      isProfessional.value = type === 'Professional';
      imageUrl.value = `https://picsum.photos/500/500?random=${Date.now()}`;
    };

    return { userType, isProfessional, setUserType, imageUrl };
  }
};
</script>

<style scoped>
.form-container {
  width: 90%;
  max-width: 900px;
}

.btn.active-btn {
  background-color: #007bff !important;
  color: white !important;
}
</style>
