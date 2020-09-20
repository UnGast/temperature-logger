<template>
	<section class="graph card">

		<h1 class="heading">Graph</h1>

		<div class="content">

			<template v-if="sensorIds.length === 0">

				<span class="no-sensor-selected-info">kein Sensor ausgewählt</span>

			</template>

			<template v-else>

				<div class="upper">

					<svg ref="graphic" class="graphic" :viewBox="`0 0 ${width} ${height}`" preserveAspectRatio="xMinYMin">

						<svg
							ref="dataArea"
							@mouseenter="handleDataAreaMouseEnter"
							@mousemove="handleDataAreaMouseMove"
							@mouseleave="handleDataAreaMouseLeave"
							pointer-events="bounding-box"
							x="10"
							y="0"
							:width="graphSize.width"
							:height="graphSize.height"
							:viewBox="`${0} ${Math.floor(0) - strokeWidth} ${(visibleXLength)} ${(visibleArea.yMax - visibleArea.yMin) * graphScale.y + strokeWidth}`"
							preserveAspectRatio="xMinYMin">

								<rect :width="graphSize.width" :height="graphSize.height" :fill="dataAreaBackgroundColor"/>

								<polyline
									v-for="line in lines"
									:key="line.sensorId"
									transform="translate(10, 0)"
									:opacity="line.opacity"
									fill="none"
									:stroke="line.color"
									:stroke-width="strokeWidth"
									:points="line.points"/>

								<template v-if="showDataPointer">
									<line
										:x1="dataPointerPosition.x" y1="0" :x2="dataPointerPosition.x" :y2="graphSize.height" stroke="white" stroke-width="0.25" stroke-dasharray="1 2" stroke-style="dotted"/>
									
									<line
										:x1="0" :y1="dataPointerPosition.y" :x2="graphSize.width" :y2="dataPointerPosition.y" stroke="white" stroke-width="0.25" stroke-dasharray="1 2" stroke-style="dotted"/>
								</template>
						</svg>

						<svg>
							<line x1="10" y1="0" x2="10" :y2="graphSize.height" :stroke-width="axisWidth" stroke="white"/>

							<line x1="7" :y1="label.y" x2="10" :y2="label.y" v-for="label in yLabels" :key="label.text" stroke-width="0.25" stroke="white"/>

							<text v-for="label in yLabels" :key="label" :x="0" :y="label.y" font-size="3" transform="translate(0, 1)" fill="white">{{ label.text }}</text>
						</svg>

						<svg x="0" :y="graphSize.height">
							<svg x="10">
								<line x1="0" y1="0" :x2="graphSize.width" y2="0" :stroke-width="axisWidth" stroke="white"/>
								
								<line :x1="label.x" :y1="0" :x2="label.x" :y2="3" v-for="label in xLabels" :key="label.text" stroke-width="0.25" stroke="white"/>
							</svg>

							<text class="x-label" v-for="label in xLabels" :key="label" text-anchor="middle" :x="label.x + 10" :y="7" font-size="3" fill="white">{{ label.text }}</text>			</svg>
					</svg>

					<div class="legend">
						<div
							v-for="line in lines"
							:key="line.sensorId"
							class="line"
							:style="{ background: line.color }"
							@mouseenter="handleLineLegendEntryMouseEnter(line)"
							@mouseleave="handleLineLegendEntryMouseLeave(line)">

								<div class="info">
									<span class="sensor-name">{{ sensorInfo[line.sensorId].name }}: </span>
									<span class="sensor-position">{{ sensorInfo[line.sensorId].position }}</span>
								</div>

								<icon class="deselect-action" name="clear" @click="handleDeselectSensorRequest(line.sensorId)"/>
						</div>
					</div>
				</div>

				<div class="lower">
					<div class="timeframe-setting">
						<label class="label">Zeitraum</label>

						<div class="options">
						
							<button class="option" :class="{ selected: timeframe === 'latest' }" @click="timeframe = 'latest'">Neue</button>

							<button class="option" :class="{ selected: timeframe === 'interval' }" @click="timeframe = 'interval'">Interval</button>

						</div>

						<div class="settings">

							<template v-if="timeframe === 'interval'">
								<date-time-input :value="new Date()"/>
							</template>
							
						</div>
					</div>
				</div>
			</template>
		</div>
	</section>
</template>

<script>
import chroma from 'chroma-js'

import variables from 'style'
import Icon from './Icon'
import DateTimeInput from './DateTimeInput'

export default {
	components: { Icon, DateTimeInput },
	data: () => ({
		width: 200,
		height: 100,
		dataPointerPosition: { x: 0, y: 0 },
		showDataPointer: false,
		strokeWidth: 0.2,
		axisWidth: 0.5,
		visibleXLength: 100,
		dataAreaBackgroundColor: chroma(variables.backgroundColor).darken(0.2),
		highlightedSensorId: null,
		timeframe: 'latest',
		timeframeSettings: {
			interval: [0, 0]
		}
	}),
	computed: {
		sensorIds() {
			return Array.from(this.$store.state.selectedSensorIds)
		},
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
			var area = {
				xMin: this.dataFeatures.highestTimestamp - this.visibleXLength,
				xMax: this.dataFeatures.highestTimestamp,
				yMin: this.dataFeatures.lowestValue,
				yMax: this.dataFeatures.highestValue
			} 
			
			if (this.dataFeatures.highestTimestamp - this.dataFeatures.lowestTimestamp < this.visibleXLength) {
				area.xMin = this.dataFeatures.lowestTimestamp
				area.xMax = this.dataFeatures.lowestTimestamp + this.visibleXLength
			}

			return area
		},
		graphSize() {
			return {
				width: this.width - 10,
				height: this.height - 10
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

			for (var i = 0; i < this.sensorIds.length; i++) {

				let sensorId = this.sensorIds[i]
				
				let sensorData = this.sensorData[sensorId]

				let sensorInfo = this.sensorInfo[sensorId]

				if (!sensorData || sensorData.length === 0) {
					continue
				}

				lines.push({
					sensorId: sensorId,
					color: sensorInfo.color,
					opacity: this.highlightedSensorId && this.highlightedSensorId !== sensorId ? 0.2 : 1,
					points: this.sensorData[sensorId].map(timeValue => {
						return `${Math.floor(timeValue.timestamp - this.visibleArea.xMin) * this.graphScale.x},${Math.floor((timeValue.value - this.visibleArea.yMin) * this.graphScale.y)}`
					}).join(' ')
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
	methods: {
		handleDataAreaMouseEnter() {
			this.showDataPointer = true
		},
		handleDataAreaMouseMove(event) {
			let dataAreaBounds = this.$refs.dataArea.getBoundingClientRect()
			
			var dataAreaPosition = this.$refs.dataArea.createSVGPoint()
			dataAreaPosition.x = event.clientX
			dataAreaPosition.y = event.clientY
			dataAreaPosition = dataAreaPosition.matrixTransform(this.$refs.dataArea.getScreenCTM().inverse())

			this.dataPointerPosition = dataAreaPosition
		},
		handleDataAreaMouseLeave() {
			this.showDataPointer = false
		},
		handleDeselectSensorRequest(sensorId) {
			this.$store.commit('setSensorUnselected', sensorId)
		},
		handleLineLegendEntryMouseEnter(line) {
			this.highlightedSensorId = line.sensorId
		},
		handleLineLegendEntryMouseLeave(line) {
			this.highlightedSensorId = null
		},
		updateAspectRatio() {
			let bounds = this.$refs.graphic.getBoundingClientRect()
			let aspectRatio = bounds.width / bounds.height
			this.width = aspectRatio * this.height
		}
	},
	mounted() {
		this.updateAspectRatio()
		window.addEventListener('resize', () => {
			this.updateAspectRatio()
		})
	}
}
</script>

<style lang="scss" scoped>
@import 'style';

.graph {
	display: flex;
	flex-direction: column;
	background: lighten($background-color, 5%);
	padding: 16px 16px 32px 16px;
}

.heading {
	text-align: left;
}

.content {
	display: flex;
	flex-direction: column;
}

.upper {
	display: flex;
	margin-bottom: 32px;
}

.no-sensor-selected-info {
	font-size: 1.2rem;
	font-weight: bold;
	width: 100%;
	text-align: center;
	opacity: .7;
	color: white;
	margin: 48px 0;
}

.graphic {
	flex-grow: 1;
	max-height: 100%;
	margin-right: 32px;
}

.legend {
	display: flex;
	flex-direction: column;

	.line {
		margin-bottom: 8px;
		padding: 8px;
		border-radius: 5px;
		max-width: 100px;
		font-size: .8rem;
		color: black;
		display: flex;
		align-items: center;

		.info {
			margin-right: 8px;
		}

		.deselect-action {
			transition: background .2s;
			border-radius: 10000px;
			padding: 4px;
			cursor: pointer;

			&:hover {
				background: rgba(0,0,0,.1);
			}
		}
	}
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