/*!

 =========================================================
 * Vue Black Dashboard PRO - v1.3.1
 =========================================================

 * Product Page: https://www.creative-tim.com/product/vue-black-dashboard-pro
 * Copyright 2019 Creative Tim (https://www.creative-tim.com)

 * Coded by Creative Tim

 =========================================================

 * The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
 */
import Vue from 'vue';
import VueRouter from 'vue-router';
import RouterPrefetch from 'vue-router-prefetch'
import DashboardPlugin from './plugins/dashboard-plugin';
import ErrorHandler from './plugins/errorHandler'
import App from './App.vue';
import axios from "axios";
import store from './store/index'

// router setup
import router from './routes/router';
import i18n from './i18n';
import './registerServiceWorker'
import VueFileAgent from 'vue-file-agent';
import VueFileAgentStyles from 'vue-file-agent/dist/vue-file-agent.css';
import 'leaflet/dist/leaflet.css';
import Vuex from 'vuex';
import VueGeolocationApi from 'vue-geolocation-api'
import {normalRequest, authRequest} from './login/auth'

import {
  ValidationProvider,
  extend,
  ValidationObserver,
  localize, // 지역
} from "vee-validate"
import * as rules from "vee-validate/dist/rules"
for (let rule in rules) {
  // add the rule
  extend(rule, rules[rule])
}
import ko from "vee-validate/dist/locale/ko.json"
localize({
  ko,
})
localize("ko") // 한국어 사용
Vue.component("ValidationProvider", ValidationProvider)
Vue.component("ValidationObserver", ValidationObserver)



// plugin setup
Vue.use(DashboardPlugin);
Vue.use(VueRouter);
Vue.use(RouterPrefetch);
Vue.use(VueFileAgent);
Vue.use(ErrorHandler);
Vue.use(Vuex);
Vue.use(VueGeolocationApi);

Vue.prototype.$http = axios;
Vue.prototype.$normalHttp = normalRequest
Vue.prototype.$authHttp = authRequest

/* eslint-disable no-new */
new Vue({
  el: '#app',
  render: h => h(App),
  router,
  i18n,
  store
});
