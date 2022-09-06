<template>
  <div>
    <div class="row d-flex justify-content-center">
      <div class="col-md-10">
        <simple-wizard>
          <template slot="header">
            <h3 class="card-title">{{$t('accont.signup')}}</h3>
            <h3 class="description">
              {{$t('accont.signupExplanation')}}
            </h3>
          </template>

          <wizard-tab :before-change="() => validateStep('step1')">
            <template slot="label">
              <i class="tim-icons icon-single-02"></i>
              <p>About</p>
            </template>
            <first-step
              ref="step1"
              @on-validated="onStepValidated"
            ></first-step>
          </wizard-tab>

          <wizard-tab :before-change="() => validateStep('step2')">
            <template slot="label">
              <i class="tim-icons icon-settings-gear-63"></i>
              <p>Account</p>
            </template>
            <second-step
              ref="step2" @on-validated="wizardComplete"
            ></second-step>
          </wizard-tab>

        </simple-wizard>
      </div>
    </div>
  </div>
</template>
<script>
import FirstStep from './Wizard/FirstStep.vue';
import SecondStep from './Wizard/SecondStep.vue';
import swal from 'sweetalert2';
import { SimpleWizard, WizardTab } from 'src/components';
import { mapState } from 'vuex';

export default {
  data() {
    return {
      wizardModel: {}
    };
  },
  components: {
    FirstStep,
    SecondStep,
    SimpleWizard,
    WizardTab,
  },
  methods: {
    validateStep(ref) {
      return this.$refs[ref].validate();
    },
    onStepValidated(validated, model) {
      this.wizardModel = { ...this.wizardModel, ...model };
    },
    wizardComplete(validated, model) {
      this.wizardModel = { ...this.wizardModel, ...model };
      this.submit(this.wizardModel)   
    },
    submit(data){
      console.log(data)
      //data.user_spots = (data.user_spots.split(', ')).map(x=>parseInt(x) )  //field에 맞게 리스트화
      this.$http({
        method : "POST",
        url : `http://localhost:8000/api/seoulbike/user/`,
        data : data,
        headers: {
        'Content-Type': 'multipart/form-data'
        }
      }).then((res)=>{
        swal.fire({
        title: this.$t('accont.welcome'),
        text: this.$t('accont.singupSuccess'),
        showCancelButton: true,
        customClass: {
          confirmButton: 'btn btn-success btn-fill',
          cancelButton: 'btn btn-info btn-fill'
        },
        confirmButtonText: this.$t('accont.confirm'),
        cancelButtonText : this.$t('accont.gotoMain'),
        customClass: {
          confirmButton: 'btn btn-success btn-fill'
        },
        icon: 'success'
        }).then(result => {
          if(result.value){
            this.$router.replace({ path: '/users/login' })
          }else{
            this.$router.replace({ path: '/' })
          }
        }
        );
      }).catch((err)=>{
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
