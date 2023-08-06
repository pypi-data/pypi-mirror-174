<template>
    <div class="row align-items-center g-2 mb-2">
        <div class="col">
            <div class="input-group">
                <span class="input-group-text" style="width:50%" :id="addon_id" :name="setting.name">{{ setting.name }}</span>
                <input type="number" :id="setting.id" :name="setting.name" class="form-control" v-model.number="my_data" :aria-describedby="help_id" />
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
            <span :id="help_id" class="form-text">
                {{ setting.help }}
            </span>
        </div>
    </div>
    <div class="row align-items-center g-2" v-if="error_msg != ''">
        <p class="error">{{error_msg}}</p>
    </div>
</template>
<script setup>
import { computed, ref, watch, onMounted } from 'vue';
import { useVSUIStore } from '@/stores/vsui_store.js';
const store = useVSUIStore();
const socket = store.socket;

const my_data = ref('')
const props = defineProps({
    process_id: String,
    setting: Object
})
const help_id = computed(() => props.setting.id + "_help_inline")
const addon_id = computed(() => props.setting.id + "_addon")

var typingInterval = 500;
var typingTimer = null;
const input_state = ref('success')
const error_msg = ref('')

watch(my_data, (newval) => {
        clearTimeout(typingTimer);
    input_state.value = 'editing'
    typingTimer = setTimeout(() => {
        save_input(newval)
    }, typingInterval)
})

function save_input(newval) {
    if (validate(newval)) {
        socket.emit('setting_change', { 'process_id': props.process_id, 'setting_id': props.setting.id, 'data': newval, 'namespace': props.setting.namespace })
        input_state.value = 'success'
        error_msg.value = ''
    } else {
        input_state.value = 'error'
        error_msg.value = validation_errors[props.setting.validation]
    }
}

function validate(newval) {
    let rule = regex_rules[props.setting.validation]
    return rule.test(newval)
}

onMounted(() => {
    socket.emit('request_setting', { 'process_id': props.process_id, 'setting_id': props.setting.id }, (response) => {
        my_data.value = response
    })
})

const regex_rules = {
    'integer': /^[0-9]*$/,
    'required integer': /^[0-9]+$/,
    'float': /^([0-9]+\.*[0-9]*|[0-9]*\.+[0-9]+|[0-9]+\.?e-?[0-9]+|^(?![\s\S]))$/,
    'required float': /^([0-9]+\.*[0-9]*|[0-9]*\.+[0-9]+|[0-9]+\.?e-?[0-9]+)$/
}

const validation_errors = {
    'integer': 'Must be an Integer.',
    'required integer': 'Required, Must be an Integer.',
    'float': 'Must be a number. Scientific notation e.g. 6.022e-23 is supported.',
    'required float': 'Required, Must be a number. Scientific notation e.g. 6.022e-23 is supported.'
}
</script>
<style scoped>
.error{
    color: red;
}
</style>