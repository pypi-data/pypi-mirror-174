<template>
    <div class="card mb-2">
        <div class="card-header">
            <div class="float-start">
                {{ id }}
            </div>
        </div>
        <div class="card-body">
            <TaskIDInput :process_id="id" @new_task_id="set_new_task_id" />
            <!-- setting sections -->
            <component v-for="section in sections" :key="section.header" :is="components[section.type]"
                :struct="section.struct" :id="id" :header="section.header" />
            <div class="row">
                <div class="col">
                    <button type="button" class="btn btn-primary" @click="launch_process">Start</button>
                </div>
                <div class="col">
                    <div class="spinner-border text-primary" role="status" v-if="loading_task == true">
                        <span class="visually-hidden">Loading...</span>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { computed, ref, defineEmits } from 'vue';
import TaskIDInput from './settings/TaskIDInput.vue'
import SettingSectionBasic from './settings/SettingSectionBasic.vue';
import SettingSectionAdvanced from './settings/SettingSectionAdvanced.vue';
import { useVSUIStore } from '@/stores/vsui_store.js';
const store = useVSUIStore();
const socket = store.socket;
const emit = defineEmits(['settings_completed'])

const components = {
    'basic': SettingSectionBasic,
    'advanced': SettingSectionAdvanced,
}
const props = defineProps({
    id: { required: true, type: String },
    struct: { default: null },
    active: { default: false, type: Boolean },
})
const new_task_id = ref('')
const loading_task = ref(false)

const sections = computed(() => split_sections(props.struct))
// logic to split the settings into their sections
// recursively separates the structure into sections
function split_sections(list) {
    let next_section = list.slice(1).findIndex(is_separator) + 1
    if (next_section == 0) {
        return [{ 'header': list[0]['header'], 'type': list[0]['type'], 'struct': list.slice(1) }]
    } else {
        return [{ 'header': list[0]['header'], 'type': list[0]['type'], 'struct': list.slice(1, next_section) }].concat(split_sections(list.slice(next_section)))
    }
}
function is_separator(obj) {
    if (obj['component'] == "section") {
        return true
    } else {
        return false
    }
}

function set_new_task_id(id) {
    new_task_id.value = id
}
function launch_process() {
    socket.emit('launch_process', { 'process_id': props.id, 'task_id': new_task_id.value })
    loading_task.value = true
}
socket.on('server_added_task', (task_id) => {
    console.log(task_id)
    if (task_id == new_task_id.value) {
        loading_task.value = false
        emit('settings_completed', new_task_id.value, props.id)
    }
})
</script>

<style scoped>

</style>