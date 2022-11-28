<template>
  <div class="common-layout">
    <el-container>

      <el-aside width="200px">
        <el-row class="" style="width:200px">
          <el-col>
            <el-menu default-active="1">
              <el-menu-item index="1" @click='click1'>
                <el-icon>
                  <icon-menu />
                </el-icon>
                <span>根据文本推荐</span>
              </el-menu-item>

              <el-menu-item index="2" @click='click2'>
                <el-icon>
                  <icon-menu />
                </el-icon>
                <span>根据视频推荐</span>
              </el-menu-item>
            </el-menu>
          </el-col>
        </el-row>
      </el-aside>

      <el-main style="width:100%">
        <div v-if="page.v === '2'">
          two
        </div>

        <div v-if="page.v === '1'">
          <el-row>
            <el-col :span="12">
              <el-form label-width="120px">
                <el-form-item label="描述">
                  <el-input v-model="bytext.text" style="width:300px" />
                </el-form-item>
                <el-form-item>
                  <el-button type="primary" @click="onSubmit">Create</el-button>
                  <el-button>Cancel</el-button>
                </el-form-item>
              </el-form>
            </el-col>

          </el-row>


          <!-- <el-row>
            <div v-for="(pic, idx) in bytext.pics" :key="idx" style="width: 200px;">
              <a :href="'https://www.bilibili.com/video/' + bytext.bvs[idx]" target="_blank">
                <img :src="pic" alt="" style="width: 200px;border-radius: 4px;">
                {{ bytext.titles[idx] }}
              </a>
            </div>

          </el-row> -->
          <el-row v-for="(pic, idx) in bytext.pics" :key="idx">
            <a :href="'https://www.bilibili.com/video/' + bytext.bvs[idx]" target="_blank">
              <el-col :span="6">
                <el-image :src="pic" alt="" style="height:120px; width: 200px; border-radius: 4px; margin: 8px"
                  fit="fill" />
              </el-col>
            </a>
            <el-col :span="18">
              <el-descriptions :title="bytext.titles[idx]" style="margin-top:8px">
                <el-descriptions-item label="播放量">{{ bytext.views[idx] }}</el-descriptions-item>
                <el-descriptions-item label="点赞率">{{ toPercent(bytext.like_rates[idx], 2) }}</el-descriptions-item>
                <el-descriptions-item label="投币率">{{ toPercent(bytext.coin_rates[idx], 3) }}</el-descriptions-item>
                <el-descriptions-item label="收藏率">{{ toPercent(bytext.favorite_rates[idx], 2) }}</el-descriptions-item>
              </el-descriptions>
            </el-col>
            <el-divider />
          </el-row>
        </div>
      </el-main>

    </el-container>
  </div>
</template>

<script setup>
import { onMounted, ref, reactive } from 'vue'
import * as echarts from 'echarts'
import axios from 'axios'
import {
  Document,
  Menu as IconMenu,
  Location,
  Setting,
} from '@element-plus/icons-vue'
const sever = 'http://10.234.160.121:5000'
const page = reactive({
  v: '1',
})
const click1 = () => {
  page.v = '1'
}
const click2 = () => {
  page.v = '2'
}
const bytext = reactive({
  text: '',
  pics: [],
  titles: [],
  bvs: [],
  views: [],
  danmus: [],
  replys: [],
  favorites: [],
  coins: [],
  shares: [],
  likes: [],
  like_rates: [],
  coin_rates: [],
  favorite_rates: [],
  honors: []
})
onMounted(() => {
  // let myChart = echarts.init(document.getElementById('chart'));
  // myChart.setOption({
  //   title: {
  //     text: 'ECharts 入门示例'
  //   },
  //   tooltip: {},
  //   xAxis: {
  //     data: ['衬衫', '羊毛衫', '雪纺衫', '裤子', '高跟鞋', '袜子']
  //   },
  //   yAxis: {},
  //   series: [
  //     {
  //       name: '销量',
  //       type: 'bar',
  //       data: [5, 20, 36, 10, 10, 20]
  //     }
  //   ]
  // });
})
const onSubmit = () => {
  let formData = new FormData()
  formData.append('text', bytext.text)
  axios.post(sever + '/video-recommend/recommend-video', formData)
    .then((res) => {
      console.log('数据：', res)
      let data = res.data.data
      for (let v of data) {
        bytext.titles.push(v.title)
        bytext.pics.push(v.pic)
        bytext.bvs.push(v.bvid)
        let stat = v.stat
        bytext.views.push(stat.view)
        bytext.danmus.push(stat.danmaku)
        bytext.replys.push(stat.reply)
        bytext.favorites.push(stat.favorite)
        bytext.coins.push(stat.coin)
        bytext.shares.push(stat.share)
        bytext.likes.push(stat.like)
        bytext.like_rates.push(stat.like / (stat.view + 1))
        bytext.coin_rates.push(stat.coin / (stat.view + 1))
        bytext.favorite_rates.push(stat.favorite / (stat.view + 1))
      }
    })
}
const toPercent = (point, re) => {
  let str = Number(point * 100).toFixed(re)
  str += "%"
  return str
}
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
