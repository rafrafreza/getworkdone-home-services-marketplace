<template>
  <div>
    <ProfesNavbar :currentPage="page" @change-page="page = $event" />

    <div class="container mt-4">
      <JobSection 
        v-if="page === 'jobs'" 
        :serviceRequests="serviceRequests"
        :packageRequests="packageRequests"
        :directBookings="directBookings"
        @accept-service="acceptService"
        @accept-package="acceptPackage"
        @accept-booking="acceptBooking"
        @reject-booking="rejectBooking"
      />

      <ServiceSection 
        v-if="page === 'services'" 
        :ongoingServices="ongoingServices" 
        :completedServices="completedServices" 
      />

      <ProfesProfile 
        v-if="page === 'profile'" 
        :profile="profile" 
        :newPackages="newPackages"
        @apply-package="applyPackage"
      />
    </div>
  </div>
</template>

<script>
import ProfesNavbar from '@/components/professional/ProfesNavbar.vue';
import JobSection from '@/components/professional/JobSection.vue';
import ServiceSection from '@/components/professional/ServiceSection.vue';
import ProfesProfile from '@/components/professional/ProfesProfile.vue';

export default {
  name: 'ProfessionalDashboard',
  components: { ProfesNavbar, JobSection, ServiceSection, ProfesProfile },
  data() {
    return {
      page: 'jobs',
      serviceRequests: [{ id: 1, name: "Plumbing Request" }, { id: 2, name: "Electrician Request" }],
      packageRequests: [{ id: 1, name: "Gold Membership" }, { id: 2, name: "Silver Membership" }],
      directBookings: [{ id: 1, customer: "John Doe" }, { id: 2, customer: "Jane Doe" }],
      ongoingServices: [{ id: 1, name: "House Cleaning" }, { id: 2, name: "AC Repair" }],
      completedServices: [{ id: 3, name: "Roof Fixing" }, { id: 4, name: "Garden Work" }],
      profile: { name: "Professional User", email: "pro@example.com" },
      newPackages: [{ id: 1, name: "VIP Package" }, { id: 2, name: "Startup Package" }]
    };
  },
  methods: {
    acceptService(id) { alert(`Accepted service request ID: ${id}`); },
    acceptPackage(id) { alert(`Accepted package request ID: ${id}`); },
    acceptBooking(id) { alert(`Accepted booking ID: ${id}`); },
    rejectBooking(id) { alert(`Rejected booking ID: ${id}`); },
    applyPackage(id) { alert(`Applied for package ID: ${id}`); }
  }
};
</script>
