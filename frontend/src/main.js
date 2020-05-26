import Vue from 'vue';
import App from './App.vue';
import router from './router';

import axios from 'axios';
import VueAxios from 'vue-axios';

import AsyncComputed from 'vue-async-computed';

import Buefy from 'buefy';
import 'buefy/dist/buefy.css';

const axiosInstance = axios.create({
  baseURL: '/',
});
axiosInstance.interceptors.request.use((config) => {
  if (config.url) {
    config.url = config.url.replace('https://api.launchpad.net', '/lp-api');
  }
  return config;
});
Vue.use(VueAxios, axiosInstance);

Vue.use(Buefy);
Vue.use(AsyncComputed);
Vue.config.productionTip = false;

new Vue({
  router,
  render: (h) => h(App),
}).$mount('#app');
