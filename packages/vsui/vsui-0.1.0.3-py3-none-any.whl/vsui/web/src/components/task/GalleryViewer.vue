<template>
    <div class="foggy d-flex justify-content-center align-items-center" @click.stop="close()" v-if="opened">
            <div class="row">
                <div class="col">
                    <img :src="focus_img" class="img-fluid" />
                </div>
                <!--TODO these should not be hardcoded as first 2-->
                <div class="col">
                    <img :src="references[1]" class = "img-fluid" />
                </div>
                <div class="col">
                    <img :src="references[0]" class = "img-fluid" />
                </div>
            </div>
    </div>
</template>
<script setup>
import { ref, defineExpose } from 'vue';
const opened = ref(false)
const focus_img = ref('')
const references = ref([])

function set_images(x) {
    focus_img.value = x
}
function close() {
    opened.value = false
}
function open() {
    opened.value = true
}
function set_reference(x) {
    references.value = x
}
defineExpose({ open, close, set_images, set_reference })
</script>
<style scoped>

.focus{
    max-height: 60vh;
    max-width: 60vw;
}
</style>