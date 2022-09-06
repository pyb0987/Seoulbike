<template>
<div class="mx-auto col-md-10 col-lg-9 col-xl-5 d-flex flex-column align-items-center">
  <div ref="scroll"></div>
  <card>
    <h5 slot="header" class="title">{{$t('accont.newPasswordSet')}}</h5>
        <ValidationObserver ref="passwordForm">
            <form @submit.prevent="passwordFormValidation">
            <ValidationProvider
            :name="$t('accont.new_password')"
            rules="required|min:7|max:20|confirmed:confirmation"
            v-slot="{ passed, failed, errors }"
            >
            <base-input
            type="password"
            required
            :label="$t('accont.new_password')"
            v-model="passwordForm.password"
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
            v-model="passwordForm.confirmation"
            :error="errors[0]"
            :class="[{ 'has-success': passed }, { 'has-danger': failed }]"
          >
          </base-input>
          </ValidationProvider>
          <div class="col-12 d-flex justify-content-between">
            <div></div>
        <base-button @click="UpdatePasswordForm" type="primary" class="btn-fill">
            <i style="font-size: 1.3rem;" class="tim-icons icon-pencil"></i>&nbsp;{{$t('accont.submit')}}
        </base-button>
          </div>
          </form>
            </ValidationObserver>
  </card>
    </div>
</template>
<script>
import { mapState,mapActions } from 'vuex';
import swal from 'sweetalert2';
import _ from 'lodash';


export default {
    components : {
    },
    data() {
        return {
      passwordForm : {
        password : null,
        confirmation : null,
        token : null
      },
    };
  },
  methods: {
    ...mapActions([
      'update', 'logout'
    ]),

    passwordFormValidation(){
        if(!!this.user_id){
        return this.$refs.passwordForm.validate().then(res => {
            if (res===true){
                this.UpdatePasswordForm()
                }
            })
        }
    },

    UpdatePasswordForm(){
        let form = _.cloneDeep(this.passwordForm)
        this.$normalHttp.post(`/api/auth/password_reset/confirm/`, form).then((res)=>{
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
            this.$router.push("/")
            }else{
                throw this.$t('swal.changePwFailed')
            }
        }).catch((err)=>{
            this.$errorHandler(err)
        })
    },
  },
  computed : {
    ...mapState(['username', 'image', 'user_id']),
  },
    created() {
        this.passwordForm.token = this.$route.query['token']
        if(!this.passwordForm.token){
          swal.fire({
            title: this.$t('swal.error'),
            text: this.$t('swal.badRequest'),
            timer: 2000,
            icon: 'warning',
            confirmButtonClass: 'btn btn-waring btn-fill',
            buttonsStyling: false
          }).finally(()=>{
            this.$router.push("/")
          })
        }

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
.deleteModal .has-success.has-label:after, .has-danger.has-label:after{
    top: 44px;
}

</style>
