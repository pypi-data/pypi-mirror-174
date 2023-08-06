<template>
    <div class="row mb-3">
        <div class="col">
            <div class="row">
                <div class="col align-self-start">
                    <h5>{{ id }}</h5>
                </div>
                <div class="col-1 align-self-end">
                </div>
            </div>
            <hr />
            <div class="container">
                <div class="row" v-for="i in num_rows" :key="i">
                    <div class="col" v-for="j in num_cols" :key="j">
                        <img :src="img_src(reversed[(i-1)*num_cols + (j-1)])" class="img-fluid"
                            @click="open_viewer((i-1)*num_cols + (j-1))" v-if="(i - 1) * num_cols + (j - 1) < image_count" />
                    </div>
                </div>
            </div>
            <hr />
        </div>
    </div>
    <GalleryViewer ref="viewer" />
</template>

<script setup>
import { computed, ref, reactive, onMounted } from "vue";
import GalleryViewer from './GalleryViewer.vue';
import { useVSUIStore } from '@/stores/vsui_store.js';
const store = useVSUIStore();
const socket = store.socket;
const viewer = ref(null)

const props = defineProps({
    id: String,
    task_id: String
});
const num_cols = 4
const my_data = reactive({ value: [] })
const reference_images = ref([])

const reversed = computed(() => {
    var images = my_data.value;
    return images.reverse();
});
function img_src(bsfimage) {
    return "data:image/jpeg;base64, " + bsfimage
}
const image_count = computed(() => my_data.value.length)
const num_rows = computed(() => Math.ceil(image_count.value / num_cols))

function open_viewer(target) {
    viewer.value.set_images(img_src(reversed.value[target]));
    viewer.value.set_reference(reference_images.value.map(img_src))
    viewer.value.open();
}

socket.on('gallery_data_update', (data) => {
    if (props.task_id in data) {
        if (props.id in data[props.task_id]) {
            my_data.value = data[props.task_id][props.id]
        }
    }
})
socket.on('gallery_reference_update', (data) => {
    if (props.task_id in data) {
        if (props.id in data[props.task_id]) {
            reference_images.value = data[props.task_id][props.id]
            console.log('have some reference images')
        }
    }
})
onMounted(() => {
    socket.emit('request_update', { 'task_id': props.task_id, 'key': props.id })
})
</script>


<style scoped>
img:hover {
    border: 2px solid grey;
    cursor: pointer;
}
</style>