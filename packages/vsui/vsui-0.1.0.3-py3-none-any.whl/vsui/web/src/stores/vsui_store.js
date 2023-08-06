import {defineStore} from 'pinia';
import {ref} from 'vue';
import io from 'socket.io-client';

export const useVSUIStore = defineStore('vsui_store', () => {
  const socket = io({
    extraHeaders: {
      'type': 'web',
      'id': 'web'
    }
  })
  const working_directory = ref('/')
  function set_working_directory(dir) {
    working_directory.value = dir
    set_prev_file_browser_path(dir)
    socket.emit('web_working_dir', dir)
  }
  // the last location of the previous file browser location
  const prev_file_browser_path = ref('/')
  function set_prev_file_browser_path(dir) {
    prev_file_browser_path.value = dir
  }
  return { socket, working_directory, set_working_directory, prev_file_browser_path, set_prev_file_browser_path }
})