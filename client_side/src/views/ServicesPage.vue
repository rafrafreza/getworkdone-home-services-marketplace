<template>
    <div class="container mt-4">
      <Navbar :hideServicesButton="true" />
      <CategoryList />
      <GeneralServices />
      <PackageList />
      <ProfessionalList />
      <FooterSection />
    </div>
  </template>
  
  <script>
  import Navbar from "@/components/Navbar.vue";
  import CategoryList from "@/components/CategoryList.vue";
  import PackageList from "@/components/PackageList.vue";
  import ProfessionalList from "@/components/ProfessionalList.vue";
  // import Footer from "@/components/FooterSection.vue";
  import FooterSection from "@/components/FooterSection.vue";
  import GeneralServices from "@/components/GeneralServices.vue";
  
  export default {
    components: {
      Navbar,
      CategoryList,
      GeneralServices,
      PackageList,
      ProfessionalList,
      FooterSection,
    },
  };
  </script>
  