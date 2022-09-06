<template>
  <div>
    <div ref="scroll"></div>

    <div class="row mt-5">
      <div class="col-md-10 m-auto">
      <card class="p-3">
        <spot-map id="spotMap" ref="spotMap" @bikeSpotClick="bikeSpotDetail" mode="single" :MapCenterSpot="MapCenterSpot" :userLikeSpots="userLikeSpots"></spot-map>
      </card>
      </div>
      <div class="col-md-10 m-auto">
      <card class="p-2">
        <div class="row">
          <ul class="nav nav-tabs">
            <li class="nav-item">
              <a class="nav-link" @click="spotTab='info'" :class="spotTab==='info' ? 'active' : ''" aria-current="page" href="#">{{$t('spots.info')}}</a>
        </li>
        <li class="nav-item">
          <a class="nav-link" @click="spotTab='search'" :class="spotTab==='search' ? 'active' : ''" href="#">{{$t('spots.search')}}</a>
        </li>
        <li class="nav-item">
          <a class="nav-link" @click="spotTab='review'" :class="spotTab==='review' ? 'active' : ''" href="#">{{$t('spots.comment')}}</a>
        </li>
        <li class="nav-item">
          <a class="nav-link" @click="spotTab='bookmark'" :class="spotTab==='bookmark' ? 'active' : ''" href="#">{{$t('spots.myspot')}}</a>
        </li>
      </ul>
        <base-button
        v-show="spotTab==='info'"
        @click="likeThisSpot"
        class="btn-link d-none d-md-block"
        id="spotlikebutton"
        :type="heartColorAllocator()"
        size="lg"
        icon
      >
        <i style="font-size: 1.8rem;" class="tim-icons icon-heart-2"></i>
      </base-button>
      </div>
        <div class="row" v-show="spotTab==='info'">
            <div class="col-lg-6">
              <div class="card-header">
                <base-button
                v-show="spotTab==='info'"
                @click="likeThisSpot"
                class="btn-link d-sm-block d-md-none"
                id="spotlikebutton"
                :type="heartColorAllocator()"
                size="lg"
                icon
              >
                <i style="font-size: 1.8rem;" class="tim-icons icon-heart-2"></i>
              </base-button>
                <h5 class="card-category">{{this.bikeSpotInfo.idnumber ? this.bikeSpotInfo.idnumber + this.$t('spots.spotnumber') : ''}}</h5>
            <h3 class="card-title">{{this.bikeSpotInfo.spot_name || this.$t('spots.spotNoselected')}}</h3>
            <h4 class="card-description pt-3">{{this.bikeSpotInfo.address || ''}}</h4>
            <h5 class="card-category">{{this.bikeSpotInfo.open_date ? this.bikeSpotInfo.open_date+'~' :''}}</h5>
            </div>
          </div>
          <div class="col-6 col-lg-4 d-flex" style="flex-direction: row-reverse">
            <h1 style="font-size:3rem" class="card-title pt-3">
            <i style="font-size:2rem" class="tim-icons icon-chart-pie-36 text-success "></i> {{this.bikeSpotInfo.bike_number || 0}}/{{this.bikeSpotInfo.capacity || 0}}<span style="font-size:1rem">{{$t('spots.numbers')}}</span>
          </h1>
          </div>
          <div class="col-6 col-lg-2">
            <div class="chart-area">
              <pie-chart ref="CapacityPie"
                  :chart-data="CapacityPie.chartData"
                  :extra-options="CapacityPie.extraOptions"
                  :height="140"
                >
                </pie-chart>
            </div>
            </div>
        </div>
        <div v-show="spotTab==='search'">
        <bike-table @findSpot="findSpot" @likeSpot="likeSpot"></bike-table>
      </div>
      <div v-show="spotTab==='review'" class="p-3">
      <review-table ref="reviewTable" :bikeSpotInfo="bikeSpotInfo"></review-table>
      </div>
      <div v-show="spotTab==='bookmark'">
        <like-bike-table ref="likebiketable" @findSpot="findSpot" :userLikeSpots="userLikeSpots" @likeSpot="likeSpot"></like-bike-table>
      </div>

      </card>
      <analysis-board :target="bikeSpotInfo.idnumber" :bikenum="bikeSpotInfo.bike_number"></analysis-board>
      </div>

    </div>
    


  </div>
</template>
<script>

import PieChart from 'src/components/Charts/PieChart';
import config from '@/config';
import * as chartConfigs from '@/components/Charts/config';
import SpotMap from 'src/components/bike/SpotMap.vue';
import UserReview from 'src/components/bike/UserReview.vue';
import { Table, TableColumn , Select, Option } from 'element-ui';
import { BasePagination } from 'src/components';
import _ from 'lodash'
import BikeTable from '../../components/bikeTable.vue';
import ReviewTable from '../../components/reviewTable.vue';
import LikeBikeTable from '../../components/likeBikeTable.vue';
import {likeAspot, getLikeSpotsList } from 'src/storage/userspots.js'
import AnalysisBoard from '../../components/AnalysisBoard.vue'

export default {
  components: {
    [Select.name]: Select,
    [Option.name]: Option,
    [Table.name]: Table,
    [TableColumn.name]: TableColumn,
    PieChart,
    SpotMap,
    BasePagination,
    UserReview,
    BikeTable,
    ReviewTable,
    LikeBikeTable,
    AnalysisBoard
},

  data() {
    return {
      spotTab : 'info',
      bikeSpotInfo : {},
      MapCenterSpot : null,
      userLikeSpots : null,
      CapacityPie : {
        chartData: {
          labels: ['거치수', '이용중'],
          datasets: [
            {
              pointRadius: 0,
              pointHoverRadius: 2,
              backgroundColor: ['#00c09d', '#e2e2e2'],
              borderWidth: 0,
              data: [0, 1]
            }
          ]
        },
        extraOptions: chartConfigs.pieChartOptions
      },
    };
  },
  computed: {
  },
  methods : {
    bikeSpotDetail(bikespot){ 
      this.bikeSpotInfo = bikespot;
      let newChartData = {
          labels: [this.$t('spots.remain'), this.$t('spots.occupied')],
          datasets: [
            {
              pointRadius: 0,
              pointHoverRadius: 2,
              backgroundColor: ['#00c09d', '#e2e2e2'],
              borderWidth: 0,
              data: [bikespot.bike_number, Math.max(bikespot.capacity-bikespot.bike_number, 0 )]
            }
          ]
        }
      this.CapacityPie.chartData = newChartData;
      this.$refs.CapacityPie.updateGradients(newChartData);
      if(this.spotTab==='review'){
      this.$refs.reviewTable.getReviewData(bikespot.idnumber);
      }
    },
    findSpot(index, row) {
      this.MapCenterSpot = row
    },
    likeSpot(row){      
      likeAspot(row)
      this.userLikeSpots = getLikeSpotsList()
      },
    likeThisSpot(){      
      likeAspot(this.bikeSpotInfo)
      this.userLikeSpots = getLikeSpotsList()
      console.log(this.userLikeSpots)
      },
    heartColorAllocator(){
      if(!!this.userLikeSpots & !!this.bikeSpotInfo.idnumber & this.userLikeSpots.includes(this.bikeSpotInfo.idnumber) ){
        return 'danger'
      }
        return 'primary'
    },
      


  },
    watch : {
      spotTab : function(value){
        if(value==='bookmark'){
          this.$refs.likebiketable.getTableData()
        }else if(value==='review'){
          this.$refs.reviewTable.getReviewData(this.bikeSpotInfo.idnumber)
        }
      },
  },
  created() {
    this.userLikeSpots = getLikeSpotsList()
  },
  mounted() {
    this.$refs.scroll.scrollIntoView();
    this.userLikeSpots = getLikeSpotsList()
  }

};
</script>

<style>
.floatingTextarea{
  height: 180px;
  font-size : 1.0rem;
}
.textareaShell{
  height: 180px;
}
.userImage{
  width: 100px;
  height: 100px;
  overflow: hidden;
  border-radius: 50%;
  margin-bottom: 15px;
}
.passwordButton .passwordInput{
  opacity: 0;
  width: 0%;
  transition: all 0.8s;
}

.passwordButton:hover .passwordInput{
  opacity: 1;
  width: 70%;
}

.passwordButton .passwordInput:focus-within{
  opacity: 1;
  width: 70%;
}
.has-danger{
  white-space: nowrap;
}
#spotlikebutton{
  position: absolute;
  right : 10px;
  top : 10px;
}
</style>