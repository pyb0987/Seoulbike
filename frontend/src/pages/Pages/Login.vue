<template>
  <div class="container">
    <div class="col-lg-4 col-md-6 ml-auto mr-auto">
      <ValidationObserver v-slot="{ handleSubmit }">
        <form @submit.prevent="handleSubmit(submit)">
          <card class="card-login card-white">
            <template slot="header">
              <img src="img/card-primary.png" alt="" />
              <h1 class="card-title">{{$t('accont.login')}}</h1>
            </template>

            <div>
              <ValidationProvider
                :name="$t('accont.id')"
                rules="required|min:7|max:20|korAlphaNum"
                v-slot="{ passed, failed, errors }"
              >
              <base-input
                required
                v-model="username"
                type="id"
                :placeholder="$t('accont.username')"
                addon-left-icon="tim-icons icon-email-85"
                :error="errors[0]"
                :class="[{ 'has-success': passed }, { 'has-danger': failed }]">
              </base-input>
             </ValidationProvider>

             <ValidationProvider
               :name="$t('accont.password')"
               rules="required|min:5|max:20"
               v-slot="{ passed, failed, errors }"
             >
             <base-input
               required
               v-model="password"
               :placeholder="$t('accont.password')"
               addon-left-icon="tim-icons icon-lock-circle"
               type="password"
               :error="errors[0]"
               :class="[{ 'has-success': passed }, { 'has-danger': failed }]">
             </base-input>
            </ValidationProvider>
            </div>

            <div slot="footer">
              <base-button native-type="submit" type="primary" class="mb-3" size="lg" block>
                {{$t('accont.doLogin')}}
              </base-button>
              <div class="pull-left">
                <h6>
                  <router-link class="link footer-link" to="/users/signup">
                    {{$t('accont.signup')}}
                  </router-link>
                </h6>
              </div>

              <div class="pull-right">
                <h6><a style="cursor : pointer" @click="emailForm=!emailForm" class="link footer-link">{{ emailForm ? $t('accont.findpwCancel') : $t('accont.findpw')}}</a></h6>
              </div>
            </div>
          </card>
        </form>
      </ValidationObserver>


    </div>
    <transition name="emailfade">
    <div v-show="emailForm" class="col-lg-5 col-md-8 ml-auto mr-auto">
    <ValidationObserver v-slot="{ handleSubmit }">
    <form @submit.prevent="handleSubmit(emailSubmit)">
      <card>
        <h5 slot="header" class="title">{{$t('accont.inputEmail')}}</h5>
    <p class="card-description">{{$t('accont.inputEmailExplanation')}}</p>
      <ValidationProvider
            :name="$t('accont.email')"
            rules="email"
            v-slot="{ passed, failed, errors }"
          >
          <base-input
            v-model="forgotemail"
            :placeholder="$t('accont.email')"
            addon-left-icon="tim-icons icon-email-85"
            :error="errors[0]"
            :class="[{ 'has-success': passed }, { 'has-danger': failed }]">
          </base-input>
         </ValidationProvider>
          <base-button native-type="submit" type="primary" class="btn-fill btn-block">
            <i style="font-size: 1.3rem;" class="tim-icons icon-pencil"></i>&nbsp;{{$t('accont.submit')}}
        </base-button>
        </card>
        </form>
        </ValidationObserver>
      </div>
      </transition>
  </div>
</template>

<script>




import { extend } from "vee-validate";
import { required, min, max } from "vee-validate/dist/rules";
import { mapActions, mapState } from 'vuex';
import swal from 'sweetalert2';
import {LoginSpotGet} from 'src/storage/userspots'

extend('korAlphaNum', {
  validate: value => {
    let regex = /^[가-힣|aA-zZ|0-9]*$/.test(value);
    if (!regex) {
      return this.$t('validation.korAlphaNum');
    } else {
      return true;
    }
  }
});

export default {
  data() {
    return {
      username: "",
      password: "",
      subscribe: true,
      nextPath: '/',
      emailForm : false,
      forgotemail: '',
    };
  },
  mounted() {
    if ('next' in this.$route.query) {
      this.nextPath = this.$route.query.next;
    }
  },
  methods: {
    ...mapActions([
      'login',
    ]),
    submit() {
      this.login({ username: this.username, password: this.password })
        .then((res) => {
          LoginSpotGet(res);
          this.$router.push(this.nextPath);
        }).catch(err =>{
          console.log(err)
          if (err.response.status === 401){
            swal.fire({
            title: '정보 없음',
            text: `아이디 또는 비밀번호가 일치하지 않습니다.`,
            timer: 2000,
            icon: 'warning',
            confirmButtonClass: 'btn btn-warning btn-fill',
            buttonsStyling: false
            })
          }else{
            this.$errorHandler(err)
          }
        }
        );
    },

    emailSubmit(){
      this.$http.post('http://localhost:8000/api/auth/password_reset/', {
        'email' : this.forgotemail
      }).then(res=>{
        console.log(res)
        swal.fire({
            title: '전송 완료',
            text: `${this.forgotemail}로 이메일을 전송했습니다.`,
            timer: 5000,
            icon: 'success',
            confirmButtonClass: 'btn btn-success btn-fill',
            buttonsStyling: false
          })
      }).catch(err=>{
        this.$errorHandler(err)
      })
      

    }

  },
  computed : {
    ...mapState(['isLoggedIn']),
  },
  created(){
    if(!!this.isLoggedIn){
      this.$router.push('/')
    }
  },

};
</script>
<style>
.navbar-nav .nav-item p {
  line-height: inherit;
  margin-left: 5px;
}
.emailfade-enter-active {
  transition: opacity .5s, transform 0.5s;
  
}
.emailfade-leave-active{
  transition: opacity .5s, transform .5s;
}

.emailfade-enter{
  opacity: 0;
  transform: translateY(40px);
}
.emailfade-leave-to{
  opacity: 0;
  transform: translateY(40px);
}
</style>
