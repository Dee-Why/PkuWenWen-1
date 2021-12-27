<template>
<div>
  <div id = 'logoimg'>
  <img alt="Vue logo" src="../../assets/logo2.jpeg" height="106" width="256">
  </div>
  <div id = 'text'>
  <p> Patient Homepage </p>
  </div>
  <el-row>
    <el-col :span="12"><div class="grid-content bg-purple">{{realName}}</div></el-col>
    <el-col :span="12"><div class="grid-content bg-purple-light">{{patientID}}</div></el-col>
  </el-row>
  <el-row>
    <el-col :span="6"><div class="grid-content bg-purple">{{userName}}</div></el-col>
    <el-col :span="6"><div class="grid-content bg-purple-light">{{gender}}</div></el-col>
    <el-col :span="12"><div class="grid-content bg-purple">{{idCardNumber}}</div></el-col>
  </el-row>
  <el-row>
    <el-col :span="6"><div class="grid-content bg-purple-light">{{phoneNumber}}</div></el-col>
    <el-col :span="6"><div class="grid-content bg-purple">{{email}}</div></el-col>
    <el-col :span="6"><div class="grid-content bg-purple-light">{{birthday}}</div></el-col>
    <el-col :span="6"><div class="grid-content bg-purple">{{appointmentNumber}}</div></el-col>
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
  data: function() {
    return {
      message: 'first',
      showHeader: false,
      OfficeList: Array(),
      realName: '真实姓名',
      patientID: '患者编号',
      userName: '登录名',
      gender: '性别',
      idCardNumber: '身份证号',
      phoneNumber: '电话号码',
      email: '邮箱',
      birthday: '生日写这里咯',
      appointmentNumber: '预约数233',
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

