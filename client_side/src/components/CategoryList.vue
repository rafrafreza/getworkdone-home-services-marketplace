<template>
  <div class="card category-card">
    <div class="header">
      <h4 class="text-primary">What are you looking for?</h4>
      <!-- <input 
        type="text" 
        v-model="searchcategory" 
        class="form-control search-box" 
        placeholder="Search categories..."
      /> -->
    </div>

    <div class="categorys-container">
      <div 
        v-for="(category, index) in filteredCategories" 
        :key="category.id" 
        class="category-item">
        <img :src="category.picture || `https://picsum.photos/100/100?random=${index}`" class="category-img" alt="category Image" />
        <!-- <img :src="`https://picsum.photos/100/100?random=${index}`" class="category-img" alt="category Image" /> -->
        <span class="category-name">{{ category.name }}</span>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      searchcategory: "",
      categories: [],
    };
  },
  computed: {
    filteredCategories() {
      return this.categories.filter(category => 
        category.name.toLowerCase().includes(this.searchcategory.toLowerCase())
      );
    }
  },
  methods: {
    async fetchCategories() {
      try {
        const response = await axios.get("http://localhost:5000/api/service-categories");
        this.categories = response.data.categories;
      } catch (error) {
        console.error("Error fetching categories:", error);
      }
    }
  },
  mounted() {
    this.fetchCategories();
  }
};
</script>

<style scoped>
/* General Card Styling */
.category-card {
  background: #ffffff;
  border: none;
  padding: 1.5rem;
  transition: all 0.3s ease-in-out;
  margin: 20px auto;
  max-width: 1400px;
  text-align: center;
}

/* Header Styling */
.header {
  display: flex;
  justify-content: center;
  align-items: center;
  position: relative;
}

.search-box {
  width: 200px;
  padding: 8px;
  border-radius: 20px;
  border: 1px solid #ddd;
  outline: none;
  transition: all 0.3s ease;
}

.search-box:focus {
  border-color: #007bff;
  box-shadow: 0px 0px 8px rgba(0, 123, 255, 0.5);
}

/* category Grid Layout */
.categorys-container {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 20px;
  margin-top: 20px;
}

.category-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 110px;
  cursor: pointer;
  transition: transform 0.3s ease;
}

.category-item:hover {
  transform: translateY(-5px);
}

/* category Image */
.category-img {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  object-fit: cover;
  box-shadow: 0px 5px 10px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s ease;
}

.category-item:hover .category-img {
  transform: scale(1.1);
}

/* category Name */
.category-name {
  margin-top: 8px;
  font-weight: 600;
  color: #333;
  font-size: 14px;
}

/* Responsive Design */
@media (max-width: 480px) {
  .categorys-container {
    gap: 15px;
  }

  .category-item {
    width: 90px;
  }
}
</style>
