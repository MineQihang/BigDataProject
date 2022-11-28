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
                <span>整体情况</span>
              </el-menu-item>

              <el-menu-item index="2" @click='click2'>
                <el-icon>
                  <icon-menu />
                </el-icon>
                <span>个体情况</span>
              </el-menu-item>
            </el-menu>
          </el-col>
        </el-row>
      </el-aside>

      <el-main style="width:100%">
        <div v-show="page.v === '1'">
          one
        </div>

        <div v-show="page.v === '2'">
          <el-row>
            <el-col :span="12">
              <el-form label-width="120px">
                <el-form-item label="视频bv或av号">
                  <el-input v-model="sing.id" style="width:300px" />
                </el-form-item>
                <el-form-item>
                  <el-button type="primary" @click="onSubmit">查询</el-button>
                  <el-button>清空</el-button>
                </el-form-item>
              </el-form>
            </el-col>
          </el-row>

          <el-row>
            <el-col :span="4">
              <el-image :src="sing.pic" alt=""
                style="height:120px;height:120px; width: 200px; border-radius: 4px;margin: 8px" fit="fill" />
            </el-col>
            <el-col :span="20">
              <el-descriptions :title="sing.title" style="margin-top:8px">
                <el-descriptions-item label="播放量">{{ sing.view }}</el-descriptions-item>
                <el-descriptions-item label="点赞率">{{ toPercent(sing.like_rate, 2) }}</el-descriptions-item>
                <el-descriptions-item label="投币率">{{ toPercent(sing.coin_rate, 3) }}</el-descriptions-item>
                <el-descriptions-item label="收藏率">{{ toPercent(sing.favorite_rate, 2) }}</el-descriptions-item>
                <el-descriptions-item v-if="sing.honor" label="荣誉">
                  {{ sing.honor }}
                </el-descriptions-item>
              </el-descriptions>
            </el-col>
            <el-divider style="margin-top:0px" />
          </el-row>

          <el-row>
            <el-col :span="11">
              <div id="wordcloud-chart" style="height:400px; width:400px;"></div>
            </el-col>

            <el-col :span="13">
              <div id="pie-chart" style="height:400px; width:400px;"></div>
            </el-col>
          </el-row>
        </div>
      </el-main>

    </el-container>
  </div>
</template>


<script setup>
import { onMounted, ref, reactive } from 'vue'
import axios from 'axios'
import * as echarts from 'echarts'
import 'echarts-wordcloud'
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
const sing = reactive({
  id: '',
  pic: 'http://i2.hdslb.com/bfs/archive/c463451672bb74453c7229651dcb39be8fae13d7.jpg',
  title: "电子监听、全国断网，棱镜门背后，中国如何从末路狂奔到世界之巅",
  view: 0,
  danmu: 0,
  reply: 0,
  favorite: 0,
  coin: 0,
  share: 0,
  like: 0,
  like_rate: 0,
  coin_rate: 0,
  favorite_rate: 0,
  honor: "",
  word_data: [{ "value": "42", "name": "存活", }, { value: '30', name: 'VIVO' }],
  pie: []
})
const onSubmit = () => {
  let formData = new FormData()
  formData.append('video_id', sing.id)
  axios.post(sever + '/single-video/basic-info', formData)
    .then((res) => {
      let data = res.data.data
      sing.pic = data.pic
      sing.title = data.title
      let stat = data.stat
      sing.view = stat.view
      sing.danmu = stat.danmaku
      sing.reply = stat.reply
      sing.favorite = stat.favorite
      sing.coin = stat.coin
      sing.share = stat.share
      sing.like = stat.like
      sing.like_rate = stat.like_rate
      sing.coin_rate = stat.coin_rate
      sing.favorite_rate = stat.favorite_rate
      sing.honor = ''
      for (let h of data.honor) {
        sing.honor += h.desc
        sing.honor += '，'
      }
    })
  axios.post(sever + '/single-video/replies-word-data', formData)
    .then((res) => {

      let data = res.data.data.word_data
      sing.word_data = []
      for (let i of data) {
        let tmp = {}
        tmp['value'] = String(i[1])
        tmp['name'] = i[0]
        sing.word_data.push(tmp)
        if (sing.word_data.length >= 25) break
      }

      let myChart = echarts.init(document.getElementById("wordcloud-chart"))
      // echarts参数设置
      myChart.setOption({
        backgroundColor: '#fff', // canvas背景颜色
        // canvas标题配置项
        title: {
          text: '评论云图',
          left: '-1%',
          textStyle: {
            fontSize: 14,
            color: '#3B3E41',
            fontWeight: 'normal'
          }
        },
        series: [
          {
            type: 'wordCloud',
            left: '10%',                 // X轴偏移量
            top: '0%',                  // Y轴偏移量
            width: '100%',               // canvas宽度大小
            height: '100%',              // canvas高度大小
            sizeRange: [12, 50],         //  词典字体大小范围配置
            rotationRange: [0, 0],       // 词典字体旋转角度配置，默认不旋转
            gridSize: 25,                // 词典字体间距配置
            layoutAnimation: true,       // 为false词典过度会阻塞
            textStyle: {                 // 词典样式配置
              normal: {
                color() {
                  // 颜色随机渐变
                  let colors = ['#fe9a8bb3', '#fe9a8bb3', '#fe9a8b03', '#9E87FFb3', '#9E87FFb3', '#9E87FFb3', '#fe9a8bb3', '#fe9a8bb3', '#fe9a8bb3', '#73DDFF', '#58D5FF']
                  return colors[parseInt(Math.random() * 10)]
                }
              }
            },
            // 渲染词典数据
            // data: [{
            //   // value: '50',          // 词典大小配置
            //   // name: '评论云图'     // 词典名称配置
            //   // textStyle: {          // 单独配置某个词典样式
            //   //   shadowBlur: 4,
            //   //   shadowOffsetY: 14,
            //   //   color: '#BDBEFA'
            //   // }
            // },
            // { value: '30', name: 'VIVO' },
            // ]
            data: sing.word_data
          }
        ]
      })
    })

  // axios.post(sever + '/single-video/replies-sentiment', formData)
  //   .then((res) => {

  //     let data = res.data.data
  //     console.log('数据：', data)
  //     sing.pie = [{ value: data.pos_rate + 1, name: '好评' },
  //     { value: data.neg_rate + 1, name: '差评' }]

  //     var chartDom = document.getElementById('pie-chart')
  //     var myChart = echarts.init(chartDom)
  //     var option

  //     option = {
  //       title: {
  //         text: 'Referer of a Website',
  //         subtext: 'Fake Data',
  //         left: 'center'
  //       },
  //       tooltip: {
  //         trigger: 'item'
  //       },
  //       legend: {
  //         orient: 'vertical',
  //         left: 'left'
  //       },
  //       series: [
  //         {
  //           name: 'Access From',
  //           type: 'pie',
  //           radius: '50%',
  //           data: sing.pie,
  //           emphasis: {
  //             itemStyle: {
  //               shadowBlur: 10,
  //               shadowOffsetX: 0,
  //               shadowColor: 'rgba(0, 0, 0, 0.5)'
  //             }
  //           }
  //         }
  //       ]
  //     }

  //     option && myChart.setOption(option)
  //   })

}
const toPercent = (point, re) => {
  let str = Number(point * 100).toFixed(re)
  str += "%"
  return str
}

// defineExpose({
//   page,
//   click1,
//   click2
// })

onMounted(() => {

})

</script>

