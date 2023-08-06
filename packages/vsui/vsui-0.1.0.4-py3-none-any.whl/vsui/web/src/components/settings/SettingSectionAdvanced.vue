<template>
    <div class="pb-4">
        <div class="row">
            <div class="col align-self-start">
                <h5 @click="toggle_expand()" style="cursor: pointer;">{{ header }}</h5>
            </div>
            <div class="col-1 align-self-end">
                <h5><i v-bind:class=expanded_icon[expanded] @click="toggle_expand()" style="cursor: pointer;"></i></h5>
            </div>
        </div>
        <hr />
        <div v-if="expanded">
            <component v-for="setting in struct" :key="setting.id" :is="components[setting.component]" :process_id="id"
                :setting="setting" />
            </div>
    </div>
</template>
<script setup>
import { ref } from 'vue';

import SettingText from './SettingText.vue';
import SettingNumber from './SettingNumber.vue';
import SettingDropdown from './SettingDropdown.vue';
import FileSelect from './FileSelect.vue';

const components = {
    'text': SettingText,
    'number': SettingNumber,
    'select': SettingDropdown,
    'file_select': FileSelect
}

const expanded = ref(false)
function toggle_expand() {
    expanded.value = !expanded.value
}
const expanded_icon = {
    true: "bi bi-chevron-up",
    false: "bi bi-chevron-down"
}

// eslint-disable-next-line
const props = defineProps({
    header: String,
    struct: Object,
    id: String
})
</script>
<style>
</style>