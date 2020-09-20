<template>
	<section class="graph">
		<svg :viewBox="`${0} ${dataFeatures.lowestValue} ${dataFeatures.highestTimestamp - dataFeatures.lowestTimestamp} ${dataFeatures.highestValue - dataFeatures.lowestValue}`" width="200" preserveAspectRatio="none">
			<polyline
				v-for="line in lines"
				:key="line.id"
				fill="none"
				stroke="#fff"
				stroke-width="1"
				:points="line.points"/>
		</svg>
	</section>
</template>

<script>
export default {
	props: {
		sensorIds: {
			type: Array,
			required: true
		}
	},
	computed: {
		sensorData() {
			var filtered = {}
			for (let sensorId of this.sensorIds) {
				if (this.$store.state.sensorData[sensorId]) {
					filtered[sensorId] = this.$store.state.sensorData[sensorId]
				}
			}
			return filtered
		},
		sensorInfo() {
			var filtered = {}
			for (let sensorId of this.sensorIds) {
				if (this.$store.state.sensorInfo[sensorId]) {
					filtered[sensorId] = this.$store.state.sensorInfo[sensorId]
				}
			}
			return filtered
		},
		dataFeatures() {
			var highestValue = -1000
			var lowestValue = 10000
			var lowestTimestamp = Number.MAX_VALUE
			var highestTimestamp = -Number.MAX_VALUE

			console.log("SENSOR DATA", this.sensorData)

			for (let timeValueList of Object.values(this.sensorData)) {

				for (let timeValue of timeValueList) {
					//console.log("value", timeValue)
					if (timeValue.value > highestValue) {
						highestValue = timeValue.value
					}
					if (timeValue.value < lowestValue) {
						lowestValue = timeValue.value
					}
					if (timeValue.timestamp > highestTimestamp) {
						highestTimestamp = timeValue.timestamp
					}
					if (timeValue.timestamp < lowestTimestamp) {
						lowestTimestamp = timeValue.timestamp
					}
				}
			}

			return {
				highestValue,
				lowestValue,
				lowestTimestamp,
				highestTimestamp
			}
		},
		lines() {
			var lines = []
			for (let sensorId of this.sensorIds) {
				let sensorData = this.sensorData[sensorId]

				if (!sensorData || sensorData.length === 0) {
					continue
				}
				
				var firstTimestamp = sensorData[0].timestamp

				lines.push({
					id: sensorId,
					points: this.sensorData[sensorId].map(timeValue => `${timeValue.timestamp - firstTimestamp},${timeValue.value}`).join(' ')
				})
			}
			return lines
		}
	}
}
</script>