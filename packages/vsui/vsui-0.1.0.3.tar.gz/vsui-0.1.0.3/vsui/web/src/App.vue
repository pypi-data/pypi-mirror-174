<template>
  <html>

  <body>
    <nav class="navbar fixed-top navbar-expand-sm navbar-light bg-light" aria-label="Volume Segmentation Toolkit">
      <div class="container-fluid">
        <div class="navbar-brand">Volume Segmentation Toolkit</div>
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbar_top"
          aria-controls="navbar_top" aria-expanded="false" aria-label="Toggle navigation">
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbar_top">
          <ul class="navbar-nav ms-auto">
            <button type="button" class="btn btn-outline-primary" @click="open_file_browser">{{
                choose_working_dir_btn_msg
            }}</button>
          </ul>
        </div>
      </div>
      <hr />
    </nav>
    <div class="container-fluid mt-20">
      <div class="row gx-1">
        <div class="col-3">
          <div class="card">
            <div class="card-header d-flex justify-content-between align-items-center">
              <h5>Tasks</h5>
              <h3><button class="btn btn-outline-primary clickable" ref="new_task_button"
                  @click.self="position_task_menu()">New Task</button>
              </h3>
            </div>
            <ul class="list-group list-group-flush">
              <!-- Setting Card -->
              <li :class=get_card_class(card) v-for="card in setting_cards" :key="card" @click="select_card(card, 'SettingsCard')">
                {{ card.id }}
                <div class="float-end" v-if="card.card_type == 'SettingsCard'"><i class="bi bi-x-lg"
                    @click.stop="remove_card(card)"></i></div>
              </li>
              <!-- Tasks -->
              <li :class=get_card_class(card) v-for="card in task_cards" :key="card" @click="select_card(card, 'TaskCard')">
                {{ card.id }}
              </li>
              <!-- Other -->
              <li :class=get_card_class(card) v-for="card in other_cards" :key="card" @click="select_card(card, 'TaskCard')">
                {{ card.id }}
              </li>
            </ul>
          </div>
        </div>
        <div class="col-9">
          <!-- Tasks cards Here -->
          <component :is="components[selected_card_list]" :id="selected_card.id" :struct="selected_card.struct"
            :active="selected_card.active" @settings_completed="settings_completed" :key="component_key" />
        </div>
      </div>
      <NewTaskMenu ref="task_menu" @process_chosen="new_settings" />
      <FileBrowserModal ref="file_browser" :valid_selections="['dir']" @user_selected="set_working_directory" />
    </div>
  </body>

  </html>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";
import TaskCard from '@/components/TaskCard.vue';
import SettingsCard from "./components/SettingsCard.vue";
import NewTaskMenu from '@/components/NewTaskMenu.vue';
import FileBrowserModal from "./components/file_browser/FileBrowserModal.vue";
import { useVSUIStore } from '@/stores/vsui_store.js';
import { useToast } from "vue-toastification";
const store = useVSUIStore();
const socket = store.socket;
const toast = useToast();
const new_task_button = ref(null)
const task_menu = ref(null)
const file_browser = ref(null)

const component_key = ref(0)
function force_reload() {
  component_key.value +=1
}
const components = {
  'TaskCard': TaskCard,
  'SettingsCard': SettingsCard
}
const choose_working_dir_btn_msg = computed(() => store.working_directory == '/' ? 'Choose Working Directory' : store.working_directory)

const available_processes = ref([])
const task_cards = ref([])
const setting_cards = ref([])
const other_cards = ref([{
    "id": "Help",
    "struct": [{ "key": "Nothing to Show", "component": "LogElement" }],
    "active": false
  }])
const selected_card_list = ref('TaskCard')

const selected_card = ref(other_cards.value[0])
function select_card(card, list) {
  selected_card_list.value = list
  selected_card.value = card
}
function remove_card(card) {
  if (card.id == selected_card.value.id) {
    select_card(other_cards.value[0])
  }
  setting_cards.value.splice(setting_cards.value.findIndex(x => x.id === card.id), 1)
}
// eslint-disable-next-line
function settings_completed(new_task_id, setting_id) {
  //select_card(task_cards.value.find(card => card.id === new_task_id))
  remove_card(setting_cards.value.find(card => card.id === setting_id))
  select_card(other_cards.value.at(0))
}
function new_settings(process) {
  if (!setting_cards.value.some(x => x.id === process.name)) {
    setting_cards.value.push({ "id": process.name, "struct": process.settings_schema, "active": false, "card_type": "SettingsCard" })
    select_card(setting_cards.value.at(-1), 'SettingsCard')
  }
}
// get the class for the item in the tasks list based on: selection status; running state ect
function get_card_class(card) {
  // spaces must be added before appended class statements
  var class_string = "list-group-item pointer clickable"
  if (selected_card.value.id == card.id) {
    class_string += " border border-primary border-4"
  }
  return class_string
}

function open_file_browser() {
  file_browser.value.toggle()
}
function set_working_directory(dir) {
  store.set_working_directory(dir)
}

function position_task_menu() {
  const left = new_task_button.value.getBoundingClientRect().left
  const bottom = new_task_button.value.getBoundingClientRect().bottom
  task_menu.value.set_position(left, bottom);
  task_menu.value.toggle(available_processes.value);
}

// SocketIO
// these events handle the connection between the frontend and backend
socket.on('connect', () => {
  console.log('connected')
  toast("server connected");
})
socket.on('disconnect', () => {
  console.log('disconnected')
  toast.error('server disconnected');
  select_card(other_cards.value.at(-1))
  task_cards.value = []
})
socket.on('tasks', (task_list) => {
  console.log('tasks update')
  force_reload()
  task_cards.value = task_list;
})
socket.on('available_processes', (process_list) => {
  available_processes.value = process_list;
})
onMounted(() => {
  socket.emit('request_working_dir', (response) => {
    store.set_working_directory(response)
  })
})
// pass notifications to toasts
socket.on('toast', (data) => {
  var txt = data.txt;
  var type = data.type;
  if (type == 'success') {
    toast.success(txt);
  } else if (type == 'error') {
    toast.error(txt);
  } else if (type == 'info') {
    toast.info(txt);
  } else if (type == 'warning') {
    toast.warning(txt);
  }
})
</script>

<style>
.clickable {
  cursor: pointer;
}

body {
  padding-top: 2.2rem;
  /*background-color: whitesmoke;*/
}

html {
  padding: 0;
  margin: 0;
  width: 100%;
  min-height: 100%;
  /*background-color: whitesmoke;*/
}

.context-bar {
  width: 100%;
  display: inline-flex;
  overflow: hidden;
  text-decoration: none;
}

.navbar {
  -webkit-box-shadow: 0px 1px 4px 0px rgba(0, 0, 0, 0.75);
  -moz-box-shadow: 0px 1px 4px 0px rgba(0, 0, 0, 0.75);
  box-shadow: 0px 1px 4px 0px rgba(0, 0, 0, 0.75);
}

.foggy {
  position: fixed;
  background-color: rgba(50, 50, 50, 0.5);
  height: 100vh;
  width: 100vw;
  z-index: 200;
  top: 0;
  left: 0;
}
</style>
