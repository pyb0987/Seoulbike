<template>
  <ValidationObserver ref="form">
    <form @submit.prevent="validate">
    <div>
      <h5 class="info-text">
        {{$t('accont.firstStep')}}
      </h5>
      <div class="row justify-content-center flex-column align-items-center">

          <div class="col-sm-6">
          <ValidationProvider
            :name="$t('accont.lastName')"
            rules="required|min:1|max:20|korAlpha"
            v-slot="{ passed, failed, errors }"
          >
          <base-input
            required
            v-model="form.last_name"
            :label="$t('accont.lastName')"
            :error="errors[0]"
            :class="[{ 'has-success': passed }, { 'has-danger': failed }]">
          </base-input>
         </ValidationProvider>
         </div>

         <div class="col-sm-6">
          <ValidationProvider
            :name="$t('accont.firstName')"
            rules="required|min:1|max:50|korAlpha"
            v-slot="{ passed, failed, errors }"
          >
          <base-input
            required
            v-model="form.first_name"
            :label="$t('accont.firstName')"
            :error="errors[0]"
            :class="[{ 'has-success': passed }, { 'has-danger': failed }]">
          </base-input>
         </ValidationProvider>
          </div>
        <div class="col-sm-6">
          <ValidationProvider
          ref="usernameValidation"
          :name="$t('accont.username')"
          rules="required|korAlphaNum|min:5|max:20"
          v-slot="{ passed, failed, errors }"
          >
          <base-input
          required
          v-model="form.username"
          :label="$t('accont.username')"
          :error="errors[0]"
          :class="[{ 'has-success': passed }, { 'has-danger': failed }]">
        </base-input>
        </ValidationProvider>
        </div>
        <div class="col-sm-6">
       <ValidationProvider
         :name="$t('accont.password')"
         rules="required|min:7|max:20|confirmed:confirmation"
         v-slot="{ passed, failed, errors }"
       >
       <base-input
         required
         v-model="form.password"
          type="password"
         :label="$t('accont.password')"
         :error="errors[0]"
         :class="[{ 'has-success': passed }, { 'has-danger': failed }]">
       </base-input>
        </ValidationProvider>
        </div>
        <div class="col-sm-6">
        <ValidationProvider
        :name="$t('accont.confirmation')"
        vid="confirmation"
        rules="required"
        v-slot="{ passed, failed, errors }"
      >
      <base-input
        required
        v-model="form.confirmation"
         type="password"
         :label="$t('accont.confirmation')"
        :error="errors[0]"
        :class="[{ 'has-success': passed }, { 'has-danger': failed }]">
      </base-input>
      </ValidationProvider>
      </div>
      <div class="col-md-6 category form-category text-end">* {{$t('accont.required')}}</div>

      
      </div>
    </div>
  </form>
</ValidationObserver>
</template>
<script>

import { extend } from "vee-validate";
import { required, min, max,confirmed } from "vee-validate/dist/rules";
import _ from "lodash";

extend('korAlpha', {
  validate: function(value){
    let regex = /^[가-힣|aA-zZ]*$/.test(value);
    if (!regex) {
      return $("validation.korAlpha");
    } else {
      return true;
    }
  }
});

extend('korAlphaNum', {
  validate: function(value){
    let regex = /^[가-힣|aA-zZ|0-9]*$/.test(value);
    if (!regex) {
      return $("validation.korAlphaNum");
    } else {
      return true;
    }
  }
});


export default {
  data() {
    return {
      form : {
        first_name: '',
        last_name: '',
        username: '',
        password: '',
        confirmation: ''
      },
    };
  },
  methods: {
    validate() {
      return this.$refs.form.validate().then(res => {
        this.$emit("on-validated", res, this.form);
        return res;
      });
    },
  },

  watch : {
    'form.username' :  _.debounce(function(){
      this.$http.get(`http://localhost:8000/api/seoulbike/user/namecheck/?username=${this.form.username}`).then((res)=>{
        if(res.data.checked!==1){
          this.$refs.usernameValidation.setErrors([this.$t("validation.nameExist")])
        }else{
          this.$refs.usernameValidation.validate()
        }
      }).catch((err)=>{
        this.$refs.usernameValidation.setErrors([this.$t("validation.nameFail")])
      })
    }, 1000)
  }
};
</script>
<style></style>
