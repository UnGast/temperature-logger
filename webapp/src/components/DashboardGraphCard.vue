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

            <button @click="handleRequestDownloadTimeframeIntervalData">Herunterladen</button>
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

        graphLabels[sensorId] = {
          color: rawSensorInfo[sensorId].color,
          text: rawSensorInfo[sensorId].position
        }
      }

      return graphLabels
    }
  },
  methods: {
		handleRequestFetchTimeframeIntervalData() {
			this.$store.dispatch('fetchTimeframeIntervalData')
    },
    handleRequestDownloadTimeframeIntervalData() {
      this.$store.dispatch('downloadTimeframeIntervalData')
    }
  },
  setup() {

  }
}
</script>

<style lang="scss" scoped>
@import 'style';

.dashboard-graph-card {
	background: lighten($background-color, 5%);
}

.timeframe-setting {
	display: flex;
	flex-direction: column;
	
	.label {
		font-weight: bold;
		text-transform: uppercase;
		font-size: 1rem;
		margin-bottom: 16px;
	}
	
	.option {
		border: 0;
		background: white;
		margin-right: 1px;
		position: relative;
		outline: 0;
		cursor: pointer;
		transition: all .2s;
		text-transform: uppercase;
		font-size: .9rem;
		padding: 4px 8px;

		&:hover {
			border-radius: 5px;
			box-shadow: 0 0 0 1px $primary-color;
		}

		&.selected {
			background: darken($background-color, 10%);
			border-radius: 12px;
			color: white;
			box-shadow: 0 0 0 3px $primary-color;
			z-index: 1000;
		}
	}
}
</style>