<template>
    <body>
        <div id="app" class="container mt-5">
            <h2 class="mb-4 text-center text-primary">Available Services</h2>

            <!-- Search, Filter & Sort Controls -->
            <div class="d-flex mb-3 gap-3">
                <input type="text" v-model="searchQuery" placeholder="🔍 Search Services..." class="form-control w-50">
                <select v-model="sortOrder" class="form-select">
                    <option value="asc">Sort by Price (Low to High) ⬆️</option>
                    <option value="desc">Sort by Price (High to Low) ⬇️</option>
                </select>
                <input type="number" v-model="maxPrice" placeholder="💰 Max Price" class="form-control w-25">
            </div>

            <ul class="list-group shadow">
                <li v-for="service in filteredServices" :key="service.id" 
                    class="list-group-item d-flex justify-content-between align-items-center p-3 service-item"
                    @click="selectService(service)">
                    <span class="fw-bold">{{ service.name }}</span>
                    <span class="">{{ service.category }}</span>
                    <span class="fw-bold">{{ service.rating }}Rating</span>
                    <span class="badge bg-primary fs-6">₹{{ service.base_price }}</span>
                </li>
            </ul>
            <div v-if="filteredServices.length === 0" class="text-center mt-4">
                <p class="no-results">No servicess found matching your criteria.</p>
            </div>

            <!-- Service Details Modal -->
            <div v-if="selectedService" class="modal-backdrop">
                <div class="modal-dialog modal-lg">
                    <div class="modal-content p-3">
                        <div class="modal-header">
                            <h5 class="modal-title text-primary">{{ selectedService.name }}</h5>
                            <button type="button" class="btn-close" @click="selectedService = null"></button>
                        </div>
                        <div class="modal-body">
                            <p><strong>💰 Price:</strong> ₹{{ selectedService.base_price }}</p>
                            <p><strong>⏳ Time Required:</strong> {{ selectedService.time_required }}</p>
                            <p><strong>📖 Description:</strong> {{ selectedService.description }}</p>
                            <div class="text-end">
                                <button class="btn btn-success btn-lg" @click="showRequestForm = true">
                                    Request Service 🚀
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Request Service Form Modal -->
            <div v-if="showRequestForm" class="modal-backdrop">
                <div class="modal-dialog">
                    <div class="modal-content p-4">
                        <div class="modal-header">
                            <h5 class="modal-title text-success">Request Service</h5>
                            <button type="button" class="btn-close" @click="showRequestForm = false"></button>
                        </div>
                        <div class="modal-body">
                            <form @submit.prevent="submitRequest">
                                <div class="mb-3">
                                    <label class="form-label">📅 Preferred Date & Time</label>
                                    <input type="datetime-local" v-model="serviceDateTime" class="form-control" required>
                                </div>
                                <div class="text-end">
                                    <button type="submit" class="btn btn-primary btn-lg">Submit Request ✅</button>
                                </div>
                            </form>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </body>
</template>

<script>
import axios from 'axios';
export default {
    data() {
        return {
            services: [],
            selectedService: null,
            showRequestForm: false,
            serviceDateTime: '',
            searchQuery: '',
            sortOrder: 'asc',
            maxPrice: ''
        };
    },
    computed: {
        filteredServices() {
            let result = this.services;

            // 🔍 Search by Name
            if (this.searchQuery) {
                result = result.filter(service =>
                    service.name.toLowerCase().includes(this.searchQuery.toLowerCase())
                );
            }

            // 💰 Filter by Max Price
            if (this.maxPrice) {
                result = result.filter(service => service.base_price <= this.maxPrice);
            }

            // ⬆️⬇️ Sort by Price
            result.sort((a, b) => {
                return this.sortOrder === 'asc' 
                    ? a.base_price - b.base_price 
                    : b.base_price - a.base_price;
            });

            return result;
        }
    },
    mounted() {
        this.fetchServices();
    },
    methods: {
        async fetchServices() {
            try {
                const response = await axios.get('http://127.0.0.1:5000/api/services');
                this.services = response.data.services;
            } catch (error) {
                console.error('Error fetching services:', error);
            }
        },
        selectService(service) {
            this.selectedService = service;
        },
        async submitRequest() {
            const token = localStorage.getItem("token");
            if (!token) {
                alert("Please log in first.");
                window.location.href = "/login";
                return;
            }
            
            try {
                const response = await axios.get("http://127.0.0.1:5000/dashboard/customer", {
                    headers: { Authorization: `Bearer ${token}` }
                });
                const customerId = response.data.customer_id;
                
                await axios.post('http://127.0.0.1:5000/api/customers/service-requests/create', {
                    service_id: this.selectedService.id,
                    customer_id: customerId,
                    service_dateTime: this.serviceDateTime
                }, {
                    headers: { Authorization: `Bearer ${token}` }
                });
                
                alert('🎉 Service request submitted successfully!');
                this.showRequestForm = false;
                this.selectedService = null;
            } catch (error) {
                console.error('Error submitting request:', error);
                alert("Failed to submit request. Please try again.");
            }
        }
    }
}
</script>

<style scoped>
/* Style for Service List */
.service-item {
    cursor: pointer;
    transition: background 0.3s ease-in-out;
}
.service-item:hover {
    background: #f8f9fa;
    transform: scale(1.02);
}

/* Modal Styling */
.modal-backdrop {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.5);
    display: flex;
    align-items: center;
    justify-content: center;
}

/* Modal Box */
.modal-content {
    background: white;
    border-radius: 10px;
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
}
</style>
