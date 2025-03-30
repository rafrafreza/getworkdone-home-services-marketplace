<template>
  <div class="landing-page">
    <Navbar />
    <HeroSection />
    <ServiceHeader/>
    <AboutUs />
    <FooterSection />
  </div>
</template>

<script>
import Navbar from "@/components/Navbar.vue";
import HeroSection from "@/components/HeroSection.vue";
import ServiceHeader from "@/components/ServiceHeader.vue";
import AboutUs from "@/components/common/AboutUs.vue";
import FooterSection from "@/components/FooterSection.vue";

export default {
  name: "LandingPage",
  components: {
    Navbar,
    HeroSection,
    ServiceHeader,
    AboutUs,
    FooterSection,
  },
};
</script>

<style scoped>
.landing-page {
  font-family: Arial, sans-serif;
  text-align: center;
  color: #333;
  padding: 0 2rem;
}
</style>
