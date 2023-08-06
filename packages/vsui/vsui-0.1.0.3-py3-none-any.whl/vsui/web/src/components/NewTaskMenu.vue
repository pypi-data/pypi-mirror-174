<template>
    <div class="position-absolute overlay" :style="{ top: context_menu_top + 'px', left: context_menu_left + 'px' }"
        v-if="opened">
        <div class="card" style="width: 18rem;">
            <div class="card-header">
                <div class="float-start">
                    Add Task
                </div>
                <div class="float-end">
                    <i class="bi bi-x-lg clickable" @click="close()"></i>
                </div>
            </div>
            <ul class="list-group list-group-flush">
                <li class="list-group-item clickable" v-for="option in available_processes.value" :key="option.name" @click="process_chosen(option)">{{ option.name }}</li>
            </ul>
        </div>
    </div>
</template>
<script setup>
import { ref, reactive, defineExpose, defineEmits } from 'vue';
const opened = ref(false)
const emit = defineEmits(['process_chosen'])
const context_menu_left = ref(0)
const context_menu_top = ref(0)
const available_processes = reactive({value: []})

function open(opt) {
    opened.value = true
    available_processes.value = opt
}
function close() {
    opened.value = false
}
function toggle(opt) {
    if (opened.value) {
        close()
    } else {
        open(opt)
    }
}
function set_position(left, bottom) {
    context_menu_left.value = left;
    context_menu_top.value = bottom;
}
function process_chosen(option) {
    close()
    emit('process_chosen', option)
}

defineExpose({ open, toggle, set_position })

</script>
<style scoped>
.overlay {
    z-index: 100;
}
li:hover {
    background-color: whitesmoke;
}
</style>