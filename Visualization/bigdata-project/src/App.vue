<script setup>
import { RouterLink, RouterView } from 'vue-router'
import { ref } from 'vue'

const activeIndex = ref('1');

</script>

<template>
  <div>
    <header>
      <el-menu :default-active="activeIndex" class="top-menu" mode="horizontal">
        <el-menu-item index="1">
          <RouterLink to="/">大数据分析</RouterLink>
        </el-menu-item>
        <el-menu-item index="2">
          <RouterLink to="/recommend">视频推荐</RouterLink>
        </el-menu-item>
      </el-menu>
    </header>
    <RouterView />
  </div>
</template>

<style scoped>
header {
  width: 100vw;
  line-height: 1.5;
  max-height: 100vh;
  /* display: flex; */
}

.top-menu {
  justify-content: center;
}
</style>
