<template>
<div>
    <card v-show="futureChart" class="card-chart" no-footer-line>
        <template slot="header">
            <h5 class="card-category">{{$t('spots.analysisFuture')}}</h5>
        <h3 class="card-title">
            <i class="tim-icons icon-chart-bar-32 text-primary"></i>{{$t('spots.remained')}}
        </h3>
        </template>
        <div class="chart-area">
            <line-chart ref="lineChart1"
            :chart-data="lineChart1.chartData"
            :gradient-colors="lineChart1.gradientColors"
            :gradient-stops="lineChart1.gradientStops"
            :extra-options="lineChart1.extraOptions"
            :height="200"
        >
        </line-chart>
        </div>
    </card>
    <card v-show="futureChart" class="card-chart">
        <template slot="header">
            <h5 class="card-category">{{$t('spots.analysisFuture')}}</h5>
    <h3 class="card-title">
        <i class="tim-icons icon-chart-pie-36 text-info"></i>{{$t('spots.volume')}}
    </h3>
    </template>
    <div class="chart-area">
      <line-chart ref="lineChart2"
      :chart-data="lineChart2.chartData"
      :gradient-colors="lineChart2.gradientColors"
      :gradient-stops="lineChart2.gradientStops"
      :extra-options="lineChart2.extraOptions"
      :height="200"
      >
      </line-chart>
    </div>
    </card>
    <card class="card-chart p-3">
      <template slot="header">
      <h3 class="card-title">
      <i class="tim-icons icon-bell-55 text-info"></i> {{$t('spots.information')}}
      </h3>
      </template>
      <base-alert v-for="(item, i) in generalData.futureInfo" :type="item.type" :key="i">
      <i class="tim-icons" :class="item.icon"></i>
          {{item.message}}
      </base-alert>
    </card>
    <card type="chart">
        <template slot="header">
          <div class="row">
            <div class="col-sm-6 text-left">
              <h5 class="card-category">{{$t('spots.analysisPast')}}</h5>
              <h3 class="card-title">
                <i class="tim-icons icon-chart-bar-32 text-primary"></i>{{$t('spots.remained')}}
                </h3>
            </div>
            <div class="col-sm-6 d-flex d-sm-block">
              <div
                class="btn-group btn-group-toggle float-right"
                data-toggle="buttons"
              >
                <label
                  v-for="(item, index) in pastLineChart.weekdays"
                  :key="item"
                  class="btn btn-sm btn-primary btn-simple"
                  :class="{ active: pastLineChart.activeIndex === index }"
                  :id="index"
                >
                  <input
                    type="radio"
                    @click="initPastLineChart(index)"
                    name="options"
                    autocomplete="off"
                    :checked="pastLineChart.activeIndex === index"
                  />
                  <span class="d-none d-sm-block">{{ item }}</span>
                  <span class="d-block d-sm-none">
                  </span>
                </label>
              </div>
            </div>
          </div>
        </template>
        <div class="chart-area">
          <line-chart
            style="height: 100%"
            ref="pastLineChart"
            :chart-data="pastLineChart.chartData"
            :gradient-colors="pastLineChart.gradientColors"
            :gradient-stops="pastLineChart.gradientStops"
            :extra-options="pastLineChart.extraOptions"
          >
          </line-chart>
        </div>
      </card>
    <div class="row">
        <div class="col-md-6 ml-auto">
            <card class="card-chart">
                <template slot="header">
                    <h5 class="card-category">{{$t('spots.analysisPastRanking')}}</h5>
            <h3 class="card-title">
                <i class="tim-icons icon-sound-wave text-danger "></i> {{$t('spots.inflow')}}
            </h3>
          </template>
          <div class="chart-area">
              <bar-chart ref="barChart1"
              :chart-data="barChart1.chartData"
              :extra-options="barChart1.extraOptions"
              :gradient-colors="barChart1.gradientColors"
              :gradient-stops="barChart1.gradientStops"
              :height="200"
            >
            </bar-chart>
          </div>
        </card>
    </div>
      <div class="col-md-6 mr-auto">
                     <card class="card-chart">
                <template slot="header">
                    <h5 class="card-category">{{$t('spots.analysisPastRanking')}}</h5>
            <h3 class="card-title">
                <i class="tim-icons icon-sound-wave text-danger "></i> {{$t('spots.outflow')}}
            </h3>
          </template>
          <div class="chart-area">
              <bar-chart ref="barChart2"
              :chart-data="barChart2.chartData"
              :extra-options="barChart2.extraOptions"
              :gradient-colors="barChart2.gradientColors"
              :gradient-stops="barChart2.gradientStops"
              :height="200"
            >
            </bar-chart>
          </div>
        </card>
      </div>
    </div>
    </div>
</template>

<script>
import LineChart from 'src/components/Charts/LineChart';
import BarChart from 'src/components/Charts/BarChart';
import PieChart from 'src/components/Charts/PieChart';
import config from '@/config';
import * as chartConfigs from '@/components/Charts/config';
import _ from 'lodash'
import { BaseAlert } from 'src/components';

let lineChart1GeneralData = {
    fill: true,
    borderColor: config.colors.primary,
    borderWidth: 2,
    borderDash: [],
    borderDashOffset: 0.0,
    pointBackgroundColor: config.colors.primary,
    pointBorderColor: 'rgba(255,255,255,0)',
    pointHoverBackgroundColor: '#be55ed',
    pointBorderWidth: 20,
    pointHoverRadius: 4,
    pointHoverBorderWidth: 15,
    pointRadius: 2,
  }
let lineChart2GeneralData = {
  fill: true,
  borderColor: config.colors.info,
  borderWidth: 2,
  borderDash: [],
  borderDashOffset: 0.0,
  pointBackgroundColor: config.colors.info,
  pointBorderColor: 'rgba(255,255,255,0)',
  pointHoverBackgroundColor: '#2380f7',
  pointBorderWidth: 20,
  pointHoverRadius: 4,
  pointHoverBorderWidth: 15,
  pointRadius: 2,
  }

let pastLineChartOptions = {
        fill: true,
        borderColor: config.colors.teal,
        borderWidth: 2,
        borderDash: [],
        borderDashOffset: 0.0,
        pointBackgroundColor: config.colors.teal,
        pointBorderColor: 'rgba(255,255,255,0)',
        pointHoverBackgroundColor: config.colors.teal,
        pointBorderWidth: 20,
        pointHoverRadius: 4,
        pointHoverBorderWidth: 15,
        pointRadius: 2,
}
let barChart1GeneralData = {
    fill: true,
    borderColor: config.colors.danger,
    borderWidth: 2,
    borderDash: [],
    borderDashOffset: 0.0,
    }
let barChart2GeneralData = {
    fill: true,
    borderColor: config.colors.orange,
    borderWidth: 2,
    borderDash: [],
    borderDashOffset: 0.0,
    }
export default {
  components: {
    LineChart,
    BarChart,
    PieChart,
    BaseAlert,
    },
    props : ["target", "bikenum"],
    data() {
    return {
      
      futureChart : false,
      generalData : {
        futureIndex : [],  //48개
        futureInflow : [],  //유입량
        futureNumber : [],    //개수
        futureVolume : [],    //이용량
        futureInfo : [],
        pastInflowIndex : [],
        pastOutflowIndex : [],
        pastInflow : [],
        pastOutflow : []
      },
      lineChart1: {
        chartData: {},
        extraOptions: chartConfigs.purpleChartOptions,
        gradientColors: config.colors.primaryGradient,
        gradientStops: [1, 0.4, 0]
      },
      lineChart2: {
        chartData: {},
        extraOptions: chartConfigs.purpleChartOptions,
        gradientColors: config.colors.purpleGradient,
        gradientStops: [1, 0.4, 0]
      },
      pastLineChart: {
        activeIndex: 0,
        chartData: {},
        extraOptions: chartConfigs.purpleDailyChartOptions,
        gradientColors: config.colors.tealGradient,
        gradientStops: [1, 0.4, 0],
        categories: [],
        data : [],   
        weekdays : [],
      },
      barChart1: {
        chartData: {},
        extraOptions: chartConfigs.barChartOptionsGradient,
        gradientColors: config.colors.purpleGradient,
        gradientStops: [1, 0]
      },
      barChart2: {
        chartData: {},
        extraOptions: chartConfigs.barChartOptionsGradient,
        gradientColors: config.colors.primaryGradient,
        gradientStops: [1, 0]
      },
    }
  },
  methods : {
    getData(idnumber){
      this.$normalHttp.get(`/api/seoulbike/bikespot/${idnumber}/analysis/`).then((res)=>{
          this.futureChart = false
          this.buildPastInfo()
          this.smeltPastData(res.data.history)
          if(res.data.result){
              this.futureChart = true
              this.smeltFutureData(res.data)
          }

      }).catch((err)=>{
          this.$errorHandler(err)
      })
    },
    smeltPastData(data){
      let starttime = data.hour.indexOf(0)
      let daystarts = [starttime+24*2, starttime+24*3, starttime+24*4, starttime+24*5, starttime+24*6, starttime+24*7, starttime+24*8]
      this.pastLineChart.data = daystarts.map(x=>{
        return data.have.slice(x, x+24)
      })
      let sortResult = Array.from(data.outflow.keys())
        .sort((a, b) => data.outflow[a] < data.outflow[b] ? -1 : (data.outflow[b] < data.outflow[a]) | 0)
      let topInflows = sortResult.slice(0, 6)
      let topoutflows = sortResult.slice(sortResult.length-6).reverse()

      this.generalData.pastInflowIndex = topInflows.map(x=>{
        let month = Math.floor(data.date[x]/100)%100
        let day = data.date[x]%100
        return month+'/'+day+' '+data.hour[x]+this.$t('spots.hour')
      })
      this.generalData.pastOutflowIndex = topoutflows.map(x=>{
        let month = Math.floor(data.date[x]/100)%100
        let day = data.date[x]%100
        return month+'/'+day+' '+data.hour[x]+this.$t('spots.hour')
      })
      this.pastLineChart.weekdays = daystarts.map(x=>{
        let month = Math.floor(data.date[x]/100)%100
        let day = data.date[x]%100
        return month+'/'+day
      })
      this.generalData.pastInflow = topInflows.map(x=>-data.outflow[x])
      this.generalData.pastOutflow = topoutflows.map(x=>data.outflow[x])
      this.buildPastChart()
    },
    buildPastChart(){
      this.initPastLineChart(0)
      let BarChart1Data = {
        labels: this.generalData.pastInflowIndex,
        datasets: [
          {
              ...barChart1GeneralData,
              label: this.$t('spots.inflow'),
              data: this.generalData.pastInflow
          }
        ]
      }
      this.barChart1.chartData = BarChart1Data;
      this.$refs.barChart1.updateGradients(BarChart1Data);
      let BarChart2Data = {
        labels: this.generalData.pastOutflowIndex,
        datasets: [
          {
              ...barChart2GeneralData,
              label: this.$t('spots.outflow'),
              data: this.generalData.pastOutflow
          }
        ]
      }
      this.barChart2.chartData = BarChart2Data;
      this.$refs.barChart2.updateGradients(BarChart2Data);
    },
    buildPastInfo(){
      this.generalData.futureInfo = []
      this.generalData.futureInfo.push({type : "info", message : this.$t("spots.InfoNotEnoughData"), icon : "icon-bell-55"})
    },
    smeltFutureData(data){
        this.generalData.futureIndex = data.index.map(x=>Date.parse(x))
        this.generalData.futureInflow = _.zip(data.borrow, data.return).reduce((acc, x)=>{
            acc.push(x[1]-x[0])
            return acc
        },[])
        this.generalData.futureNumber = this.generalData.futureInflow.reduce((acc, x, idx)=>{
            acc.push(Math.max(acc[idx]+x, 0))
            return acc
        },[this.bikenum]).slice(1).map(x=>Math.round(x))
        this.generalData.futureVolume = _.zip(data.borrow, data.return).reduce((acc, x)=>{
            acc.push(Math.round(x[1]+x[0]))
            return acc
        },[])
        this.buildFutureChart()
        this.buildFutureInfo(data.info)
    },
    buildFutureChart(){
        let linechart1Data = {
          labels: this.generalData.futureIndex,
          datasets: [
            {
              ...lineChart1GeneralData,
              label: this.$t('spots.remained'),
              data: this.generalData.futureNumber
            }
          ]
        }
        this.lineChart1.chartData = linechart1Data;
        this.$refs.lineChart1.updateGradients(linechart1Data);

        let linechart2Data = {
          labels: this.generalData.futureIndex,
          datasets: [
            {
              ...lineChart2GeneralData,
              label: this.$t('spots.volume'),
              data: this.generalData.futureVolume
            }
          ]
        }
        this.lineChart2.chartData = linechart2Data;
        this.$refs.lineChart2.updateGradients(linechart2Data);
    },
    buildFutureInfo(info){
      console.log(info)
      this.generalData.futureInfo = []
      let holiday = info.holiday.indexOf(1)
      if(holiday === -1){
        this.generalData.futureInfo.push({type : "info", message : this.$t("spots.InfoNoHolidays"), icon : "icon-bell-55"})
      }else{
        let ts = new Date(this.generalData.futureIndex[holiday]).getDay()
        let now = new Date(Date.now()).getDay()
        let jumpday = (ts - now +7 )%7
        if(jumpday == 0){
          this.generalData.futureInfo.push({type : "info", message : this.$t("spots.InfoHolidaysToday"), icon : "icon-bell-55"})
        }else{
          this.generalData.futureInfo.push({type : "info", message : jumpday+this.$t("spots.InfoHolidaysWithin"), icon : "icon-bell-55"})
        }
      }
      let temp = info.snowrain.indexOf(1)
      if (temp===-1){
        this.generalData.futureInfo.push({type : "success", message : this.$t("spots.InfoNoRain"), icon : "icon-check-2"})
      }else{
        let ts = new Date(this.generalData.futureIndex[temp]).toLocaleString("kr-KR", {timeZone: "Asia/Seoul"})
        let tmp = info.temp[temp]
        this.generalData.futureInfo.push({type : "warning", icon : "icon-simple-remove" , message : `${ts} ${tmp>=0 ? '강수' : '적설'}예보. 앞으로 ${temp}시간 안에 ${tmp>=0 ? '비가' : '눈이'} 내립니다.`})
        let fall = info.rainfall.indexOf(Math.max(...info.rainfall))
        ts = new Date(this.generalData.futureIndex[fall]).toLocaleString("kr-KR", {timeZone: "Asia/Seoul"})
        tmp = info.temp[fall]
        this.generalData.futureInfo.push({type : "warning", icon : "icon-simple-remove" , message : `${ts} 에 최대${tmp>=0 ? '강수' : '적설'}량 ${info.rainfall[fall]}mm의 ${tmp>=0 ? '비가' : '눈이'} 내립니다.`})
      }

      temp = info.temp.indexOf(Math.max(...info.temp))
      let ts = new Date(this.generalData.futureIndex[temp]).toLocaleString("kr-KR", {timeZone: "Asia/Seoul"})
      let type = info.temp[temp] > 30 ? "danger" : "info"
      this.generalData.futureInfo.push({type : type, message : `${ts}에 48시간 최고기온 ${info.temp[temp]}도 입니다.`, icon : "icon-bell-55"})

      temp = info.temp.indexOf(Math.min(...info.temp))
      ts = new Date(this.generalData.futureIndex[temp]).toLocaleString("kr-KR", {timeZone: "Asia/Seoul"})
      type = info.temp[temp] < 0 ? "danger" : "info"
      this.generalData.futureInfo.push({type : type, message : `${ts}에 48시간 최저기온 ${info.temp[temp]}도 입니다.`, icon : "icon-bell-55"})

      
    },
    initPastLineChart(index) {
      let chartData = {
        datasets: [{
          ...pastLineChartOptions,
          label: this.$t('spots.remained'),
          
          data: this.pastLineChart.data[index]
        }],
        labels : Array.from(Array(24).keys()).map(x=>x+this.$t('spots.hour'))
      };
      this.$refs.pastLineChart.updateGradients(chartData);
      this.pastLineChart.chartData = chartData;
      this.pastLineChart.activeIndex = index;
    }
  },
  watch : {
    target : function(value){
        this.getData(value)
    }
  },

}


</script>
<style>


</style>