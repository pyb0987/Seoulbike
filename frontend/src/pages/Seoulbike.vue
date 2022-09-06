<template>
    <div id="seoulbike">
        <div style="height:340px"></div>
         <card class="card-subcategories card-plain col-sm-9 col-md-7 col-lg-5 mx-auto">
        
          <template slot="header">
            <h1 class="card-title text-center mt-5">Seoulbike</h1>
            <h1 class="text-center card-category">{{$t('seoulbike.seoulbikeExplanation')}}</h1>
            <br />
          </template>

          <tabs
            type="primary"
            tabContentClasses="tab-subcategories"
            square
            centered
            class="row"
          >

              <tab-pane class="main-tab-pane">
                  <span slot="label">
                      <i class="tim-icons icon-compass-05"></i>Map
              </span>
              <p>{{$t('seoulbike.mapExplanation')}}</p>
              <div class="row justify-content-end">

                  <base-button
                type="primary"
                @click="toMap"
                >{{$t('seoulbike.seemore')}}</base-button>
                </div>

            </tab-pane>

            <tab-pane class="main-tab-pane">
                <span slot="label">
                    <i class="tim-icons icon-bulb-63"></i>Insight
              </span>
              <p>{{$t('seoulbike.insightExplanation')}}</p>
              <div class="row justify-content-end">

                  <base-button
                type="primary"
                @click="toEDA"
                >{{$t('seoulbike.seemore')}}</base-button>
                </div>
            </tab-pane>

            <tab-pane class="main-tab-pane">
                <span slot="label">
                    <i class="tim-icons icon-chart-bar-32"></i>Analysis
              </span>
              Completely synergize resource taxing relationships via premier
              niche markets. Professionally cultivate one-to-one customer
              service with robust ideas. <br /><br />Dynamically innovate
              resource-leveling customer service for state of the art customer
              service.
            </tab-pane>
          </tabs>
        </card>

    </div>
</template>

<script>
import { TabPane, Tabs} from 'src/components';

export default {
  components: {
    TabPane,
    Tabs,
  },
  data() {
    return {
      
    };
  },
  methods : {
    toMap(){
        this.$router.push('/seoulbike/spots')
    },
    toEDA(){
      this.$router.push('/analysis/eda-1')
    }
  }
};
</script>
<style>
.main-tab-pane{
    height: 350px;
}

</style>