<template>
<div class="mx-auto col-md-10 col-lg-9 col-xl-5 d-flex flex-column align-items-center">
  <div ref="scroll"></div>
    <card class="card-user">
        <p class="card-text"></p>
    <div class="author">
        <div class="block block-one"></div>
      <div class="block block-two"></div>
      <div class="block block-three"></div>
      <div class="block block-four"></div>
      <a href="javascript:void(0)">
          <img class="avatar" :src="image" alt="userImage" />
        <h5 class="title">{{username}}</h5>
      </a>
        <div class="card-description">
      <h5>{{$t('mypage.welcome')}}</h5>
      <small v-if="sinceDay<2">{{$t('mypage.signupToday')}}</small>
      <small v-else>{{$t('mypage.signupDay')}} {{sinceDay}}{{$t('mypage.signupDay2')}}</small>
    </div>
    </div>
  </card>
  <card>
      <h5 slot="header" class="title">{{$t('mypage.EditProfile')}}</h5>
      <ValidationObserver ref="form"> 

    <form @submit.prevent="formValidation">
      <div class="row">
        <div class="col-7">
            <div>

                <base-input
            type="text"
            :label="$t('accont.username')"
            :disabled="true"
            v-model="form.username"
          >
          </base-input>
        </div>
        <div>
            <ValidationProvider
            :name="$t('accont.password')"
            rules="required|min:7|max:20|confirmed:confirmation"
            v-slot="{ passed, failed, errors }"
            >
            <base-input
            type="password"
            required
            :label="$t('accont.password')"
            v-model="form.password"
            :error="errors[0]"
            :class="[{ 'has-success': passed }, { 'has-danger': failed }]"
          >
          </base-input>
          </ValidationProvider>
        </div>
        <div>
            <ValidationProvider
            :name="$t('accont.confirmation')"
            vid="confirmation"
            rules="required"
            v-slot="{ passed, failed, errors }"
            >
            <base-input
            type="password"
            required
            :label="$t('accont.confirmation')"
            v-model="form.confirmation"
            :error="errors[0]"
            :class="[{ 'has-success': passed }, { 'has-danger': failed }]"
          >
          </base-input>
          </ValidationProvider>
        </div>
        </div>
        <div class="col-5 m-auto">
            <image-upload
              type="avatar"
              class="imgupload"
              select-text="Change photo"
              @change="onImageChange"
            />
        </div>
      </div>

      <div class="row">
        <div class="col-md-6">
            <ValidationProvider
            :name="$t('accont.lastName')"
            rules="required|min:1|max:20|korAlpha"
            v-slot="{ passed, failed, errors }"
            >
            <base-input
            type="text"
            required
            :label="$t('accont.lastName')"
            v-model="form.last_name"
            :error="errors[0]"
            :class="[{ 'has-success': passed }, { 'has-danger': failed }]"
          >
          </base-input>
          </ValidationProvider>
        </div>
        <div class="col-md-6"> 
            <ValidationProvider
            :name="$t('accont.firstName')"
            rules="required|min:1|max:50|korAlpha"
            v-slot="{ passed, failed, errors }"
            >
            <base-input
            type="text"
            required
            :label="$t('accont.firstName')"
            v-model="form.first_name"
            :error="errors[0]"
            :class="[{ 'has-success': passed }, { 'has-danger': failed }]"
          >
          </base-input>
          </ValidationProvider>
        </div>
      </div>
      <div class="row">
          <div class="col-md-12">
            <ValidationProvider
            :name="$t('accont.email')"
            rules="email"
            v-slot="{ passed, failed, errors }"
            >
            <base-input
            type="email"
            :label="$t('accont.email')"
            v-model="form.email"
            :error="errors[0]"
            :class="[{ 'has-success': passed }, { 'has-danger': failed }]"
          >
          </base-input>
          </ValidationProvider>
        </div>
      </div>

      <div class="row">
          <div class="col-md-12">
            <ValidationProvider
            :name="$t('accont.user_spots')"
            rules="spots"
            v-slot="{ passed, failed, errors }"
            >
            <base-input
            type="text"
            :label="$t('accont.user_spots')"
            v-model="form.user_spots"
            @focus="modalFunc"
            :error="errors[0]"
            :class="[{ 'has-success': passed }, { 'has-danger': failed }]"
          >
          </base-input>
          </ValidationProvider>
        </div>
      </div>
      <div class="row col-12 d-flex justify-content-between">
        <base-button @click="PasswordChangeButton(true)" type="primary" class="btn-fill">
        <i style="font-size: 1.3rem;" class="tim-icons icon-cloud-upload-94"></i>&nbsp;{{$t('mypage.changePw')}}
        </base-button>
      <base-button native-type="submit" type="primary" class="btn-fill">
        <i style="font-size: 1.3rem;" class="tim-icons icon-badge"></i>&nbsp;{{$t('mypage.changeInfo')}}
      </base-button>
      </div>
    </form>
    </ValidationObserver>
  </card>
  <div class="row col-12 d-flex justify-content-between">
      <base-button v-show="!passwordPageShow" @click="BackRoute" type="warning" class="btn-fill">
        <i style="font-size: 1.3rem;" class="tim-icons icon-refresh-01"></i>&nbsp;{{$t('mypage.goBack')}}
    </base-button>
    <base-button v-show="!passwordPageShow" @click="DeleteUserButton" type="danger" class="btn-fill">
        <i style="font-size: 1.3rem;" class="tim-icons icon-trash-simple"></i>&nbsp;{{$t('mypage.withdrawal')}}
    </base-button>
  </div>
  <transition name="fade">
  <card v-show="passwordPageShow">
    <h5 slot="header" class="title">{{$t('mypage.changePw')}}</h5>
        <ValidationObserver ref="passwordForm">
            <form @submit.prevent="passwordFormValidation">
            <ValidationProvider
            :name="$t('accont.password')"
            rules="required|min:7|max:20"
            v-slot="{ passed, failed, errors }"
            >
            <base-input
            type="password"
            required
            :label="$t('accont.password')"
            v-model="passwordForm.password"
            :error="errors[0]"
            :class="[{ 'has-success': passed }, { 'has-danger': failed }]"
          >
          </base-input>
          </ValidationProvider>
            <ValidationProvider
            :name="$t('accont.new_password')"
            rules="required|min:7|max:20|confirmed:confirmation"
            v-slot="{ passed, failed, errors }"
            >
            <base-input
            type="password"
            required
            :label="$t('accont.new_password')"
            v-model="passwordForm.new_password"
            :error="errors[0]"
            :class="[{ 'has-success': passed }, { 'has-danger': failed }]"
          >
          </base-input>
          </ValidationProvider>
            <ValidationProvider
            :name="$t('accont.new_confirmation')"
            vid="confirmation"
            rules="required"
            v-slot="{ passed, failed, errors }"
            >
            <base-input
            type="password"
            required
            :label="$t('accont.new_confirmation')"
            v-model="passwordForm.new_confirmation"
            :error="errors[0]"
            :class="[{ 'has-success': passed }, { 'has-danger': failed }]"
          >
          </base-input>
          </ValidationProvider>
          <div class="col-12 d-flex justify-content-between">
            <base-button @click="PasswordChangeButton(false)" type="primary" class="btn-fill">
            <i style="font-size: 1.3rem;" class="tim-icons icon-minimal-up"></i>&nbsp;{{$t('mypage.cancel')}}
        </base-button>
        <base-button native-type="submit" type="primary" class="btn-fill">
            <i style="font-size: 1.3rem;" class="tim-icons icon-pencil"></i>&nbsp;{{$t('mypage.changePw')}}
        </base-button>
          </div>
          </form>
            </ValidationObserver>
  </card>
  </transition>
      <modal
    :show.sync="modalShow"
    headerClasses="justify-content-center"
    :showClose="false"
  >
  <div slot="header">
    <h4 class="title title-up">{{$t('accont.bikespotselect')}}</h4>
  </div>
  <p class="description">{{$t('accont.bikespotselectExplanation')}}</p>
    <spot-map v-if="modalShow" @bikeSpots="bikeSpots" mode="multiple" :selectedBikespot="newSelectedBikespot"></spot-map>
    <p class="description p-3 pt-3"><strong>{{this.selectedBikespotString}}</strong></p>
    <template slot="footer">
      <div>
        <base-button class="my-3" type="danger" @click="DeleteSpot" >{{$t('accont.deleteAll')}}</base-button>
        <base-button class="my-3 mx-3" type="danger" @click="CancelSpot" >{{$t('accont.cancel')}}</base-button>
      </div>
      <base-button class="m-3"

        @click="Okayspot"
        >{{$t('accont.confirm')}}
      </base-button>
    </template>
  </modal>
    <modal
        :show.sync="deleteModalShow"
        :centered="true"
        class="deleteModal"
      >
        <ValidationObserver ref="deleteForm">
        <form @submit.prevent="deleteFormValidation">
          <ValidationProvider
            :name="$t('accont.password')"
            rules="required|min:7|max:20|confirmed:confirmation"
            v-slot="{ passed, failed, errors }"
            >
            <base-input
            type="password"
            required
            :label="$t('accont.password')"
            v-model="deleteForm.password"
            :error="errors[0]"
            :class="[{ 'has-success': passed }, { 'has-danger': failed }]"
          >
          </base-input>
          </ValidationProvider>
            <ValidationProvider
            :name="$t('accont.confirmation')"
            vid="confirmation"
            rules="required"
            v-slot="{ passed, failed, errors }"
            >
            <base-input
            type="password"
            required
            :label="$t('accont.confirmation')"
            v-model="deleteForm.confirmation"
            :error="errors[0]"
            :class="[{ 'has-success': passed }, { 'has-danger': failed }]"
          >
          </base-input>
          </ValidationProvider>
          <div class="col-12 py-4 d-flex justify-content-between">
              <base-button @click="deleteModalShow=false" type="success" class="btn-fill">
            <i style="font-size: 1.3rem;" class="tim-icons icon-satisfied"></i>&nbsp;{{$t('mypage.changeMind')}}
        </base-button>
        <base-button native-type="submit" type="danger" class="btn-fill">
            <i style="font-size: 1.3rem;" class="tim-icons icon-user-run"></i>&nbsp;{{$t('mypage.delete')}}
        </base-button>
          </div>
          </form>
          </ValidationObserver>
      </modal>
    </div>
</template>
<script>
import { mapState,mapActions } from 'vuex';
import { extend } from "vee-validate";
import { Modal} from 'src/components';
import SpotMap from 'src/components/bike/SpotMap.vue';
import swal from 'sweetalert2';
import _ from 'lodash';

import {
  ImageUpload
} from 'src/components/index';


extend('korAlphaNum', {
  validate: function(value){
    let regex = /^[가-힣|aA-zZ|0-9]*$/.test(value);
    if (!regex) {
      return this.$t("validation.korAlphaNum");
    } else {
      return true;
    }
  }
});

extend('korAlpha', {
  validate: function(value){
    let regex = /^[가-힣|aA-zZ]*$/.test(value);
    if (!regex) {
      return this.$t("validation.korAlpha");
    } else {
      return true;
    }
  }
});

extend('spots', {
  validate: function(value){
    let regex = /^[0-9 \,]*$/.test(value);
    if (!regex) {
      return this.$t("validation.spots");
    } else {
      return true;
    }
  }
});

export default {
    components : {
        ImageUpload,
        Modal,
        SpotMap
    },
    data() {
        return {
        form: {
        username: null,
        email: null,
        password : null,
        confirmation : null,
        first_name: null,
        last_name: null,
        user_spots: null,
        image : null,
      },
      passwordForm : {
        password : null,
        new_password : null,
        new_confirmation : null,
      },
      deleteForm : {
        password : null,
        confirmation : null,
      },
        date_joined : null,
        selectedBikespot : [],
        newSelectedBikespot : [],
        modalShow : false,
        ImageChange : false,
        passwordPageShow : false,
        deleteModalShow : false,
    };
  },
  methods: {
    ...mapActions([
      'update', 'logout'
    ]),
    formValidation() {
        if(!!this.user_id){
            return this.$refs.form.validate().then(res => {
                if (res===true){
                    this.UpdateForm()
                }
            })
        }
    },
    passwordFormValidation(){
        if(!!this.user_id){
        return this.$refs.passwordForm.validate().then(res => {
            if (res===true){
                this.UpdatePasswordForm()
                }
            })
        }
    },
    deleteFormValidation(){
        if(!!this.user_id){
        return this.$refs.deleteForm.validate().then(res => {
            if (res===true){
                this.UserDeleteForm()
                }
            })
        }
    },
    UpdateForm(){
        console.log(this.form);
        let form = _.cloneDeep(this.form)
        let headers
        if(!this.ImageChange){
            delete form.image
            headers = {'Content-Type' : 'application/json'}
        }else{
            headers = {'Content-Type': 'multipart/form-data' }
        }
        this.$authHttp.patch(`/api/seoulbike/user/${this.user_id}/`, form, {
            headers : headers
        }).then((res)=>{
            let data = res.data
            data.user_id = res.data.id
            this.update({ data : data })
            swal.fire({
            title: this.$t('')`성공!`,
            text: `유저 정보가 성공적으로 변경되었습니다.`,
            timer: 3000,
            buttonsStyling: false,
            customClass: {
              confirmButton: 'btn btn-success btn-fill'
            },
            icon: 'success'
            }).then(()=>{
              this.$router.push('/')
            })
        }).catch((err)=>{
            this.$errorHandler(err)
        })
        
    },
    UpdatePasswordForm(){
        let form = _.cloneDeep(this.passwordForm)
        this.$authHttp.put(`/api/seoulbike/user/${this.user_id}/change_pw/`, form).then((res)=>{
            if(res.data.data=1){
                swal.fire({
                    title: this.$t('swal.success'),
            text: this.$t('swal.changePwSuccess'),
            timer: 3000,
            buttonsStyling: false,
            customClass: {
                confirmButton: 'btn btn-success btn-fill'
            },
            icon: 'success'
            });
            this.passwordForm.password = ''
            this.passwordForm.new_password = ''
            this.passwordForm.new_confirmation = ''
            this.passwordPageShow = false
            }else{
                throw this.$t('swal.changePwFailed')
            }
        }).catch((err)=>{
            this.$errorHandler(err)
        })
    },
    UserDeleteForm(){
        let form = _.cloneDeep(this.deleteForm)
        this.$authHttp.delete(`/api/seoulbike/user/${this.user_id}/`, {
            data : form
        }).then((res)=>{
            swal.fire({
            title: this.$t('swal.deleted'),
            text: this.$t('swal.deletedSuccessfully'),
            timer: 3000,
            buttonsStyling: false,
            customClass: {
                confirmButton: 'btn btn-login btn-fill'
            }
            }).then(()=>{
                this.logout({user_id:undefined})
            }).finally(()=>{
                this.$router.push('/')
            })
        }).catch((err)=>{
                console.log(err)
        })
    },
    onImageChange(file) {
      this.form.image = file;
      this.ImageChange = true;
    },
    bikeSpots(bikeSpots){ 
        this.newSelectedBikespot = bikeSpots
    },
    DeleteSpot(){
     this.newSelectedBikespot = []
      this.selectedBikespot = []
      this.form.user_spots =''
      this.modalShow = false
    },
    CancelSpot(){
      this.modalShow = false
      this.newSelectedBikespot = this.selectedBikespot.slice()
    },
    Okayspot(){
      this.selectedBikespot = this.newSelectedBikespot.slice()
      this.form.user_spots = this.selectedBikespot.join(', ')
      this.modalShow = false
    },
    modalFunc(){
        this.modalShow = true
    },
    BackRoute(){
        swal.fire({
        title: this.$t('swal.goBack'),
        text: this.$t('swal.goBackConfirm'),
        showCancelButton: true,
        customClass: {
          confirmButton: 'btn btn-info btn-fill',
          cancelButton: 'btn btn-danger btn-fill'
        },
        confirmButtonText: this.$t('swal.goBack'),
        cancelButtonText : this.$t('swal.cancel'),
        buttonsStyling: false
      }).then(result => {  
        if(result.value){this.$router.back();   }
        });
    },
    PasswordChangeButton(value){
        this.passwordPageShow = value
    },
    DeleteUserButton(){
        if(!!this.user_id){
            swal.fire({
                title: this.$t('swal.withdrawal'),
        text: this.$t('swal.withdrawalConfirm'),
        icon: 'warning',
        showCancelButton: true,
        customClass: {
            confirmButton: 'btn btn-success btn-fill',
          cancelButton: 'btn btn-danger btn-fill'
        },
        confirmButtonText: this.$t('swal.yes'),
        cancelButtonText : this.$t('swal.noIwillGoBack'),
        buttonsStyling: false
      }).then(result => {  
          if(result.value){
              this.deleteModalShow = true  
         }
        });
        }
    },

  },
  computed : {
    ...mapState(['username', 'image', 'user_id']),
    selectedBikespotString(){
      return this.newSelectedBikespot.map(x=>x+'번').join(', ')
    },
    sinceDay(){
        return Math.ceil((Date.now()-Date.parse(this.date_joined))/1000/60/60/24)
    }
  },
  mounted() {
    this.$refs.scroll.scrollIntoView();
    this.$authHttp.get(`/api/seoulbike/user/${this.user_id}/`).then((res)=>{
        this.form.username = res.data.username
        this.form.first_name = res.data.first_name
        this.form.last_name = res.data.last_name
        this.form.image = res.data.image
        this.form.id = res.data.id
        this.form.email = res.data.email
        this.form.user_spots = res.data.user_spots.join(', ')
        this.date_joined = res.data.date_joined
        this.selectedBikespot = res.data.user_spots
        this.newSelectedBikespot = res.data.user_spots
        this.$el.querySelector('.imgupload img')['src'] = res.data.image

    }).catch((res)=>{

        //밖으로 내보내기
    })
  }

};
</script>


<style>
.imgupload img{
    height: 100px;
    width: 100px;
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
.deleteModal .has-success .form-control{
    color : black !important;
}
.deleteModal .has-success.has-label:after,.deleteModal .has-danger.has-label:after{
    top: 44px;
}

</style>
