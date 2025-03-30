<template>
    <div>
      <canvas ref="barChartCanvas"></canvas>
    </div>
  </template>
  
  <script>
  import { ref, onMounted } from "vue";
  import { Chart } from "chart.js/auto";
  
  export default {
    props: ["chart-data"],
    setup(props) {
      const barChartCanvas = ref(null);
  
      onMounted(() => {
        new Chart(barChartCanvas.value, {
          type: "bar",
          data: props.chartData
        });
      });
  
      return { barChartCanvas };
    }
  };
  </script>
  