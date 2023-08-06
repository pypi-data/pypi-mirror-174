<template>
    <div class="pb-4">
        <h5>{{ header }}</h5>
        <hr />
        <component v-for="setting in struct" :key="setting" :is="components[setting.component]" :process_id="id"
            :setting="setting" />
    </div>
</template>
<script setup>
import SettingText from './SettingText.vue';
import SettingNumber from './SettingNumber.vue';
import SettingDropdown from './SettingDropdown.vue';
import FileSelect from './FileSelect.vue';

// eslint-disable-next-line
const components = {
    'text': SettingText,
    'number': SettingNumber,
    'select': SettingDropdown,
    'file_select': FileSelect
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