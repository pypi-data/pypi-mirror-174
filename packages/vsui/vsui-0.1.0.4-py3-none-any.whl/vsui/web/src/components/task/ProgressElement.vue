<template>
    <div class="row mb-3">
        <div class="col">
            <h5>{{ id }} - {{my_data.value.current}} / {{my_data.value.max}}</h5>
            <div class="progress">
                <div class="progress-bar" role="progressbar" id="epoch-progress-bar" v-bind:style="{width: percentage + '%'}"
                    v-bind:aria-valuenow="percentage" aria-valuemin="0" aria-valuemax="100">
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { computed, reactive, onMounted } from "vue";
import { useVSUIStore } from '@/stores/vsui_store.js'
const store = useVSUIStore();
const socket = store.socket;

const props = defineProps({
        id: String,
        task_id: String
})

const my_data = reactive({value: {'current': 0, 'max': 1}});

const percentage = computed(() => {
        return ((my_data.value.current / my_data.value.max) *100);
})

socket.on('progress_data_update', (data) => {
    if (props.task_id in data) {
        if (props.id in data[props.task_id]) {
            my_data.value = data[props.task_id][props.id]
        }
    }
})
onMounted(() => {
    socket.emit('request_update', { 'task_id': props.task_id, 'key': props.id})
})
</script>

<style scoped>
.progress-bar {
    /* transition: width 100ms linear; */
    -webkit-transition: none !important;
    transition: none !important;
}
</style>