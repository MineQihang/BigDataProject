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
                  <el-button>清空</el-button>
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
                  <el-button>清空</el-button>
                </el-form-item>
              </el-form>
            </el-col>
          </el-row>



          <vedio v-for="(vedio, idx) in list.vedios" :key="idx" :msg="vedio"></vedio>
          <!--
          <el-row v-for="(pic, idx) in bytext.pics" :key="idx">
            <a :href="'https://www.bilibili.com/video/' + bytext.bvs[idx]" target="_blank">
              <el-col :span="6">
                <el-image :src="pic" alt="" style="height:120px; width: 200px; border-radius: 4px; margin: 8px"
                  fit="fill" />
              </el-col>
            </a>

            <el-col :span="18">
              <a :href="'https://www.bilibili.com/video/' + bytext.bvs[idx]" target="_blank">
                <el-descriptions :title="bytext.titles[idx]" column="4" style="margin-top:8px">
                  <el-descriptions-item label="up">{{ bytext.ups[idx] }}</el-descriptions-item>
                  <el-descriptions-item label="播放量">{{ bytext.views[idx] }}</el-descriptions-item>
                  <el-descriptions-item label="点赞">
                    {{ bytext.likes[idx] + ' ' }}({{ toPercent(bytext.like_rates[idx], 2) }})
                  </el-descriptions-item>
                  <el-descriptions-item label="投币">
                    {{ bytext.coins[idx] + ' ' }}({{ toPercent(bytext.coin_rates[idx], 3) }})
                  </el-descriptions-item>
                  <el-descriptions-item label="收藏">
                    {{ bytext.favorites[idx] + ' ' }}({{ toPercent(bytext.favorite_rates[idx], 2) }})
                  </el-descriptions-item>
                  <el-descriptions-item label="分享">
                    {{ bytext.shares[idx] + ' ' }}({{ toPercent(bytext.share_rates[idx], 3) }})
                  </el-descriptions-item>
                  <el-descriptions-item label="弹幕">
                    {{ bytext.danmus[idx] + ' ' }}({{ toPercent(bytext.danmu_rates[idx], 3) }})
                  </el-descriptions-item>
                  <el-descriptions-item label="评论">
                    {{ bytext.replys[idx] + ' ' }}({{ toPercent(bytext.reply_rates[idx], 3) }})
                  </el-descriptions-item>
                </el-descriptions>
              </a>
            </el-col>
            <el-divider />
          </el-row> -->
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
let text = reactive({
  t: '',
  id1: '',
  id2: '',
  id3: '',
  id4: '',
  id5: '',
  id6: '',
})
// let temp = reactive({
//   pics: [],
//   titles: [],
//   bvs: [],
//   ups: [],
//   views: [],
//   danmus: [],
//   replys: [],
//   favorites: [],
//   coins: [],
//   shares: [],
//   likes: [],
//   like_rates: [],
//   coin_rates: [],
//   favorite_rates: [],
//   danmu_rates: [],
//   share_rates: [],
//   reply_rates: [],
//   honors: []
// })
// let bytext = temp
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
      // bytext = temp
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
      // for (let v of data) {
      //   bytext.titles.push(v.title)
      //   bytext.pics.push(v.pic)
      //   bytext.bvs.push(v.bvid)
      //   bytext.ups.push(v.owner.name)
      //   let stat = v.stat
      //   bytext.views.push(stat.view)
      //   bytext.danmus.push(stat.danmaku)
      //   bytext.replys.push(stat.reply)
      //   bytext.favorites.push(stat.favorite)
      //   bytext.coins.push(stat.coin)
      //   bytext.shares.push(stat.share)
      //   bytext.likes.push(stat.like)
      //   bytext.like_rates.push(stat.like / (stat.view + 1))
      //   bytext.coin_rates.push(stat.coin / (stat.view + 1))
      //   bytext.favorite_rates.push(stat.favorite / (stat.view + 1))
      //   bytext.danmu_rates.push(stat.danmaku / (stat.view + 1))
      //   bytext.reply_rates.push(stat.reply / (stat.view + 1))
      //   bytext.share_rates.push(stat.share / (stat.view + 1))
      //   // let tmp = ''
      //   // for (let h of v.honor) {
      //   //   tmp += h.desc
      //   //   tmp += '，'
      //   // }
      //   // tmp -= '，'
      //   // bytext.honors.push(tmp)
      // }
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
