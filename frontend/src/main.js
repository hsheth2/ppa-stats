import Vue from 'vue';
import App from './App.vue';
import router from './router';

import VueResource from 'vue-resource';

import Buefy from 'buefy';
import 'buefy/dist/buefy.css';

Vue.use(Buefy);
Vue.use(VueResource);
Vue.config.productionTip = false;

new Vue({
  router,
  render: (h) => h(App),
}).$mount('#app');
