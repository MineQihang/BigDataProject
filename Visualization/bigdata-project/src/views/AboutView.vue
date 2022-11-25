<template>
  <div class="about">
    <!-- <h1>This is an about page</h1>
    <div>
      <el-button> Hello </el-button>
    </div> -->
    <div id="chart"></div>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import * as echarts from 'echarts';

onMounted(() => {
  let myChart = echarts.init(document.getElementById('chart'));
  myChart.setOption({
    title: {
      text: 'ECharts 入门示例'
    },
    tooltip: {},
    xAxis: {
      data: ['衬衫', '羊毛衫', '雪纺衫', '裤子', '高跟鞋', '袜子']
    },
    yAxis: {},
    series: [
      {
        name: '销量',
        type: 'bar',
        data: [5, 20, 36, 10, 10, 20]
      }
    ]
  });
})

</script>

<style>
@media (min-width: 1024px) {
  .about {
    min-height: 100vh;
    display: flex;
    align-items: center;
  }
}

#chart {
  width: 100%;
  height: 100px;
}
</style>
