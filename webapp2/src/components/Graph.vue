<template>
	<section class="graph card">

		<svg ref="graphic" class="graphic" :viewBox="`0 0 ${width} ${height}`" preserveAspectRatio="xMinYMin">

			<svg x="10" y="0" :width="graphSize.width" :height="graphSize.height" :viewBox="`${0} ${Math.floor(visibleArea.yMin) * graphScale.y - strokeWidth} ${(visibleXLength)} ${(visibleArea.yMax - visibleArea.yMin) * graphScale.y + 2 * strokeWidth}`" preserveAspectRatio="xMinYMin">
				<polyline
					v-for="line in lines"
					:key="line.sensorId"
					transform="translate(10, 0)"
					fill="none"
					:stroke="line.color"
					:stroke-width="strokeWidth"
					:points="line.points"/>
			</svg>

			<svg>
				<line x1="10" y1="0" x2="10" :y2="graphSize.height + 10" stroke-width="1" stroke="white"/>

				<line x1="7" :y1="label.y" x2="10" :y2="label.y" v-for="label in yLabels" :key="label.text" stroke-width="0.25" stroke="white"/>

				<text v-for="label in yLabels" :key="label" :x="0" :y="label.y" font-size="3" transform="translate(0, 1)" fill="white">{{ label.text }}</text>
			</svg>

			<svg x="0" :y="graphSize.height + 10">
				<svg x="10">
					<line x1="0" y1="0" :x2="graphSize.width" y2="0" stroke-width="1" stroke="white"/>
					
					<line :x1="label.x" :y1="0" :x2="label.x" :y2="7" v-for="label in xLabels" :key="label.text" stroke-width="0.25" stroke="white"/>
				</svg>

				<text class="x-label" v-for="label in xLabels" :key="label" text-anchor="middle" :x="label.x + 10" :y="10" font-size="3" fill="white">{{ label.text }}</text>			</svg>

		</svg>
	</section>
</template>

<script>
import chroma from 'chroma-js'

export default {
	props: {
		sensorIds: {
			type: Array,
			required: true
		}
	},
	data: () => ({
		width: 200,
		height: 100,
		strokeWidth: 0.5,
		visibleXLength: 100,
		colorScale: chroma.scale(['yellow', 'green', 'lightblue', 'orange']).mode('lch')
	}),
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
		visibleArea() {
			return {
				xMin: this.dataFeatures.highestTimestamp - this.visibleXLength,
				xMax: this.dataFeatures.highestTimestamp,
				yMin: this.dataFeatures.lowestValue,
				yMax: this.dataFeatures.highestValue
			}
		},
		graphSize() {
			return {
				width: this.width - 30,
				height: this.height - 30
			}
		},
		graphScale() {
			return {
				x: this.graphSize.width / (this.visibleArea.xMax - this.visibleArea.xMin),
				y: this.graphSize.height / (this.visibleArea.yMax - this.visibleArea.yMin)
			}
		},
		lines() {
			var lines = []

			let colors = this.colorScale.colors(this.sensorIds.length)

			for (var i = 0; i < this.sensorIds.length; i++) {

				let sensorId = this.sensorIds[i]
				
				let sensorData = this.sensorData[sensorId]

				if (!sensorData || sensorData.length === 0) {
					continue
				}

				lines.push({
					sensorId: sensorId,
					color: colors[i],
					points: this.sensorData[sensorId].map(timeValue => `${Math.floor(timeValue.timestamp - this.visibleArea.xMin) * this.graphScale.x},${Math.floor(timeValue.value * this.graphScale.y)}`).join(' ')
				})
			}

			return lines
		},
		yLabels() {
			var labels = []

			var visibleAxisLength = this.visibleArea.yMax - this.visibleArea.yMin

			var labelCount = 10

			var stepSize = Math.floor(visibleAxisLength / labelCount)

			var startValue = Math.floor(this.visibleArea.yMin)

			for (var i = 0; i < labelCount; i++) {
				let value = startValue + i * stepSize

				labels.push({
					text: value,
					y: this.graphSize.height - i * stepSize * this.graphScale.y
				})
			}
			
			return labels
		},
		xLabels() {

			var labels = []

			var visibleAxisLength = this.visibleArea.xMax - this.visibleArea.xMin
			
			var labelCount = 4

			var stepSize = visibleAxisLength / labelCount

			var startValue = this.visibleArea.xMin

			for (var i = 0; i < labelCount; i++) {

				let value = startValue + i * stepSize

				let date = new Date(0)
				date.setUTCSeconds(value)

				labels.push({
					text: date.toLocaleTimeString(),
					x: i * stepSize * this.graphScale.x
				})
			}
			
			return labels
		}
	},
	mounted() {
		let bounds = this.$refs.graphic.getBoundingClientRect()
		let aspectRatio = bounds.width / bounds.height
		this.width = aspectRatio * this.height
	}
}
</script>

<style lang="scss" scoped>
@import 'style';

.graph {
	display: flex;
	background: lighten($background-color, 5%);
	padding: 16px;

	.graphic {
		flex-grow: 1;
		max-height: 100%;
	}
}
</style>