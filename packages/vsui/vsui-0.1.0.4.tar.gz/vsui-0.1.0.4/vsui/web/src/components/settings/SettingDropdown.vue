<template>
    <div class="row g-2 align-items-center mb-2">
        <div class="col">
            <div class="input-group">
                <span class="input-group-text" style="width:50%" :id="addon_id" :name="addon_id">{{ setting.name }}</span>
                <select class="form-select" :id="setting.id" :name="setting.name" v-model="my_data"
                    :aria-describedby="downsample_help_inline">
                    <option v-for="option in setting.options" :key="option.value" :value=option.value> {{ option.label }}
                    </option>
                </select>
                <span class="input-group-text">
                    <i class="bi bi-check"></i>
                </span>
            </div>
        </div>
        <div class="col">
            <span :id="help_id" class="form-text">
                {{ setting.help }}
            </span>
        </div>
    </div>
</template>
<script setup>
import { computed, ref, onMounted, watch } from 'vue';
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

watch(my_data, (newval) => {
    socket.emit('setting_change', { 'process_id': props.process_id, 'setting_id': props.setting.id, 'data': newval, 'namespace': props.setting.namespace })
})

onMounted(() => {
    socket.emit('request_setting', { 'process_id': props.process_id, 'setting_id': props.setting.id }, (response) => {
        my_data.value = response
    })
})
</script>
<style scoped>

</style>