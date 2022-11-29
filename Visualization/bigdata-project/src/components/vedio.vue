<script setup>
defineProps({
    msg: {
        type: Object,
        required: true
    }
})
const toPercent = (point, re) => {
    let str = Number(point * 100).toFixed(re)
    str += "%"
    return str
}
</script>

<template>
    <el-row>
        <el-col :span="4">
            <a :href="'https://www.bilibili.com/video/' + msg.bv" target="_blank" >
            <el-image :src="msg.pic" alt=""
                style="height:120px;height:120px; width: 200px; border-radius: 4px;margin: 8px" fit="fill" /></a>
        </el-col>
        <el-col :span="20">
            <el-row style="font-size: 17px;font-weight: 700;margin: 5px;">
                <a :href="'https://www.bilibili.com/video/' + msg.bv" target="_blank" style="color:black">
                {{ msg.title }}</a>
            </el-row>
            <el-row class="content-row">
                <el-col :span="6">
                    <img src="../../static/up.svg" class="icon" style="" alt="">
                    <span class="value">{{ msg.up }}</span>
                </el-col>
                <el-col :span="6">
                    <img src="../../static/play.svg" class="icon" alt="">
                    <span class="name">播放量:</span>
                    <span class="value">{{ msg.view }}</span>
                </el-col>
                <el-col :span="6">
                    <img src="../../static/like.svg" class="icon" alt="">
                    <span class="name">点赞:</span>
                    <span class="value">{{ msg.like + ' ' }}({{ toPercent(msg.like_rate, 2) }})</span>
                </el-col>
                <el-col :span="6" style="">
                    <img src="../../static/coin.svg" class="icon" style="height: 24px;" alt="">
                    <span class="name" style="">投币:</span>
                    <span class="value">{{ msg.coin + ' ' }}({{ toPercent(msg.coin_rate, 3) }})</span>
                </el-col>
            </el-row>
            <el-row class="content-row">
                <el-col :span="6">
                    <img src="../../static/favorites-o.svg" class="icon" style="width:18px;height:18px;" alt="">
                    <span class="name">收藏:</span>
                    <span class="value">{{ msg.favorite + ' ' }}({{ toPercent(msg.favorite_rate, 2) }})</span>
                </el-col>
                <el-col :span="6">
                    <img src="../../static/share.svg" class="icon" style="width:18px;height:18px;" alt="">
                    <span class="name">分享:</span>
                    <span class="value">{{ msg.share + ' ' }}({{ toPercent(msg.share_rate, 3) }})</span>
                </el-col>
                <el-col :span="6">
                    <img src="../../static/danmu.svg" class="icon" style="" alt="">
                    <span class="name">弹幕:</span>
                    <span class="value">{{ msg.danmu + ' ' }}({{ toPercent(msg.danmu_rate, 3) }})</span>
                </el-col>
                <el-col :span="6">
                    <img src="../../static/comment.svg" class="icon" style="" alt="">
                    <span class="name">评论:</span>
                    <span class="value">{{ msg.reply + ' ' }}({{ toPercent(msg.reply_rate, 3) }})</span>
                </el-col>
            </el-row>
            <el-row class="content-row">
                <el-col v-if="msg.honor">
                    <img src="../../static/honor.svg" class="icon" style="" alt="">
                    <span class="name">荣誉:</span>
                    <span class="value">{{ msg.honor }}</span>
                </el-col>
            </el-row>
        </el-col>
        <el-divider style="margin:0px 0px 10px 0px" />
    </el-row>
</template>

<style scoped>
.content-row {
    margin: 8px 5px;
}

.icon {
    height: 20px;
    width: 20px;
    vertical-align: middle;
}

.name {
    position: static;
    padding: 0px;
    margin-left: 2px;
    line-height: 20px;
    vertical-align: middle;
}

.value {
    position: static;
    padding: 0px;
    margin-left: 2px;
    line-height: 20px;
    vertical-align: middle;
}

a :link {
    color: rgba(0, 0, 0, 0.627);
}

a :visited {
    color: black;
}
</style>
