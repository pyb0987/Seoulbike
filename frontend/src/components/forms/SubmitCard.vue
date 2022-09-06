<template>
      <transition name="fade">
        
      <card>
          <div slot="header">
            <slot name="header" class="row">
              <h3 class="card-title">{{$t('admin.add')}}</h3>
            </slot>

          </div>
          <div>
          <ValidationObserver v-slot="{ handleSubmit }"> 
      <form @submit.prevent="handleSubmit(submit)">
  

      <div>
        <ValidationProvider v-for="(item, i) in inForm"
          :name="item.name"
          :rules="item.rules"
          :key="i"
          v-slot="{ passed, failed, errors }"
        >
        <base-input v-if="item.input"
          :required="item.required"
          :disabled="!!item.disabled"
          v-model="formField[item.name]"
          :type="item.type"
          :label="item.label"
          :error="errors[0]"
          :class="[{ 'has-success': passed }, { 'has-danger': failed }]">
        </base-input>
        <span class="card-category" v-if="!item.input"> {{item.label + (item.required ? "*" : "")}} </span>
        <base-input v-if="!item.input">
          <el-date-picker
              :type="item.type"
              v-model="formField[item.name]"
            >
          </el-date-picker>
        </base-input>
       </ValidationProvider>


        <div class="category form-category">* Required fields</div>
      </div>
      <div class="d-flex justify-content-center justify-content-sm-between">
        <slot name='additional'></slot>
        <base-button
          native-type="submit"
          type="primary"
          >{{$t('admin.complete')}}</base-button
        >
      </div>
      </form>
      </ValidationObserver>
          </div>
      </card>
        </transition>
</template>

<script>
import { TimeSelect, DatePicker, Select, Option } from 'element-ui';

import { extend } from "vee-validate";

extend('korAlphaNum', {
  validate: function(value){
    let regex = /^[가-힣|aA-zZ|0-9]*$/.test(value);
    if (!regex) {
      return "한글, 영문, 숫자만 입력해 주세요.";
    } else {
      return true;
    }
  }
});

extend('number.', {
  validate: function(value){
    let regex = /^[0-9.]*$/.test(value);
    if (!regex) {
      return "숫자만 입력할 수 있습니다.";
    } else {
      return true;
    }
  }
});

extend('address', {
  validate: function(value){
    let regex = /^[가-힣|aA-zZ|0-9 \-]*$/.test(value);
    if (!regex) {
      return "한글, 영문, 숫자 및 하이픈(-), 공백만 입력할 수 있습니다.";
    } else {
      return true;
    }
  }
});

extend('korAlpha', {
  validate: function(value){
    let regex = /^[가-힣|aA-zZ]*$/.test(value);
    if (!regex) {
      return "한글, 영문만 입력해 주세요.";
    } else {
      return true;
    }
  }
});

extend('spots', {
  validate: function(value){
    let regex = /^[0-9 \,]*$/.test(value);
    if (!regex) {
      return "숫자, 공백, 쉼표만 입력해 주세요.";
    } else {
      return true;
    }
  }
});

export default {
    props : ['inForm', 'editField'],
  components: {
    [DatePicker.name]: DatePicker,
    [TimeSelect.name]: TimeSelect,
    [Select.name]: Select,
    [Option.name]: Option,
  },
  data() {
    return {
        formField : {},
    }
  },
  methods : {
    submit() {
        let data = Object.keys(this.inForm).reduce((form, field)=>{
          form[field] = this.formField[field]
        return form
        } ,{} )
        this.$emit('onSubmit', data);
    },
    formRefresh(){
      Object.keys(this.inForm).map((field)=>{
      this.formField[field] = undefined
      } ,{} )
    },
  },
  watch : {
    editField(value){
      this.formField = value
    }
  }
}

</script>
<style>
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