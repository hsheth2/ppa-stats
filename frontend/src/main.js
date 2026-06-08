import { createApp } from 'vue';
import App from './App.vue';
import router from './router';

import axios from 'axios';

import AsyncComputed from 'vue-async-computed';

import '@mdi/font/css/materialdesignicons.css';
import Buefy from 'buefy';
import 'buefy/dist/css/buefy.css';

const axiosInstance = axios.create({
  baseURL: '/',
});
axiosInstance.interceptors.request.use((config) => {
  if (config.url) {
    config.url = config.url.replace('https://api.launchpad.net', '/lp-api');
  }
  return config;
});

const app = createApp(App);
app.config.globalProperties.$http = axiosInstance;
app.use(Buefy);
app.use(AsyncComputed);
app.use(router);
app.mount('#app');
