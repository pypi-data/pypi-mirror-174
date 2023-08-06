<template>
    <div class="card">
        <div class="card-header d-flex justify-content-center">
            <div class="btn-group p-2" role="group" aria-label="Nav Buttons">
                <button type="button" class="btn btn-outline-primary" :disabled="at_end_of_backward_stack" @click="go_back">
                    <i class="bi bi-chevron-left"></i></button>
                <button type="button" class="btn btn-outline-primary" :disabled="at_end_of_forward_stack" @click="go_forward">
                    <i class="bi bi-chevron-right"></i></button>
            </div>
            <div class="input-group p-2">
                <input v-model="search_path" type="text" class="form-control" aria-label="filepath"
                    @focus="$event.target.select()" @keyup.enter="search">
                <button class="btn btn-outline-primary" type="button" @click="search"><i
                        class="bi bi-search"></i></button>
            </div>
            <div class="btn-group p-2" role="group" aria-label="Right nav Buttons">
                <button type="button" class="btn btn-outline-primary" @click="go_up">
                    <i class="bi bi-arrow-90deg-up"></i></button>
                <button type="button" class="btn btn-outline-primary" @click="go_home">
                    <i class="bi bi-house"></i></button>
                <button type="button" class="btn btn-outline-secondary p-2" @click="close_me"><i
                        class="bi bi-x-lg"></i></button>
            </div>
        </div>
        <div class="card-body" v-if="view_mode == 'list'">
            <div class="list-view">
                <div v-for="child in directory_contents" :key="child.path" :class="file_class(child)"
                    @click="select(child)">
                {{child.path}}
                </div>
            </div>
        </div>
        <div class="card-body overflow-scroll" v-if="view_mode == 'grid'">
            <div class="d-flex flex-wrap">
                <div v-for="child in directory_contents" :key="child.path" :class="file_class(child)"
                    @click="select(child)">
                    <div class="col">
                        <div class="row text-center">
                            <i :class="icons[child.type]" style="font-size: 6rem;"></i>
                        </div>
                        <div class="row text-center d-flex flex-wrap" style="width: 12rem;">
                            <p>{{ "/" + child.path.split("/").at(-1) }}</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <div class="card-footer text-muted inline align-middle d-flex justify-content-between">
            <b>{{ selected_file_path }}</b>
            <b>{{ error }}</b>
            <button type="button" class="btn btn-outline-primary" :disabled="nothing_selected"
                @click="push_selection">Select</button>
        </div>
    </div>
</template>
<script setup>
import { defineEmits, defineExpose, ref, onMounted, computed, watch } from 'vue';
import { useVSUIStore } from '@/stores/vsui_store.js';
const store = useVSUIStore();
const socket = store.socket;
const home_dir = ref(store.working_directory);
const initial_dir = ref('')
const emit = defineEmits(['close, user_selected'])

const props = defineProps ({
    valid_selections: Object,
})
const view_mode = ref('grid')
// This stores the current string in the search bar
const search_path = ref('')
// the forward and backward stacks and our current directory stored as a list of paths
const forward_path_stack = ref([])
const backward_path_stack = ref([])
const current_path = ref('')

// the currently selected file
const selected_file_path = ref('')
// the error if there was one
const error = ref('')
// the contents of the directory we are currently viewing
const directory_contents = ref([])
// the rules for what can be selected this session
// eslint-disable-next-line 

// these check if we are at the start or end of the history
const at_end_of_forward_stack = computed(() => forward_path_stack.value.length == 0 || current_path.value == forward_path_stack.value.at(-1))
const at_end_of_backward_stack = computed(() => backward_path_stack.value.length == 0 || current_path.value == backward_path_stack.value.at(-1))
const nothing_selected = computed(() => selected_file_path.value == '')

// incrementing through the history
function go_back() {
    console.log(backward_path_stack.value)
    if (at_end_of_backward_stack.value) {
        error.value = 'cannot go back'
    } else {
        // add the current path to the forward stack
        forward_path_stack.value.push(current_path.value);
        // set current path to top of backward stack
        move_to_dir(backward_path_stack.value.at(-1));
        // remove from backward stack
        backward_path_stack.value.pop();
    }
}
function go_forward() {
    console.log(forward_path_stack.value)
    if (at_end_of_forward_stack.value) {
        error.value = 'Cannot go Forward'
        return;
    } else {
        // add the current path to the backward stack
        backward_path_stack.value.push(current_path.value);
        // set current path to top of the forward stack
        move_to_dir(forward_path_stack.value.at(-1))
        // remove from forward stack
        forward_path_stack.value.pop();
    }
}
// go back to the initial directory
function go_home() {
    move_to_dir(home_dir.value)
}
// go up a directory
function go_up() {
    let split_path = current_path.value.split("/")
    if (split_path.at(-1) == "") {
        // Remove any trailing /
        split_path.pop()
    }
    // there is no trailing /
    // remove our current dir
    split_path.pop()
    let new_path = split_path.join("/")
    if (new_path == "") {
        // are we at the root
        new_path = "/"
    }
    move_to_dir(new_path)
}
function search() {
    // set our current directory to what is in the search bar
    if (search_path.value == selected_file_path.value) {
        push_selection(search_path.value)
    } else {
        move_to_dir(search_path.value)
    }
}
// navigate to the initial directory on mount
onMounted(() => {
    // if a home is passed set it, else got to the global home
    initial_dir.value == '' ? move_to_dir(store.prev_file_browser_path) : move_to_dir(initial_dir.value)
    // go to the initial directory
})


// watch the current path, when it is changed we should request and display the contents of that directory
function move_to_dir(path) {
    // request the contents of that dir
    socket.emit('request_directory_contents', path, (response) => {
        if (response.status == 'success') {
        // clear any errors
        error.value = ''
        // if the current path is not empty
        if (current_path.value != '') {
            // add where we just were to the backward stack
            backward_path_stack.value.push(current_path.value)
        }
        // set the current path to the new dir
        current_path.value = response.path
        // set the selected file to be the one we are moving to
        selected_file_path.value = response.path
        // set the directory contents to the current directory
        directory_contents.value = response.contents
    } else {
        error.value = response.status
    }
    })
}

// logic for single clicking a file to select
function select(file) {
    // is this file already selected?
    if (selected_file_path.value != file.path) {
        // if it isn't it should be selected
        selected_file_path.value = file.path
    } else {
        // if it is a directory try to move to it
        if (file.dir) {
            move_to_dir(file.path)
        } else {
            // double clicking something we cannot move to should make it our final selection
            push_selection(file.path)
            //push_selection()
        }
    }
}
// add highlight to selected file
function file_class(file) {
    if (selected_file_path.value == file.path) {
        return "p-2 selected"
    } else {
        return "p-2"
    }
}

// when the path is changed, the search bar should be updated
watch(current_path, (newval) => {
    search_path.value = newval
})

// tell my parent to close
function close_me() {
    console.log('close')
    emit('close')
}
// push the user's selection to my parent
function push_selection() {
    // should check we are selecting the right type of thing
    socket.emit("request_filetype", selected_file_path.value, (response) => {
        if (props.valid_selections.includes(response)) {
            error.value = ''
            store.set_prev_file_browser_path(current_path.value)
            emit('user_selected', selected_file_path.value)
        } else {
            error.value = 'Invalid selection'
        }
    });
}
function set_initial_dir(dir) {
    initial_dir.value = dir
}
defineExpose({ set_initial_dir})
// map what a child is to what icon to display for it
const icons = {
    'directory': 'bi bi-folder-fill file clickable',
    'directory-empty': 'bi bi-folder file clickable',
    'file-generic': 'bi bi-file-earmark file clickable',
    'file-data': 'bi bi-file-earmark-image file clickable',
    'file-yaml': 'bi bi-filetype-yml file clickable'
}
</script>
<style scoped>
.card {
    width: 70%;
    height: 70%
}

.file {
    margin-bottom: 0.1rem;
}

.selected {
    background-color: lightgray;
    border-radius: 10px;
}

.list-view {
    display: flex;
    flex-flow: wrap column;
    align-items: stretch;
    max-width: 200px;
}
</style>