<template>
    <div class="row align-items-center g-2 mt-2 pb-4">
        <div class="col">
            <div class="input-group">
                <span class="input-group-text" style="width:20%" id="task_id_label" name="task_id_label">Task ID</span>
                <input type="text" id="task_id_input" name="task_id_input" class="form-control" v-model="my_data"
                    :aria-describedby="task_id_help" />
                <span class="input-group-text">
                    <div v-if="input_state == 'editing'" class="spinner-grow spinner-grow-sm" role="status">
                        <span class="visually-hidden">Editing...</span>
                    </div>
                    <i v-if="input_state == 'success'" class="bi bi-check"></i>
                    <i v-if="input_state == 'error'" class="bi bi-exclamation-lg"></i>
                </span>
            </div>
        </div>
        <div class="col">
            <span id="task_id_help" class="form-text">
                Must be Unique
            </span>
        </div>
    </div>
    <div class="row align-items-center g-2">
        <p class="error">{{ error_msg }}</p>
    </div>
</template>
<script setup>
import { ref, watch, defineEmits, onMounted, onUpdated } from 'vue';
import { useVSUIStore } from '@/stores/vsui_store.js';
const store = useVSUIStore();
const socket = store.socket;
const emit = defineEmits(['new_task_id'])

const props = defineProps({
    process_id: String
})

const my_data = ref('')

var typingInterval = 1200;
var typingTimer = null;
const input_state = ref('success')
const error_msg = ref('')

watch(my_data, (newval) => {
    clearTimeout(typingTimer);
    input_state.value = 'editing'
    typingTimer = setTimeout(() => {
        if (validate(newval)) {
            socket.emit('request_is_task_id_unique', newval, (is_unique) => {
                if (is_unique) {
                    emit('new_task_id', my_data.value)
                    error_msg.value = ''
                    input_state.value = 'success'
                } else {
                    error_msg.value = 'Not Unique'
                    input_state.value = 'error'
                }
            })
        } else {
            error_msg.value = validation_errors['id']
            input_state.value = 'error'
        }
    }, typingInterval)
})

onUpdated(() => {
    update_task_id_input()
})
onMounted(() => {
    update_task_id_input()
})

function update_task_id_input() {
    let today = new Date();
    let date = String(today.getFullYear()) + String((today.getMonth() + 1)) + String(today.getDate());
    var time = String(today.getHours()) + String(today.getMinutes());
    let dateTime = date + "_" + time;
    my_data.value = props.process_id + "_" + dateTime
    if (validate(my_data.value)) {
        socket.emit('request_is_task_id_unique', my_data.value)
    } else {
        error_msg.value = validation_errors['id']
        input_state.value = 'error'
    }
}

function validate(newval) {
    let rule = regex_rules['id']
    return rule.test(newval)
}

const regex_rules = {
    'id': /^[\w\-_]+$/ // same as required filename
}

const validation_errors = {
    'id': 'Required, Must only contain characters { A-Z - _ }.'
}
</script>
<style scoped>
.error {
    color: red;
}
</style>