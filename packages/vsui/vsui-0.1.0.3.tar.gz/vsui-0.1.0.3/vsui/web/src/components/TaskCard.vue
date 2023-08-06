<template>
    <div class="card mb-2">
        <div class="card-header">
            <div class="float-start">
                {{ id }}
            </div>
            <div class="float-end">
                <button type="button" class="btn btn-outline-danger" @click="end_associated_process" disabled>End Process</button>
            </div>
        </div>
        <div :class="body_class">
            <component v-for="element in struct" :key="element.key" :is="components[element.component]"
                :id="element.key" :task_id="id" />
        </div>
    </div>
</template>

<script setup>
import { computed } from 'vue';
import ProgressElement from './task/ProgressElement.vue';
import LogElement from './task/LogElement.vue';
import ChartElement from './task/ChartElement.vue';
import GalleryElement from './task/GalleryElement.vue';
import { useVSUIStore } from '@/stores/vsui_store.js';

const store = useVSUIStore();
const socket = store.socket;

const components = {
    'ProgressElement': ProgressElement,
    'LogElement': LogElement,
    'ChartElement': ChartElement,
    'GalleryElement': GalleryElement
}

// eslint-disable-next-line
const props = defineProps({
    id: { required: true, type: String },
    struct: { default: null },
    active: { default: false, type: Boolean }
})

const body_class = computed (() => body_class_dict[props.active])
const body_class_dict = {
    true : "card-body border border-primary",
    false : "card-body border border-secondary"
}

function end_associated_process() {
    socket.emit('end_process', {'task_id': props.id})
}

</script>

<style scoped>
.inactive {
    background-color: lightgray;
}
.active {
    background-color: white;
}
</style>