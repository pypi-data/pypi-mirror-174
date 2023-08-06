<template>
    <div class="foggy d-flex justify-content-center align-items-center" v-if="opened">
        <FileBrowserCard ref="my_browser" :valid_selections="valid_selections" @close=close @user_selected=save_selection />
    </div>
</template>
<script setup>
import { ref, defineExpose, defineEmits } from 'vue';
import FileBrowserCard from './FileBrowserCard.vue';
const emit = defineEmits(['user_selected'])
const my_browser = ref(null)
// eslint-disable-next-line 
const props = defineProps({
    valid_selections: Object
})
const opened = ref(false)
function close() {
    opened.value = false
}
function open() {
    opened.value = true
}
function toggle() {
    if (opened.value) {
        close()
    } else {
        open()
    }
}
function set_initial_dir(dir) {
    my_browser.value.set_initial_dir(dir)
}
function save_selection(selection) {
    emit('user_selected', selection)
    close()
}
defineExpose({ open, close, toggle, set_initial_dir })
</script>
<style scoped>

</style>