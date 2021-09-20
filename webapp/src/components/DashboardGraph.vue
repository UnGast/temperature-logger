<template>
  <section class="dashboard-graph dashboard-section">
    <h1 class="heading">Graph</h1>
		<div class="content">
      <graph :visibleArea="graphVisibleArea" :data="graphData" :labels="graphLabels"/>
      <!--<div class="timeframe-selection">
        <label class="label">Zeitraum</label>
        <button-options class="options" :options="[ { label: 'Neueste', value: 'latest' }, { label: 'Intervall', value: 'interval' } ]" v-model="selectedTimeframe"/>
        <div class="settings">
          <template v-if="selectedTimeframe === 'interval'">
            <datetime-input v-model="timeframeIntervalStart"/>
            <datetime-input v-model="timeframeIntervalEnd"/>
            <button class="fetch-timeframe-interval-button button" @click="handleRequestFetchTimeframeIntervalData">Anzeigen</button>
          </template>
        </div>
      </div>-->
    </div>
  </section>
</template>

<script>
//import { reactive } from 'vue'
import Graph from './Graph'
//import DatetimeInput from './DatetimeInput'
import SensorDataManager from '~/data/sensor/SensorDataManager'
//import ButtonOptions from './ButtonOptions'

export default {
  components: { Graph },
  computed: {
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
    graphVisibleArea() {
      if (this.selectedTimeframe === 'latest') {
        let latestTimestamp = SensorDataManager.getLatestTimestamp(this.$store.state.sensorData)

        return {
          xMin: latestTimestamp - this.$store.state.timeframeSettings.latest,
          xMax: latestTimestamp
        }
      } else if (this.selectedTimeframe === 'interval') {
        return {
          xMin: this.$store.state.timeframeSettings.interval.start,
          xMax: this.$store.state.timeframeSettings.interval.end
        }
      } else {
        return null
      }
    },
    graphLabels() {
      let rawSensorInfo = this.$store.state.sensorInfo

      let graphLabels = {}

      for (let sensorId of this.selectedSensorIds) {

        graphLabels[sensorId] = {
          color: rawSensorInfo[sensorId].color,
          text: rawSensorInfo[sensorId].type + ', ' + rawSensorInfo[sensorId].position
        }
      }

      return graphLabels
    }
  },
  methods: {
    updateStoreTimeframeInterval() {
      this.$store.commit('setTimeframeIntervalStart', this.timeframeIntervalStart)
      this.$store.commit('setTimeframeIntervalEnd', this.timeframeIntervalEnd)
    },
		handleRequestFetchTimeframeIntervalData() {
      this.updateStoreTimeframeInterval()
			this.$store.dispatch('fetchTimeframeIntervalData')
    }
  },
  watch: {
    '$store.state.timeframeSettings.interval.start'() {
      this.timeframeIntervalStart = this.$store.state.timeframeSettings.interval.start
    },
    '$store.state.timeframeSettings.interval.end'() {
      this.timeframeIntervalEnd = this.$store.state.timeframeSettings.interval.end
    }
  },
  setup() {

  }
}
</script>

<style lang="scss" scoped>
@import 'style';

.dashboard-graph {
  padding: 32px;
  display: flex;
  flex-direction: column;

  .heading {
    margin-bottom: 24px;
  }
}

.graph {
  margin-bottom: 48px;
}

.timeframe-selection {
	display: flex;
  flex-direction: column;
  align-items: flex-start;
	
	.label {
		font-weight: bold;
		text-transform: uppercase;
		font-size: 1rem;
    margin-bottom: 24px;
    color: $muted-foreground-color;
	}
	
	.options {
    margin-bottom: 16px;
  }

  .settings {
    margin-right: -16px;
    margin-bottom: -16px;
    
    > * {
      margin-right: 16px;
      margin-bottom: 16px;
    }
  }
}
</style>