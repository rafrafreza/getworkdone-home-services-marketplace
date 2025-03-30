<template>
    <div>
      <canvas ref="pieChartCanvas"></canvas>
    </div>
  </template>
  
  <script>
  import { ref, onMounted } from "vue";
  import { Chart } from "chart.js/auto";
  
  export default {
    props: ["chart-data"],
    setup(props) {
      const pieChartCanvas = ref(null);
  
      onMounted(() => {
        new Chart(pieChartCanvas.value, {
          type: "pie",
          data: props.chartData
        });
      });
  
      return { pieChartCanvas };
    }
  };
  </script>
  