import { createRouter, createWebHistory } from 'vue-router';
import LandingPage from '@/views/LandingPage.vue';
import LoginPage from '@/views/LoginPage.vue';
import SignupPage from '@/views/SignupPage.vue';
import AdminDash from '@/views/AdminDash.vue';
import ProfessionalDash from '@/views/ProfessionalDash.vue';
import CustomerDash from '@/views/CustomerDash.vue';
import ServicesPage from '@/views/ServicesPage.vue';
import ManageServices from '@/components/admin/ManageServices.vue';
import ManageUsers from '@/components/admin/ManageUsers.vue';
import ProfesProfile from '@/components/professional/ProfesProfile.vue';
import Analytics from '@/components/admin/Analytics.vue';
import All_Requests from '@/components/admin/All_Requests.vue';
import All_Bookings from '@/components/admin/All_Bookings.vue';

const routes = [
  { path: '/', name: 'LandingPage', component: LandingPage },
  { path: '/login', name: 'Login', component: LoginPage },
  { path: '/signup', name: 'Signup', component: SignupPage }, 
  { path: '/dashboard/admin', name: 'AdminDash', component: AdminDash },
  { path: '/dashboard/professional', name: 'ProfessionalDash', component: ProfessionalDash },
  { path: '/dashboard/customer', name: 'CustomerDash', component: CustomerDash },
  { path: '/services', name: 'ServicesPage', component: ServicesPage },
  { path: '/admin/manage-services', name: 'ManageServices', component: ManageServices },
  { path: '/admin/manage-users', name: 'ManageUsers', component: ManageUsers },
  { path: '/professional/profile', name: 'ProfesProfile', component: ProfesProfile },
  { path: '/admin/analytics', name: 'Analytics', component: Analytics },
  { path: '/admin/all-requests', name: 'All_Requests', component: All_Requests },
  { path: '/admin/all-bookings', name: 'All_Bookings', component: All_Bookings },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
