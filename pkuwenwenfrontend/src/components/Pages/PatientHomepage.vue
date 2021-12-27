<template>
<div>
  <div id = 'logoimg'>
  <img alt="Vue logo" src="../../assets/logo2.jpeg" height="106" width="256">
  </div>
  <div id = 'text'>
  <p> Patient Homepage </p>
  </div>
  <el-row>
    <el-col :span="12"><div class="grid-content bg-purple">患者真实姓名</div></el-col>
    <el-col :span="12"><div class="grid-content bg-purple-light">患者编号</div></el-col>
  </el-row>
  <el-row>
    <el-col :span="6"><div class="grid-content bg-purple">登录名</div></el-col>
    <el-col :span="6"><div class="grid-content bg-purple-light">性别</div></el-col>
    <el-col :span="12"><div class="grid-content bg-purple">身份证号</div></el-col>
  </el-row>
  <el-row>
    <el-col :span="6"><div class="grid-content bg-purple-light">电话</div></el-col>
    <el-col :span="6"><div class="grid-content bg-purple">电子邮件</div></el-col>
    <el-col :span="6"><div class="grid-content bg-purple-light">出生日期</div></el-col>
    <el-col :span="6"><div class="grid-content bg-purple">进行中的预约数</div></el-col>
  </el-row>
  <div class="">
    <el-table :data="OfficeList" style="width: 30%">
      <el-table-column
        fixed
        prop="office_name"
        label="全部科室"
        width="250">
        <template #default="scope">
          <span class="message-title" @click="openOffice(scope.row.office_name)">
            {{scope.row.office_name}}  {{scope.row.doctor_num}}
          </span>
        </template>
      </el-table-column>
    </el-table>
  </div>
</div>
</template>

<script>
export default {
  name: 'tabs',
  data() {
    return {
      message: 'first',
      showHeader: false,
      OfficeList: Array()
    }
  },
  mounted(){
    this.$http
    .request({
      url: this.$url + '/getOfficeIndex',
      method: 'get',
    })
    .then((response) =>{
      //console.log('get return data')
      console.log(response)
      this.OfficeList = response.data.Officelist
    })
  },

  methods: {
    openOffice (officename) {
       console.log(`dash: ${officename}`);
       this.$router.push({
         path: '/'+ officename + '/DoctorIndex',
       })
    },
  },
}

</script>

<style>
.message-title{
  cursor: pointer;
}
.handle-row{
  margin-top: 30px;
}
.bg-purple {
  background: #d3dce6;
}
.bg-purple-light {
  background: #e5e9f2;
}
/*
#logoimg {
  text-align: left;
}
#text {
  text-align: right;
}
*/
</style>

