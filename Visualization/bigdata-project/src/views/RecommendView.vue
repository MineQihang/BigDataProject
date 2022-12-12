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
          <el-row>
            <el-col :span="24">
              <el-form label-width="100px" @submit.native.prevent>
                <el-form-item label="多个视频号:">
                  <el-row style="width:900px;margin: 5px 0px;">
                    <el-col :span="8">
                      <el-input v-model="text.id1" style="width:250px" />
                    </el-col>
                    <el-col :span="8">
                      <el-input v-model="text.id2" style="width:250px" />
                    </el-col>
                    <el-col :span="8">
                      <el-input v-model="text.id3" style="width:250px" />
                    </el-col>
                  </el-row>
                  <el-row style="width:900px;margin: 5px 0px;">
                    <el-col :span="8">
                      <el-input v-model="text.id4" style="width:250px" />
                    </el-col>
                    <el-col :span="8">
                      <el-input v-model="text.id5" style="width:250px" />
                    </el-col>
                    <el-col :span="8">
                      <el-input v-model="text.id6" style="width:250px" />
                    </el-col>
                  </el-row>
                </el-form-item>
                <el-form-item>
                  <el-button type="primary" @click="onSubmit2">推荐一下</el-button>
                  <el-button @click="clear">清空</el-button>
                </el-form-item>
              </el-form>
            </el-col>
          </el-row>

          <vedio v-for="(vedio, idx) in list2.vedios" :key="idx" :msg="vedio"></vedio>

        </div>

        <div v-if="page.v === '1'">
          <el-row>
            <el-col :span="24">
              <el-form :inline="true" label-width="300px" @submit.native.prevent>
                <el-form-item label="描述:">
                  <el-input v-model="text.t" style="width:400px" @keyup.enter.native="onSubmit" />
                </el-form-item>
                <el-form-item style="margin-left:30px">
                  <el-button type="primary" @click="onSubmit">推荐一下</el-button>
                  <el-button @click="() => { text.t = '' }">清空</el-button>
                </el-form-item>
              </el-form>
            </el-col>
          </el-row>



          <vedio v-for="(vedio, idx) in list.vedios" :key="idx" :msg="vedio"></vedio>

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
const sever = 'http://219.221.121.47:5000'
const page = reactive({
  v: '1',
})
const click1 = () => {
  page.v = '1'
}
const click2 = () => {
  page.v = '2'
}
let text = reactive({
  t: '',
  id1: '',
  id2: '',
  id3: '',
  id4: '',
  id5: '',
  id6: '',
})

const list = reactive({
  vedios: []
})
const list2 = reactive({
  vedios: []
})
onMounted(() => {

})
const onSubmit = () => {
  let formData = new FormData()
  formData.append('text', text.t)
  axios.post(sever + '/video-recommend/recommend-video-by-text', formData)
    .then((res) => {
      // console.log('数据：', res)
      let data = res.data.data
      list.vedios = []
      for (let v of data) {
        let tmp = {}
        tmp.pic = v.pic
        tmp.title = v.title
        tmp.bv = v.bvid
        tmp.up = v.owner.name
        let stat = v.stat
        tmp.view = stat.view
        tmp.danmu = stat.danmaku
        tmp.reply = stat.reply
        tmp.favorite = stat.favorite
        tmp.coin = stat.coin
        tmp.share = stat.share
        tmp.like = stat.like
        tmp.like_rate = stat.like / (stat.view + 1)
        tmp.coin_rate = stat.coin / (stat.view + 1)
        tmp.favorite_rate = stat.favorite / (stat.view + 1)
        tmp.danmu_rate = stat.danmaku / (stat.view + 1)
        tmp.share_rate = stat.share / (stat.view + 1)
        tmp.reply_rate = stat.reply / (stat.view + 1)
        list.vedios.push(tmp)
      }
    })
}

const onSubmit2 = () => {
  let formData = new FormData()
  let tmp = ''
  for (let i = 1; i <= 6; i++) {
    let id = 'id' + i
    if (text[id]) {
      tmp += text[id]
      tmp += ','
    }
  }
  tmp = tmp.substring(0, tmp.length - 1)
  // console.log(tmp)
  formData.append('videos', tmp)
  axios.post(sever + '/video-recommend/recommend-video-by-videos', formData)
    .then((res) => {
      let data = res.data.data
      list2.vedios = []
      for (let v of data) {
        let tmp = {}
        tmp.pic = v.pic
        tmp.title = v.title
        tmp.bv = v.bvid
        tmp.up = v.owner.name
        let stat = v.stat
        tmp.view = stat.view
        tmp.danmu = stat.danmaku
        tmp.reply = stat.reply
        tmp.favorite = stat.favorite
        tmp.coin = stat.coin
        tmp.share = stat.share
        tmp.like = stat.like
        tmp.like_rate = stat.like / (stat.view + 1)
        tmp.coin_rate = stat.coin / (stat.view + 1)
        tmp.favorite_rate = stat.favorite / (stat.view + 1)
        tmp.danmu_rate = stat.danmaku / (stat.view + 1)
        tmp.share_rate = stat.share / (stat.view + 1)
        tmp.reply_rate = stat.reply / (stat.view + 1)
        list2.vedios.push(tmp)
      }
    })
}
const clear = () => {
  text.id1 = ''
  text.id2 = ''
  text.id3 = ''
  text.id4 = ''
  text.id5 = ''
  text.id6 = ''
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

.el-descriptions__body {
  z-index: 10000;
}
</style>
