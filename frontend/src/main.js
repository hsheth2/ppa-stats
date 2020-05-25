import Vue from 'vue';
import App from './App.vue';
import router from './router';

import axios from 'axios';
import VueAxios from 'vue-axios';

import AsyncComputed from 'vue-async-computed';

import Buefy from 'buefy';
import 'buefy/dist/buefy.css';

Vue.use(Buefy);
Vue.use(VueAxios, axios);
Vue.use(AsyncComputed);
Vue.config.productionTip = false;

new Vue({
  router,
  render: (h) => h(App),
}).$mount('#app');
