<template>
    <div class="row mb-3">
        <div class="col">
            <div class="row">
                <div class="col align-self-start">
                    <h5>{{id}}</h5>
                </div>
                <div class="col-1 align-self-end">
                    <h5><i v-bind:class=get_expand_icon @click="toggle_expand()" style="cursor: pointer;"></i></h5>
                </div>
            </div>
            <hr />
            <div v-bind:class=get_expand_class>
                <p v-for="line in reversed" :key="line">{{line}}</p>
            </div>
            <hr />
        </div>
    </div>
</template>

<script setup>
import { computed, ref, reactive, onMounted } from "vue";
import { useVSUIStore } from '@/stores/vsui_store.js'
const store = useVSUIStore();
const socket = store.socket;

const props = defineProps({
    id: String,
    task_id: String
});
const expanded = ref(false)
function toggle_expand() {
    expanded.value = !expanded.value
}
const get_expand_class = computed(() => {
    if (expanded.value) {
        return ""
    } else {
        return "log"
    }
})
const get_expand_icon = computed(() => {
    if (expanded.value) {
        return "bi bi-chevron-up"
    } else {
        return "bi bi-chevron-down"
    }
});
const reversed = computed(() => {
    var logs = my_data.value;
    return logs.reverse();
});

const my_data = reactive({value: ['nothing to show']})

socket.on('log_data_update', (data) => {
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
.log {
    display: flex;
    flex-direction: column;
    max-height: 250px;
    overflow-y: scroll;
    mask-image: linear-gradient(to bottom, black 85%, transparent 100%);
    padding-bottom: 40px;
}
</style>