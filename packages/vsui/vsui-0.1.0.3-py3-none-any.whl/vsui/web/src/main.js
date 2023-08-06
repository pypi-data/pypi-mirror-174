import { createApp } from 'vue';
import { createPinia } from 'pinia';
import App from './App.vue';
import Toast from "vue-toastification";
import "vue-toastification/dist/index.css";
import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap';
import "bootstrap-icons/font/bootstrap-icons.css";
import 'bootstrap/dist/js/bootstrap.bundle.min.js';

const pinia = createPinia();
const app = createApp(App);
const options = {
    position : 'bottom-right'
};
app.use(pinia);
app.use(Toast, options);
app.mount('#app')
