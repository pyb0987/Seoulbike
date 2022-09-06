<template>

  <ValidationObserver ref="form">
    <form @submit.prevent="validate">
    <div>
      <h4 class="info-text">
        {{$t('accont.secondStep')}}
      </h4>
      <h6 class="info-text">
        *{{$t('accont.emailExplanation')}}
      </h6>
      <div class="justify-content-center mt-5">
        <div class="row flex-column align-items-center">

          <div class="row">
          <image-upload
            type="avatar"
            class="imgupload"
            select-text="추가"
            remove-text='삭제'
            change-text="변경"
            @change="onImageChange"
          />
        </div>
          <div class="col-sm-6 my-1">
          <ValidationProvider
            :name="$t('accont.email')"
            rules="email"
            v-slot="{ passed, failed, errors }"
          >
          <base-input
            v-model="form.email"
            :placeholder="$t('accont.email')"
            addon-left-icon="tim-icons icon-email-85"
            :error="errors[0]"
            :class="[{ 'has-success': passed }, { 'has-danger': failed }]">
          </base-input>
         </ValidationProvider>
         </div>
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
        <div class="col-sm-6 my-1">
       <ValidationProvider
         :name="$t('accont.user_spots')"
         rules=""
         v-slot="{ passed, failed, errors }"
       >
       <base-input
         v-model="form.user_spots"
         @focus="modalFunc"
         :placeholder="$t('accont.user_spots')"
          addon-left-icon="tim-icons icon-map-big"
         :error="errors[0]"
         :class="[{ 'has-success': passed }, { 'has-danger': failed }]">
       </base-input>
        </ValidationProvider>
        </div>

      </div>
      
      </div>
    </div>
  </form>
</ValidationObserver>



</template>
<script>

import { extend } from "vee-validate";
import axios from 'axios';
import {  ImageUpload} from 'src/components/index';
import SpotMap from 'src/components/bike/SpotMap.vue';
import { Modal} from 'src/components';

extend('phone', {
  validate: value => {
    let regex = /^[0-9]{3,4}-[0-9]{3,4}-[0-9]{4}$/.test(value);
    if (!regex) {
      return $t("validation.phone");
    } else {
      return true;
    }
  }
});


export default {
  components: {
    ImageUpload,
    SpotMap,
    Modal,
    
  },
  data() {
    return {
        form : {
          image : '',
          email: '',
          user_spots: ''
        },
        modalShow : false,
        selectedBikespot : [],
        newSelectedBikespot : []
    };
  },
  computed : {
    selectedBikespotString(){
      return this.newSelectedBikespot.map(x=>x+'번').join(', ')
    }
  },
  methods: {
    onImageChange(file) {
      this.form.image = file;
    },
    modalFunc(){
      this.modalShow = true
    }, 
    validate() {
      return this.$refs.form.validate().then(res => {
        if (!res) {
          return;
        }
        this.$emit("on-validated", res, this.form);
        return res;
      });
    },
    bikeSpots(bikeSpots){ 
        this.newSelectedBikespot = bikeSpots
    },
    DeleteSpot(){
      this.modalShow = false
      this.newSelectedBikespot = []
      this.selectedBikespot = []
      this.form.user_spots = ''
    },
    CancelSpot(){
      this.modalShow = false
      this.newSelectedBikespot = this.selectedBikespot.slice()
    },
    Okayspot(){
      this.selectedBikespot = this.newSelectedBikespot.slice()
      this.form.user_spots = this.selectedBikespot.join(', ')
      this.modalShow = false
    }
  },
};
</script>
<style>
.imgupload img{
    height: 100px;
    width: 100px;
}
</style>