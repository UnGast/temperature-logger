<template>
  <section class="graph">
    <canvas ref="canvas"/>
  </section>
</template>

<script>
import Chart from 'chart.js'

export default {
  props: {
    data: {
			type: Object,
			required: true
		},
		labels: {
			type: Object,
			required: true
		},
		initialVisibleArea: {
			type: Object,
			default: null
		}
  },
  watch: {
    data() {
      if (this.chart) {
        this.$nextTick(() => {
          if (this.chart.data.datasets.length < Object.values(this.data).length) {
            this.chart.data.datasets = this.buildDatasetsConfig()
          } else {
            Object.values(this.preparedData).forEach((values, index) => {
              this.chart.data.datasets[index].data = values
            })
          }
          this.chart.update()
        })
      }
    }
  },
  computed: {
    preparedData() {
      return Object.entries(this.data).reduce((result, [sensorId, values]) => {
        result[sensorId] = values.map(value => ({ x: value.x * 1000, y: value.y }))
        return result
      }, {})
    }
  },
  methods: {
    buildDatasetsConfig() {
      return Object.entries(this.preparedData).map(([sensorId, values]) => ({
        data: values,
        label: this.$store.state.sensorInfo[sensorId].type + ': ' + this.$store.state.sensorInfo[sensorId].position,
        borderColor: this.$store.state.sensorInfo[sensorId].color,
        fill: false
      }))
    }
  },
  mounted() {
    this.chart = new Chart(this.$refs.canvas, {
      type: 'line',
      data: {
        datasets: this.buildDatasetsConfig()
      },
      options: {
        scales: {
          xAxes: [{
            show: false,
            type: 'time',
            time: { unit: 'day' },
            position: 'bottom'
          }]
        }
      }
    })
  }
}
</script>