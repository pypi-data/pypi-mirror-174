<template>
    <div class="row mb-3">
        <div class="col">
            <h5> {{ id }}</h5>
            <Line :chart-options="chartOptions" :chart-data="chartData.value" />
        </div>
    </div>
</template>

<script setup>
import { computed, reactive, onMounted } from "vue";
import { useVSUIStore } from '@/stores/vsui_store.js';
import { Line } from 'vue-chartjs';
import {
    Chart as ChartJS,
    Title,
    Tooltip,
    Legend,
    LineElement,
    LinearScale,
    PointElement,
    CategoryScale,
} from 'chart.js'

ChartJS.register(
    Title,
    Tooltip,
    Legend,
    LineElement,
    LinearScale,
    PointElement,
    CategoryScale
)

const store = useVSUIStore();
const socket = store.socket;

const props = defineProps({
    id: String,
    task_id: String
})

const my_data = reactive({ value: { 'x': [], 'y': [] } })

const chartData = computed(() => {
    return {
        value: {
            labels: my_data.value.x,
            datasets: [
                {
                    label: "Training Loss",
                    backgroundColor: '#f87979',
                    data: my_data.value.y
                }
            ]
        }
    }
})

const chartOptions = {
    responsive: true,
    maintainAspectRatio: false
}

socket.on('chart_data_update', (data) => {
    if (props.task_id in data) {
        if (props.id in data[props.task_id]) {
            my_data.value = data[props.task_id][props.id]
        }
    }
})
onMounted(() => {
    socket.emit('request_update', { 'task_id': props.task_id, 'key': props.id })
})
</script>

<style scoped>

</style>