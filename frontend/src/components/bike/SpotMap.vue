<template>
    <l-map ref="map" style="height: 500px" :zoom="map.zoom" :center="map.center" @update:bounds="boundsUpdated" :minZoom="14"  :max-bounds="maxBounds">
          <l-tile-layer :url="map.url" :attribution="map.attribution"></l-tile-layer>
            <l-marker v-for="(item, i) in bikespotOnMap"
          @click="bikeSpotClick(item)"
            :key="item.idnumber"
            :autoPanOnFocus="false"
            :lat-lng="[item.latitude, item.longitude]">
            <l-icon>
            <div class="bike_number_digit1" v-if="item.bike_number<10" >{{ item.bike_number }}</div>
            <div class="bike_number_digit2" v-else>{{ item.bike_number }}</div>
            </l-icon>
            <l-tooltip>{{item.spot_name}}</l-tooltip>
          </l-marker>
        <l-circle-marker v-for="(item, i) in bikespotOnMap" 
          @click="bikeSpotClick(item)"
          :lat-lng="[item.latitude, item.longitude]"
          :radius = "15"
          :weight = "2"
          :autoPanOnFocus="false"
          :key="-item.idnumber"
          :color = "bikeSpotColor(item.idnumber)"
          :fillColor = "bikeSpotColor(item.idnumber)"
          >
          </l-circle-marker>
          <l-control-scale position="topright" :imperial="false" :metric="true"></l-control-scale>
    </l-map>
</template>

<script>
import config from '@/config';
import L from 'leaflet';
import { LMap, LTileLayer, LMarker, LControlScale, LPopup,  LTooltip, LCircleMarker, LIcon } from 'vue2-leaflet';
import { Icon } from 'leaflet';
import { latLngBounds } from "leaflet";


export default {
  components: {
    LMap,
    LTileLayer,
    LMarker,
    LControlScale,
    LPopup,
    LTooltip,
    LCircleMarker,
    LIcon,
  },
  props : ['mode', 'selectedBikespot', 'MapCenterSpot', 'userLikeSpots'],
  data() {
    return {
      map : {
        url: 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
        attribution:'&copy; <a target="_blank" href="http://osm.org/copyright">OpenStreetMap</a> contributors',
        zoom: 15,
        center: [],
        bounds : {
          xmin : null,
          xmax : null,
          ymin : null,
          ymax : null,
        },
      },
    maxBounds: latLngBounds([
        [37.4120824,126.7601119],
        [37.6999234,127.1658936]
      ]),

      bikespotOnMap : [],
      bikespotData : null,
      bikeSpotInfo : {},
      bikespotSet : [],
    };
  },
  methods : {
    addSpotsOnMap(){
      let y2 = this.map.bounds.ymax;
      let x2 = this.map.bounds.xmax;
      let y1 = this.map.bounds.ymin;
      let x1 = this .map.bounds.xmin;
      if (this.bikespotOnMap.length > 500){
        this.bikespotOnMap.splice(0, 300)
      }
      this.bikespotOnMap = this.bikespotData.reduce((acc, spot) => {
        if (spot.latitude > y1 && spot.latitude < y2 && spot.longitude > x1 && spot.longitude < x2){    //지도안에 있을경우
        acc.push(spot);
      }
        return acc
      }, []);
    },
    boundsUpdated (bounds) {
      this.map.bounds.ymax = bounds._northEast.lat;
      this.map.bounds.xmax = bounds._northEast.lng;
      this.map.bounds.ymin = bounds._southWest.lat;
      this.map.bounds.xmin = bounds._southWest.lng;
      if(!!this.bikespotData){
        this.addSpotsOnMap()
      }
    },
    bikeSpotClick(bikespot){ 
        this.$emit('bikeSpotClick', bikespot)
        if(this.mode === 'multiple'){
          let index = this.bikespotSet.indexOf(bikespot.idnumber);
            if (index === -1) {
              this.bikespotSet.push(bikespot.idnumber)
          }else{
            this.bikespotSet.splice(index, 1);
          }
        }else{
          this.bikespotSet = [bikespot.idnumber]
        }
        this.$emit('bikeSpots', this.bikespotSet)
        
    },
    bikeSpotColor(idnumber){
      if (!!this.bikespotSet && this.bikespotSet.includes(idnumber)){
        return 'red'
      }
      else if(!!this.userLikeSpots && this.userLikeSpots.includes(idnumber)){
        return 'green'
      }
      return 'blue'
    },
    async geofind(defaultvalue) {
      if(!("geolocation" in navigator)) {
        await this.$errorHandler(null, '해당 브라우저에서 gps 서비스를 지원하지 않습니다.')
            this.map.center = defaultvalue;
            }
            navigator.geolocation.getCurrentPosition(pos => {
              console.log('pos', pos, [pos.coords.latitude, pos.coords.longitude])
            this.map.zoom = 17
            this.map.center= [pos.coords.latitude, pos.coords.longitude];
            }, err => {
            this.$errorHandler(null, '현재 위치를 확인하는데 에러가 발생했습니다.')
            this.map.center = defaultvalue
            })
          return
        }
  },
  watch : {
    'MapCenterSpot' : function(value){
      this.map.center = [value.latitude, value.longitude]
      this.map.zoom = 18
      this.bikeSpotClick(value)
    }
  },
  created(){
    

    if(!!this.selectedBikespot){
      this.bikespotSet = this.selectedBikespot
    }
    if(!!this.MapCenterSpot){
      this.map.center = [this.MapCenterSpot.latitude, this.MapCenterSpot.longitude]
    }else{
      this.map.center = [37.52715683, 126.9319]
    }
    this.geofind([37.52715683, 126.9319])
    console.log(this.map.center)

    this.$normalHttp.get("/api/seoulbike/bikespot/all").then((res)=>{
    this.bikespotData = res.data  
    this.map.bounds.xmin = this.map.center[1] - 0.04076/2
    this.map.bounds.xmax = this.map.center[1] + 0.04076/2
    this.map.bounds.ymin = this.map.center[0] - 0.017/2
    this.map.bounds.ymax = this.map.center[0] + 0.017/2
    this.addSpotsOnMap()
  }).catch((err)=>{
    this.$errorHandler(err, '대여소 지도 정보를 받아오는 데 실패했습니다!')
  })

  }


};
</script>
<style>
.bike_number_digit1{
    font-size: 1rem;
    font-weight: 600;
    white-space: nowrap;
    transform: translateY(-0.3rem) translateX(0.15rem);
    color: black;
    text-shadow: -0.7px 0 #fff, 0 0.7px #fff, 0.7px 0 #fff, 0 -0.7px #fff;
}
.bike_number_digit2{
    font-size: 1rem;
    font-weight: 600;
    white-space: nowrap;
    transform: translateY(-0.3rem) translateX(-0.15rem);
    color: black;
    text-shadow: -0.7px 0 #fff, 0 0.7px #fff, 0.7px 0 #fff, 0 -0.7px #fff;
}
</style>
