<template>
    <div class="row align-items-center g-2">
        <div class="col-6">
            <div class="vertical-input-group mb-2">
                <div :class="input_group_class(index)" @click="open_file_browser(index - 1)" v-for="index in input_count"
                    :key="my_data[index - 1]">
                    <span v-if="index==1" class="input-group-text" style="width:25%" :id="addon_id" :name="setting.name">
                    {{setting.name}}</span>
                    <button type="Button" style="width:15%" :id="id + 'btn'" :name="setting.name" class="form-control"
                        :aria-describedby="help_id">Browse</button>
                    <span class="input-group-text filename" style="width:60%" :id="addon_id + 'post'"
                        :name="name">{{ textbox_msg(my_data[index - 1]) }}</span>
                </div>
            </div>
        </div>
        <div class="col-6">
            <span :id="help_id" class="form-text">
                {{ setting.help }}
            </span>
        </div>
    </div>
    <FileBrowserModal :valid_selections="['file']" ref="file_browser" @user_selected="add_filepath_to_selection" />
</template>
<script setup>
import { ref, computed } from 'vue';
import FileBrowserModal from '../file_browser/FileBrowserModal.vue';
import { useVSUIStore } from '@/stores/vsui_store.js';
const store = useVSUIStore();
const socket = store.socket;
const file_browser = ref(null)

const my_data = ref([])
const last_opened_index = ref(0)
const input_count = computed(() => my_data.value.length + 1)
// eslint-disable-next-line
const props = defineProps({
    process_id: String,
    setting: Object
})
function open_file_browser(index) {
    last_opened_index.value = index
    file_browser.value.open()
}
function add_filepath_to_selection(path) {
    if (last_opened_index.value < input_count.value - 1) {
        my_data.value.splice(last_opened_index, 1, path)
        save_input(my_data.value)
    } else {
        my_data.value.push(path)
        save_input(my_data.value)
        input_count.value = ++input_count.value
    }
}

function save_input(newval) {
    socket.emit('setting_change', { 'process_id': props.process_id, 'setting_id': props.setting.id, 'data': newval, 'namespace': props.setting.namespace })
}
const textbox_msg = (txt) => txt == undefined ? '+ Add' : txt.split("/").at(-1)
const is_optional = (index) => index == my_data.value.length + 1 && my_data.value.length != 0
const input_group_class = (index) => ({
    "input-group": !is_optional(index),
    "input-group translucent": is_optional(index)
})
</script>
<style scoped>
.filename {
    background-color: white;
}

.input-group-text {
    overflow-x: scroll;
    max-width: 100%;
}

button:hover {
    background-color: whitesmoke;
}

.translucent {
    opacity: 0.6;
}
/*https://stackoverflow.com/a/55864043*/
.vertical-input-group .input-group:first-child {
    padding-bottom: 0;
}

.vertical-input-group .input-group:first-child:not(:only-child) * {
    border-bottom-left-radius: 0;
    border-bottom-right-radius: 0;
}

.vertical-input-group .input-group:last-child {
    padding-top: 0;
}

.vertical-input-group .input-group:last-child:not(:only-child) * {
    border-top-left-radius: 0;
    border-top-right-radius: 0;
}

.vertical-input-group .input-group:not(:last-child):not(:first-child) {
    padding-top: 0;
    padding-bottom: 0;
}

.vertical-input-group .input-group:not(:last-child):not(:first-child) * {
    border-radius: 0;
}

.vertical-input-group .input-group:not(:first-child) * {
    border-top: 0;
}
</style>