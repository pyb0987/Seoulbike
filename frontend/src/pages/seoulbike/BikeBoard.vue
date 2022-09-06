<template>
    <div class="admin-page">
      <div ref="scroll"></div>
      <h1 class="card-title text-center my-3">{{$t('admin.adminPage')}}</h1>
    <div class="row justify-content-center">
      <div class="col-md-10">
        <card>
            <div class="row d-flex align-items-center">
              <div class="col-md-5">
                <el-select
                  class="select-primary"
                  size="large"
                  :placeholder="$t('admin.type')"
                  v-model="selects.type"
                >
                  <el-option
                    v-for="option in selects.types"
                    class="select-primary"
                    :value="option.value"
                    :label="option.label"
                    :key="option.value"
                  >
                  </el-option>
                </el-select>
              </div>
            </div>
        </card>
      </div>
      <div class="col-md-12">
      <card card-body-classes="table-full-width">
          <h4 slot="header" class="card-title">Paginated Tables</h4>
          <div>
            <div
              class="col-12 d-flex justify-content-center justify-content-sm-between flex-wrap"
            >
              <el-select
                class="select-primary mb-3 pagination-select"
                v-model="pagination.perPage"
                placeholder="Per page"
              >
                <el-option
                  class="select-primary"
                  v-for="item in pagination.perPageOptions"
                  :key="item"
                  :label="item"
                  :value="item"
                >
                </el-option>
              </el-select>

              <base-input>
                <el-input
                  type="search"
                  class="mb-3 search-input"
                  clearable
                  prefix-icon="el-icon-search"
                  placeholder="Search records"
                  v-model="searchWord"
                  aria-controls="datatables"
                >
                </el-input>
              </base-input>
            </div>
            <el-table 
              header-cell-class-name="table-transparent"
              :data="tableData">
              <el-table-column>
                <div v-show="row.image" class="photo" slot-scope="{ row }">
                  <img :src="row.image" alt="Table image" />
                </div>
              </el-table-column>
              <el-table-column
                v-for="column in tableColumns"
                sortable
                :key="column.label"
                :min-width="column.minWidth"
                :prop="column.prop"
                :label="column.label"
              >
              </el-table-column>
              <el-table-column :min-width="135" align="right" label="Actions">
                <div slot-scope="props">
                  <base-button
                    @click.native="handleEdit(props.$index, props.row)"
                    class="edit btn-link"
                    type="warning"
                    size="sm"
                    icon
                  >
                    <i class="tim-icons icon-pencil"></i>
                  </base-button>
                  <base-button
                    @click.native="handleDelete(props.$index, props.row)"
                    class="remove btn-link"
                    type="danger"
                    size="sm"
                    icon
                  >
                    <i class="tim-icons icon-simple-remove"></i>
                  </base-button>
                </div>
              </el-table-column>
            </el-table>
          </div>
          <div
            slot="footer"
            class="col-12 d-flex justify-content-center justify-content-sm-between flex-wrap"
          >
            <div class="">
              <p class="card-category">
                Showing {{ from + 1 }} to {{ to }} of {{ pagination.total }} entries
              </p>
            </div>
            <base-pagination
              class="pagination-no-border"
              v-model="pagination.currentPage"
              :per-page="pagination.perPage"
              :total="pagination.total"
            >
            </base-pagination>
          </div>
        </card>
      <div class="col-md-12 d-flex justify-content-between">
        <div>

          <base-button v-show="mode===null"
          type="primary"
          @click="cronjob('current')"
          >CronJOB-current</base-button
        >
        
        <base-button v-show="mode===null"
          type="primary"
          @click="cronjob('history')"
          >CronJOB-history</base-button
        >        
        <base-button v-show="mode===null"
          type="primary"
          @click="cronjob('updateSpots')"
          >CronJOB-updateSpots</base-button
        >
        </div>
        <base-button v-show="mode===null"
          type="primary"
          :disabled="selects.type===undefined"
          @click="mode='post'"
          >{{$t('admin.add')}}</base-button
        >
      </div>
      <submit-card-vue ref="postForm" v-show="mode==='post'" :inForm="generalForm" @onSubmit="postSubmit">
        <div slot="header" class="d-flex justify-content-between">
          <div class="p-3"><h2 class="card-category">{{this.selects.type}}</h2>
          <h3 class="card-title">{{$t('admin.add')}}</h3></div>
          <base-button
            @click="mode=null"
              class="remove btn-link"
              type="danger"
              size="md"
              icon
            ><i class="tim-icons icon-simple-remove"></i>
          </base-button>
        </div>
        <div slot="additional">
          <base-button
            class=""
            @click.stop="modalShow = true"
            type="primary"
            >{{$t('admin.byfile')}}</base-button
          >
        </div>
      </submit-card-vue>
      <submit-card-vue ref="putForm" v-show="mode==='put'" :inForm="editForm" @onSubmit="putSubmit" :editField="editField">
        <div slot="header" class="d-flex justify-content-between">
          <div class="p-3"><h2 class="card-category">{{this.selects.type}}</h2>
          <h3 class="card-title">{{$t('admin.edit')}}</h3></div>
          <base-button
            @click="mode=null"
              class="remove btn-link"
              type="danger"
              size="md"
              icon
            ><i class="tim-icons icon-simple-remove"></i>
          </base-button>
        </div>
        <div slot="additional">
        </div>
      </submit-card-vue>
      
      </div>


    </div>
      <modal
    :show.sync="modalShow"
    headerClasses="justify-content-center"
  >
    <h4 slot="header" class="title title-up">파일로 업로드하기</h4>
      <VueFileAgent
    ref="vueFileAgent"
    :theme="'list'"
    :multiple="false"
    :deletable="true"
    :meta="true"
    :accept="'.csv'"
    :maxSize="'1MB'"
    :helpText="'Choose csv file'"
    enctype="multipart/form-data"
    :errorText="{
      type: 'Invalid file type. Only csv file Allowed',
      size: 'Files should not exceed 1MB in size',
    }"
    @select="filesSelected($event)"
    @beforedelete="onBeforeDelete($event)"
    @delete="fileDeleted($event)"
    v-model="fileRecords"
  ></VueFileAgent>
  <div class="row m-3">
    <p>다음의 정보가 있는지 확인하세요.</p>
  </div>
    <p v-for="(item) in generalForm" :key="item.label">
    {{'- ' + item.label}} {{item.required ? "*" : ""}}
    </p>

    <div class="row d-flex justify-content-between m-3">
            <base-button
        type="danger"
        @click.native="modalShow = false"
        >Close
      </base-button>
      <base-button :disabled="!fileRecordsForUpload.length" @click="uploadFiles()">Upload</base-button>
    </div>
  </modal>
  </div>

</template>

<script>
import { TimeSelect, DatePicker, Select, Option,Table, TableColumn  } from 'element-ui';
import { BaseAlert,BasePagination, Modal } from 'src/components';
import { BaseCheckbox, BaseRadio } from 'src/components/index';
import SubmitCardVue from 'src/components/forms/SubmitCard.vue';
import _ from 'lodash'
import { mapState } from 'vuex';

import swal from 'sweetalert2';


export default {
  components: {
    [DatePicker.name]: DatePicker,
    [TimeSelect.name]: TimeSelect,
    [Select.name]: Select,
    [Option.name]: Option,
    [Table.name]: Table,
    [TableColumn.name]: TableColumn,
    SubmitCardVue,
    BaseAlert,
    BasePagination,
    BaseCheckbox,
    BaseRadio,
    Modal,
  },
  data() {
    return {
      selects: {
        type: undefined,
        types: [],
      },
      pagination: {
        perPage: 5,
        currentPage: 1,
        perPageOptions: [5, 10, 25, 50],
        total: 0
      },
      tableData: [],
      tableColumns : [],
      totalTableColumns: [
        {
          prop: 'district_spot',
          label: this.$t('table.district_spot'),
          minWidth: 150
        },
        {
          prop: 'id',
          label: this.$t('table.id'),
          minWidth: 100
        },
        {
          prop: 'is_active',
          label: this.$t('table.is_active'),
          minWidth: 100
        },
        {
          prop: 'opened',
          label: this.$t('table.opened'),
          minWidth: 100
        },
        {
          prop: 'idnumber',
          label: this.$t('table.idnumber'),
          minWidth: 150
        },
        {
          prop: 'name',
          label: this.$t('table.name'),
          minWidth: 150
        },
        {
          prop: 'spot_name',
          label: this.$t('table.name'),
          minWidth: 150
        },
        {
          prop: 'review_count',
          label: this.$t('table.review_count'),
          minWidth: 150
        },
        {
          prop: 'district',
          label: this.$t('table.district'),
          minWidth: 100
        },
        {
          prop: 'bike_number',
          label: this.$t('table.bike_number'),
          minWidth: 150
        },
        {
          prop: 'capacity',
          label: this.$t('table.capacity'),
          minWidth: 100
        },
        {
          prop: 'latitude',
          label: this.$t('table.latitude'),
          minWidth: 120
        },
        {
          prop: 'longitude',
          label: this.$t('table.longitude'),
          minWidth: 120
        },
        {
          prop: 'address',
          label: this.$t('table.address'),
          minWidth: 250
        },
        {
          prop: 'username',
          label: this.$t('table.username'),
          minWidth: 200
        },
        {
          prop: 'first_name',
          label: this.$t('table.first_name'),
          minWidth: 150
        },
        {
          prop: 'last_name',
          label: this.$t('table.last_name'),
          minWidth: 150
        },
        {
          prop: 'email',
          label: this.$t('table.email'),
          minWidth: 200
        },
        {
          prop: 'date_joined',
          label: this.$t('table.date_joined'),
          minWidth: 200
        },
        {
          prop: 'user_spots',
          label: this.$t('table.user_spots'),
          minWidth: 200
        },
        {
          prop: 'target_spot',
          label: this.$t('table.target_spot'),
          minWidth: 120
        },
        {
          prop: 'create_date',
          label: this.$t('table.create_date'),
          minWidth: 200
        },
        {
          prop: 'predict_date',
          label: this.$t('table.predict_date'),
          minWidth: 200
        },
        {
          prop: 'predict_number',
          label: this.$t('table.predict_number'),
          minWidth: 100
        },
        {
          prop: 'observed_number',
          label: this.$t('table.observed_number'),
          minWidth: 100
        },
        {
          prop: 'user',
          label: this.$t('table.user'),
          minWidth: 200
        },
        {
          prop: 'open_date',
          label: this.$t('table.open_date'),
          minWidth: 150
        },
        {
          prop: 'content',
          label: this.$t('table.content'),
          minWidth: 250
        },

      ],
      generalForm : {},
      editForm : {},
      totalgeneralForm : {
        id : {name: 'id', label : this.$t('table.id'), required : false, input : true, disabled : true},
        username : {name : 'username', label : this.$t('table.username'), rules : "required|korAlphaNum|min:5|max:20", required : true, input : true},
        password : {name : 'password', label : this.$t('table.password'), rules : "required|min:7|max:20", required : true, input : true, type : 'password'},
        target_spot : {name : 'target_spot', label : this.$t('table.target_spot'),rules : "required|numeric", required : true, input : true},
        last_name : {name : 'last_name', label : this.$t('table.last_name'),rules : "required|min:1|max:20|korAlpha", required : true, input : true},
        first_name : {name : 'first_name', label : this.$t('table.first_name'),rules : "required|min:1|max:50|korAlpha", required : true, input : true},
        user_spots : {name : 'user_spots', label : this.$t('table.user_spots'),rules : "spots|max:30", required : false, input : true},
        email : {name : 'email', label : this.$t('table.email'), rules : "email", type : 'email' , required : false, input : true},
        user : {name : 'user', label : this.$t('table.user'), rules : "required|korAlphaNum", required : false, input : true, disabled : true},
        address : {name : 'address', label : this.$t('table.address'), rules : "required|address|max:100" , required : true, input : true},
        longitude : {name : 'longitude', label : this.$t('table.longitude'), rules : "required|number.", required : true, input : true},
        latitude : {name : 'latitude', label : this.$t('table.latitude'), rules : "required|number.", required : true, input : true},
        capacity : {name : 'capacity', label : this.$t('table.capacity'), rules : "numeric", required : false, input : true},
        district : {name : 'district', label : this.$t('table.district'),rules : "required|korAlpha|max:30", required : true, input : true},
        open_date : {name : 'open_date', label : this.$t('table.open_date'), required : false, input : false},
        name : {name : 'name', label : this.$t('table.name'),rules : "required|korAlphaNum|max:50" , required : true, input : true},
        spot_name : {name : 'spot_name', label : this.$t('table.name'),rules : "required|address|max:50" , required : true, input : true},
        district_spot : {name : 'district_spot', label : this.$t('table.district_spot'),rules : "required|korAlphaNum|max:50", required : true, input : true},
        idnumber : {name: 'idnumber', label : this.$t('table.idnumber'), rules : "required|numeric", required : true, input : true},
        predict_date : {name : 'predict_date', label : this.$t('table.predict_date'), required : true, input : false},
        observed_number : {name : 'observed_number', label : this.$t('table.observed_number'), rules : "numeric", required : false, input : true},
        predict_number : {name : 'predict_number', label : this.$t('table.predict_number'), rules : "required|numeric", required : true, input : true},
        content : {name : 'content', label : this.$t('table.content'), rules : "required|min:5", required : true, input : true},
      },
      searchWord: '',
      mode : null,
      modalShow : false, 
      editField : {},
      fileRecords: [],
      fileRecordsForUpload: [],
    }

  },
computed: {
    to() {
      let highBound = this.from + this.pagination.perPage;
      if (this.pagination.total < highBound) {
        highBound = this.pagination.total;
      }
      return highBound;
    },
    from() {
      return this.pagination.perPage * (this.pagination.currentPage - 1);
    },
    ...mapState(['is_superuser']),
  },
  methods : {
    getModels(){
      this.$authHttp.get(`/api/seoulbike/models`).then((res)=>{
        this.selects.types = res.data.map(x => {return {value : x.toLowerCase(), label : x }})
      }).catch((err)=>{
        this.$errorHandler(err)
      })
    },

    getTableData() {
      let url = new URL(`http://localhost:8000/api/seoulbike/admin/${this.selects.type}`)
      url.searchParams.append('page', this.pagination.currentPage)
      url.searchParams.append('page_size', this.pagination.perPage)
      if(!!this.searchWord){
        url.searchParams.append('search', this.searchWord)
      }
      this.$http.get(url.toString()).then((res)=>{
        let tableData = res.data.results
        if(this.selects.type==='user'){
          tableData = tableData.reduce((acc, obj)=>{
          obj.user_spots = obj.user_spots.join(', ');
          obj.is_active = obj.is_active? 'YES' : "NO";
          acc.push(obj);
          return acc;
          }, [])
          }
        if(this.selects.type==='bikespot'){
          tableData = tableData.reduce((acc, obj)=>{
          obj.opened = obj.opened? 'YES' : "NO";
          acc.push(obj);
          return acc;
          }, [])
          }
        if(this.selects.type==='review'){
          tableData = tableData.reduce((acc, obj)=>{
          obj.user = !!obj.user? obj.user.username : "익명";
          obj.create_date = obj.create_date.slice(0, 19)
          acc.push(obj);
          return acc;
          }, [])
          
        }
        this.tableData = tableData
        this.pagination.total = res.data.count  
      }).catch((err)=>{
        this.$errorHandler(err)
      })
    },

    getFields(model) {
      this.$authHttp.get(`/api/seoulbike/${model}/field`).then((res)=>{
        console.log(res.data)
        this.BuildColumns(res.data)
        this.BuildForms(res.data)
      }).catch((err)=>{
        this.$errorHandler(err)
      })
    },
    BuildColumns(fields){
      this.tableColumns = this.totalTableColumns.reduce((acc, cur)=>{
        if (fields.includes(cur.prop)){ 
          acc.push(cur)
        }
          return acc
        }, [])


    },
    BuildForms(fields){
      this.generalForm = {}
      Object.keys(this.totalgeneralForm).forEach(element => {
        if (fields.includes(element)) {
          this.generalForm[element] = _.cloneDeep(this.totalgeneralForm[element])     
        }
      });
      this.editForm = {}
      Object.keys(this.totalgeneralForm).forEach(element => {
        if (fields.includes(element)) {
          this.editForm[element] = _.cloneDeep(this.totalgeneralForm[element])     
          if(element ==='id' || element ==='idnumber' || element ==='username'){
            this.editForm[element]['disabled'] = true
          }
          if(element ==='password'){
            delete this.editForm[element]
          }
        }
      });
    },

    handleEdit(index, row) {
      let id = row.idnumber ? row.idnumber : row.id
      this.mode = 'put'
      this.editField = _.cloneDeep(row)
      console.log('editField', this.editField)
    },
    handleDelete(index, row) {
      let id = row.idnumber ? row.idnumber : row.id
      swal.fire({
        title: `삭제 실행`,
        text: `${id} 번 데이터를 삭제 하시겠습니까?`,
        icon: 'warning',
        showCancelButton: true,
        customClass: {
          confirmButton: 'btn btn-success btn-fill',
          cancelButton: 'btn btn-danger btn-fill'
        },
        confirmButtonText: '네. 삭제 하겠습니다.',
        cancelButtonText : '취소',
        buttonsStyling: false
      }).then(result => {  
        if(result.value){this.Delete(id);   }
        });
    },
    Delete(value){
      this.$authHttp({
        method : "DELETE",
        url : `/api/seoulbike/admin/${this.selects.type}/${value}`})
      .then((res) =>{
        this.getTableData();
          swal.fire({
            title: '삭제 완료',
            text: `${value} 번 데이터를 삭제 하였습니다.`,
            timer: 2000,
            icon: 'success',
            confirmButtonClass: 'btn btn-success btn-fill',
            buttonsStyling: false
          })
        }
      ).catch((err)=>{
        this.$errorHandler(err)
      })
    },
    postSubmit(data) {
      console.log(data)
      if(data['open_date']!==undefined){
        data['open_date'] = data['open_date'].toISOString().slice(0,10)
      }
      this.$authHttp({
        method : "POST",
        url : `/api/seoulbike/admin/${this.selects.type}/`,
        data : data
      })
      .then((res) => {
        swal.fire({
        title: `성공!`,
        text: '성공적으로 등록되었습니다.',
        timer: 2000,
        buttonsStyling: false,
        customClass: {
          confirmButton: 'btn btn-success btn-fill'
        },
        icon: 'success'
        });
        this.getTableData();

        this.$refs.postForm.formRefresh();
        this.mode = null
      }).catch((err) => {
        this.$errorHandler(err)
      })
    },
    putSubmit(data) {
      let id
      if(data['id']!==undefined){
        id = data['id']
      }
      if(data['idnumber']!==undefined){
        id = data['idnumber']
      }

      console.log(data)
      this.$authHttp({
        method : "PATCH",
        url : `/api/seoulbike/admin/${this.selects.type}/${id}/`,
        data : data
      })
      .then((res) => {
        swal.fire({
        title: `성공!`,
        text: '성공적으로 변경되었습니다.',
        timer: 2000,
        buttonsStyling: false,
        customClass: {
          confirmButton: 'btn btn-success btn-fill'
        },
        icon: 'success'
        });
        this.getTableData();

        this.$refs.postForm.formRefresh();
        this.mode = null
      }).catch((err) => {
        console.log(err)
        this.$errorHandler(err, "id 값이 있는지 확인해 주세요.")
      })
    },
    uploadFiles: function () {
      let formData = new FormData()
      formData.append("files", this.fileRecordsForUpload[0].file )
      formData.append("field",  JSON.stringify(this.generalForm))
      this.$authHttp.post ( `/api/seoulbike/admin/${this.selects.type}/file` , 
              formData ,
              {   
                headers: {"Content-Type": "multipart/form-data" }
        }).then ( response => { 
          console.log(repsonse)
          this.deleteUploadedFile(this.fileRecords[0])
          this.fileRecords = []
            swal.fire({
            title: `성공!`,
            text: `${response.data}개의 데이터가 \n성공적으로 등록되었습니다.`,
            timer: 2000,
            buttonsStyling: false,
            customClass: {
              confirmButton: 'btn btn-success btn-fill'
            },
            icon: 'success'
          });
          this.modalShow = false; 
          this.getTableData();
        }).catch(err => {
          console.log("uploadFiles", err)
          this.$errorHandler(err)
        })
      },
    deleteUploadedFile: function (fileRecord) {
      this.$refs.vueFileAgent.deleteUpload(`http://localhost:8000/api/seoulbike/${this.selects.type}/file`, {   
              headers: {"Content-Type": "multipart/form-data" }
      }, fileRecord);
    },
    filesSelected: function (fileRecordsNewlySelected) {
      var validFileRecords = fileRecordsNewlySelected.filter((fileRecord) => !fileRecord.error);
      this.fileRecordsForUpload = this.fileRecordsForUpload.concat(validFileRecords);
    },
    onBeforeDelete: function (fileRecord) {
      var i = this.fileRecordsForUpload.indexOf(fileRecord);
      if (i !== -1) {
        this.fileRecordsForUpload.splice(i, 1);
      } else {
        if (confirm('Are you sure you want to delete?')) {
          this.$refs.vueFileAgent.deleteFileRecord(fileRecord); // will trigger 'delete' event
        }
      }
    },
    fileDeleted: function (fileRecord) {
      var i = this.fileRecordsForUpload.indexOf(fileRecord);
      if (i !== -1) {
        this.fileRecordsForUpload.splice(i, 1);
      } else {
        this.deleteUploadedFile(fileRecord);
      }
    },
    cronjob(value){
      this.$authHttp.get(`/api/seoulbike/cronjob/${value}`).then(
        res => {
        this.$notify({
        message:
        `cronjob 실행이 완료되었습니다.`,
        timeout: 10000,
        icon: 'tim-icons icon-bell-55',
        horizontalAlign: 'right',
        verticalAlign: 'top',
        type: 'info'
          });
        }
      ).catch((err)=>{
        this.$errorHandler(err, 'cronjob 실행이 실패했습니다.')
      })
    },
  },
  created(){
    if(!this.is_superuser){
      this.$router.push('/')
    }
  },
  mounted(){
    this.$refs.scroll.scrollIntoView();
    this.getModels()
  },

  watch : {
    'selects.type' : function(value) {
      if(this.pagination.currentPage !== 1){
        console.log('watch select type')
        this.pagination.currentPage = 1
      }else{
        this.getTableData()
      }
      this.getFields(value)
    },
    'pagination.perPage' : function(value) {
      if(this.pagination.currentPage !== 1){
        console.log('watch perPage')
        this.pagination.currentPage = 1
      }else{
        this.getTableData()
      }
    },
    'pagination.currentPage' : function(value) {
      this.getTableData()
    },
    searchWord : _.debounce(function(){

      if(this.pagination.currentPage !== 1){
        console.log('watch search word')
        this.pagination.currentPage = 1
      }else{
        this.getTableData()
      }
    }, 500,{
      'leading' : false,
      'trailing' : true
    }),



  }
};
</script>
<style>
.table-transparent {
  background-color: transparent !important;
}
.fade-enter-active {
  transition: opacity .5s;
}
.fade-leave-active{
  transition: opacity .5s, transform .5s;
}

.fade-enter{
  opacity: 0;
}
.fade-leave-to{
  opacity: 0;
 transform: translateY(40px);
}


</style>
