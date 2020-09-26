<template>
  <section class="dashboard-graph-card card">
    <h1 class="heading">Graph</h1>

		<div class="content">
      <graph :data="graphData" :labels="graphLabels"/>

      <div class="timeframe-setting">
        <label class="label">Zeitraum</label>

        <div class="options">
        
          <button class="option" :class="{ selected: selectedTimeframe === 'latest' }" @click="selectedTimeframe = 'latest'">Neue</button>

          <button class="option" :class="{ selected: selectedTimeframe === 'interval' }" @click="selectedTimeframe = 'interval'">Interval</button>

        </div>

        <div class="settings">

          <template v-if="selectedTimeframe === 'interval'">

            <date-time-input v-model="timeframeIntervalStart"/>
            
            <date-time-input v-model="timeframeIntervalEnd"/>

            <button class="fetch-timeframe-interval-button" @click="handleRequestFetchTimeframeIntervalData">Laden</button>
          </template>
          
        </div>
      </div>
    </div>
  </section>
</template>

<script>
import { reactive } from 'vue'
import Graph from './Graph'
import DateTimeInput from './DateTimeInput'

export default {
  components: { Graph, DateTimeInput },
  computed: {
		timeframeIntervalStart: {
			get() {
				return this.$store.state.timeframeSettings.interval.start
			},
			set(value) {
				this.$store.commit('setTimeframeIntervalStart', value)
			}
		},
		timeframeIntervalEnd: {
			get() {
				return this.$store.state.timeframeSettings.interval.end
			},
			set(value) {
				this.$store.commit('setTimeframeIntervalEnd', value)
			}
		},
		selectedTimeframe: {
			get()  {
				return this.$store.state.selectedTimeframe
			},
			set(value) {
				this.$store.commit('setSelectedTimeframe', value)
			}
    },
    selectedSensorIds() {
      return this.$store.state.selectedSensorIds
    },
    graphData() {
      let rawSensorData = this.$store.state.sensorData

      let graphData = {}

      for (let sensorId of this.selectedSensorIds) {
        graphData[sensorId] = []

        if (!rawSensorData[sensorId]) {
          continue
        }

        for (let timeValue of rawSensorData[sensorId]) {
          graphData[sensorId].push({
            x: timeValue.timestamp,
            y: timeValue.value
          })
        }
      }

      return graphData
    },
    graphLabels() {
      let rawSensorInfo = this.$store.state.sensorInfo

      let graphLabels = {}

      for (let sensorId of this.selectedSensorIds) {

        console.log("RAW SENSOR INFO IS", rawSensorInfo)
        console.log(sensorId)

        graphLabels[sensorId] = rawSensorInfo[sensorId].position
      }

      return graphLabels
    }
  },
  setup() {

  }
}
</script>