<template>
    <div>
        <div class="row d-flex justify-content-between">
          <h3 class="card-description"><i class="tim-icons icon-square-pin"></i>&nbsp;{{this.bikeSpotInfo.spot_name || this.$t('spots.spotNoselected')}}</h3>
            <h3><i class="tim-icons icon-chat-33 text-primary"></i>&nbsp;{{this.$t('spots.reviewNumber')}} {{this.reviewPagination.total }} {{this.$t('spots.reviewNumberUnit')}}</h3>
        </div>
        <user-review :imgsrc="image" :username="explicit_username">
          <template v-slot:quote>
            <p class="blockquote textareaShell">
              <textarea class="form-control floatingTextarea reviewWrite" :placeholder="$t('spots.reviewPlaceholder')" v-model="reviewForm.content"></textarea>
            </p>
          </template>
          <template v-slot:button>
            <base-button class="btn btn-block" type="primary" round @click="reviewSubmit">
          <i style="font-size: 2rem;" class="tim-icons icon-check-2"></i>
          </base-button>
          <ValidationProvider
            v-if="!isLoggedIn"
            class="mx-auto"
            name="비밀번호"
            rules="reviewPassword"
            v-slot="{ failed, errors }"
          >
          <base-input
            style="width: 70%"
            v-model="reviewForm.password"
            placeholder="****"
            type="password"
            :error="errors[0]"
            :class="[{ 'has-danger': failed }]"
            class="mx-auto">
          </base-input>
         </ValidationProvider>
          </template>
      </user-review>
      <user-review v-for="(item, i) in reviewData" :key="i" :imgsrc="imageUrlFindFromReviewData(item)" :username="usernameFindFromReviewData(item)">
          <template v-slot:quote>
                <p v-if="reviewEditFormRender !== item.id" class="blockquote">{{item.content}}
                    <br />
                    <br />
                    <small> - {{item.create_date.replace('T', ' ').slice(0,16)}}</small><small> - {{item.update_date ? item.update_date.replace('T', ' ').slice(0,16) : ""}}</small>
                    </p>
                <p v-else class="blockquote textareaShell">
                  <textarea class="form-control floatingTextarea reviewWrite" :placeholder="$t('spots.reviewEditPlaceholder')" v-model="item.content"></textarea>
                </p>
          </template>
          <template v-slot:button>
            <div class="passwordButton" v-if="reviewEditFormRender !== item.id">
              <base-button class="btn btn-block" type="primary" round simple v-if="reviewPasswordButton(item)===true" @click="reviewEditButton(item.id)">
              <i class="tim-icons icon-lock-circle icon2rem"></i>
            </base-button>
            <ValidationProvider
            v-if="reviewPasswordButton(item)===true"
            class="passwordInput mx-auto"
            name="비밀번호"
            rules="reviewPassword"
            v-slot="{ failed, errors }"
          >
          <base-input
            v-model="passwordField[item.id]"
            placeholder="****"
            type="password"
            :error="errors[0]"
            :class="[{ 'has-danger': failed }]"
            class="passwordInput mx-auto">
          </base-input>
         </ValidationProvider>
            <base-button class="btn btn-block" type="info" round simple v-if="reviewPasswordButton(item)===false" @click="reviewEditButtonWithID(item)">
              <i class="tim-icons icon-lock-circle icon2rem"></i><p class="text-info textnowrap">&nbsp;{{$t('spots.edit')}}</p>
            </base-button>
            </div>
            <div v-else>
              <base-button class="btn btn-block" type="success" round @click="reviewEditUpdate(item.id, item.content)">
                <i class="tim-icons icon-pencil icon15rem"></i><p class="textnowrap">&nbsp;{{$t('spots.editDone')}}</p>
              </base-button>
              <base-button class="btn btn-block" type="primary" round @click="reviewEditExit">
                <i class="tim-icons icon-refresh-01 icon15rem"></i><p class="textnowrap">&nbsp;{{$t('spots.cancel')}}</p>
              </base-button>
              <base-button class="btn btn-block" type="warning" round @click="reviewEditDelete(item.id)">
                <i class="tim-icons icon-simple-remove icon15rem"></i><p class="textnowrap">&nbsp;{{$t('spots.delete')}}</p>
              </base-button>
            </div>
          </template>
      </user-review>

          <div
        slot="footer"
        class="col-12 d-flex justify-content-center justify-content-sm-between flex-wrap"
        >
        <div class="">
          <p class="card-category">
            {{$t('spots.entrytotal')}} {{ reviewPagination.total }} {{$t('spots.entryshow')}} {{ reviewFrom + 1 }}-{{ reviewTo }}
          </p>
        </div>
        <base-pagination
          class="pagination-no-border"
          v-model="reviewPagination.currentPage"
          :per-page="reviewPagination.perPage"
          :total="reviewPagination.total"
        >
        </base-pagination>
        </div>


    </div>


</template>
<script>
import UserReview from 'src/components/bike/UserReview.vue';
import { BasePagination } from 'src/components';
import swal from 'sweetalert2';
import _ from 'lodash'
import { mapState } from 'vuex';
import { extend } from "vee-validate";

extend('reviewPassword', {
  validate: value => {
    let regex = /^[0-9a-zA-Z]{4}$/.test(value);
    if (!regex) {
      return this.$t("validation.reviewPassword");
    } else {
      return true;
    }
  }
});

export default {
    components: {
    BasePagination,
    UserReview,
    },
    props : ['bikeSpotInfo'],
      data() {
    return {
        reviewForm : {
        content : '',
        password : '',
      },
        passwordField : {},
        reviewPagination: {
        perPage: 10,
        currentPage: 1,
        total: 0
      },
        reviewData : [],
        reviewEditFormRender : null,
    
    }
    },
    computed: {
    reviewTo() {
      let highBound = this.reviewFrom + this.reviewPagination.perPage;
      if (this.reviewPagination.total < highBound) {
        highBound = this.reviewPagination.total;
      }
      return highBound;
    },
    reviewFrom() {
      return this.reviewPagination.perPage * (this.reviewPagination.currentPage - 1);
    },
    ...mapState(['isLoggedIn', 'username', 'image', 'user_id']),
    explicit_username(){
      if(this.isLoggedIn){
        return this.username
      }else{
        return this.$t('spots.anonymous')
      }      
    }
  },
  methods : {
        reviewSubmit(){
      if(!this.bikeSpotInfo.idnumber){
        this.$errorHandler(null, this.$t('error.reviewErrorNoselect'))
        return
      }
      if(this.reviewForm.content.length < 5){
        this.$errorHandler(null, this.$t('error.reviewErrorLetters'))
        return
      }
      if(!this.user_id & this.reviewForm.password.length!==4){
        this.$errorHandler(null, this.$t('error.reviewErrorPassword'))
        return
      }
      let formData = {}
      formData.user = this.user_id
      formData.target_spot = this.bikeSpotInfo.idnumber
      formData.content = this.reviewForm.content
      formData.password = this.reviewForm.password
      this.$normalHttp.post(`/api/seoulbike/review/`,formData).then((res)=>{
        this.reviewForm.content = ''
        this.reviewForm.password = ''
        this.getReviewData(this.bikeSpotInfo.idnumber)
      })
    },
    getReviewData(idnumber){
      if(!idnumber){
        return
      }
      let url = new URL(`http://localhost:8000/api/seoulbike/review`)
      url.searchParams.append('page', this.reviewPagination.currentPage)
      url.searchParams.append('page_size', this.reviewPagination.perPage)
      url.searchParams.append('idnumber', idnumber)
      this.$http.get(url.toString()).then((res)=>{
        this.reviewData = res.data.results;
        console.log(this.reviewData)
        this.reviewPagination.total = res.data.count;
        this.passwordField = {};
        this.reviewEditFormRender = null;
      }).catch((err)=>{
        this.$errorHandler(err);
      })
    },
    imageUrlFindFromReviewData(item){
      if(!!item.user){
        return item.user.image
      }
      return  "http://localhost:8000/media/image/placeholder.jpg" //서버단에서 제공하는법 찾아보기
    },
    usernameFindFromReviewData(item){
      if(!!item.user){
        return item.user.username
      }
      return this.$t('spots.anonymous') //서버단에서 제공하는법 찾아보기
    },
    reviewPasswordButton(item){
      if(!!item.user){
        if(item.user.username===this.username){
          return false
        }
        return null
      }
      return true
    },
    reviewEditButton(id){
      if(this.passwordField[id]===undefined || this.passwordField[id].length!==4){
        this.$errorHandler(null, this.$t('error.reviewErrorPassword'))
        return
      }
      let url = new URL(`http://localhost:8000/api/seoulbike/review/pwcheck`)
      url.searchParams.append('id', id)
      url.searchParams.append('password', this.passwordField[id])
      this.$http.get(url.toString()).then((res)=>{
        if(this.reviewEditFormRender!==null){
          this.$errorHandler(null, this.$t('error.reviewErrorDoubleEdit'))
        }else if(res.data.checked===1){
          this.reviewEditFormRender = id
        }else{
          this.$errorHandler(null, this.$t('error.reviewErrorWrongPassword'))
          this.passwordField[id] = ''
        }
      }).catch((err)=>{
        this.$errorHandler(err, this.$t('error.reviewErrorCheckPassword'))
        this.passwordField[id] = ''
      })
    },
    reviewEditButtonWithID(item){
      if(item.user.username===this.username){

        if(this.reviewEditFormRender!==null){
          this.$errorHandler(null, this.$t('error.reviewErrorDoubleEdit'))
        }else{
          this.reviewEditFormRender = item.id
        }
      }else{
        this.$errorHandler(err, this.$t('error.reviewErrorPermission'))
        this.reviewEditFormRender===null
      }
    },
    reviewEditExit(){
      swal.fire({
            title: this.$t('swal.editCancel'),
            text: this.$t('swal.editCancelConfirm'),
            confirmButtonText: this.$t('swal.editCancel'),
            cancelButtonText: this.$t('swal.editContinue'),
            showCancelButton: true,
          })
          .then((result) => {
            if (result.value) {
              this.getReviewData(this.bikeSpotInfo.idnumber);
            }
          });
    },
    reviewEditDelete(id){
      swal.fire({
            title: this.$t('swal.reviewDelete'),
            text: this.$t('swal.reviewDeleteConfirm'),
            confirmButtonText: this.$t('swal.reviewDeleteYes'),
            cancelButtonText: this.$t('swal.reviewDeleteNo'),
            showCancelButton: true,
          })
          .then((result) => {
            if (result.value) {
              this.reviewDelete(id)
            }
          });
    },
    reviewDelete(id){
      this.$normalHttp.delete(`/api/seoulbike/review/${id}`, {
        data : {
          password : this.passwordField[id],
          username : this.username
        }
      }).then((res)=>{
        this.getReviewData(this.bikeSpotInfo.idnumber)
      }).catch((err)=>{
        this.$errorHandler(err)
      })
    },
    reviewEditUpdate(id, content){
      swal.fire({
        title: this.$t('swal.reviewEditDone'),
        text: this.$t('swal.reviewEditDoneConfirm'),
        confirmButtonText: this.$t('swal.reviewEditYes'),
        cancelButtonText: this.$t('swal.reviewEditNo'),
        showCancelButton: true,
      })
      .then((result) => {
        if (result.value) {
          this.reviewUpdate(id, content)
        }
      });
    },
    reviewUpdate(id, content){
      this.$normalHttp.patch(`/api/seoulbike/review/${id}/`, {
          password : this.passwordField[id],
          username : this.username,
          content : content
          }).then((res)=>{
        this.getReviewData(this.bikeSpotInfo.idnumber)
      }).catch((err)=>{
        this.$errorHandler(err)
      })
    }
  },
  watch : {
    'reviewPagination.currentPage' : function(value) {
      this.getReviewData(this.bikeSpotInfo.idnumber);
    },
    'reviewForm.content' : function(value){
      if(value.length>1000){
        this.reviewForm.content = value.slice(0, 1000)
      }
    }
  }




}


</script>
<style>
.icon2rem{
  font-size: 2rem;
}
.icon15rem{
  font-size: 1.5rem;
}
.textnowrap{
  white-space : nowrap;
  font-size: 0.9rem;
  margin: auto;
}
.reviewWrite{
  height: 100% !important;
  max-height: 100% !important;
}
</style>