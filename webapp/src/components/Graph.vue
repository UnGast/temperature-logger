<template>
	<section class="graph">

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
				:viewBox="`0 0 ${graphSize.width} ${graphSize.height}`"
				preserveAspectRatio="none">

					<rect :width="graphSize.width" :height="graphSize.height" :fill="dataAreaBackgroundColor"/>

					<polyline
						v-for="line in lines"
						:key="line.id"
						:opacity="line.opacity"
						fill="none"
						:stroke="line.label.color"
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
				<line :x1="tickFontSize" y1="0" :x2="tickFontSize" :y2="graphSize.height" :stroke-width="axisWidth" :stroke="axisColor"/>

				<line x1="7" :y1="label.y" x2="10" :y2="label.y" v-for="label in yAxisTicks" :key="label.text" stroke-width="0.25" :stroke="axisColor"/>

				<text v-for="label in yAxisTicks" :key="label" :x="0" :y="label.y" :font-size="tickFontSize" transform="translate(0, 1)" :fill="axisColor">{{ label.text }}</text>
				
				<text v-if="showDataPointer" :x="0" :y="dataPointerTicks.y.y" :font-size="tickFontSize" transform="translate(0, 1)" :fill="axisColor">{{ dataPointerTicks.y.text }}</text>
			</svg>

			<svg x="0" :y="graphSize.height">
				<svg :x="tickFontSize">
					<line x1="0" y1="0" :x2="graphSize.width" y2="0" :stroke-width="axisWidth" :stroke="axisColor"/>
					
					<line :x1="label.x" :y1="0" :x2="label.x" :y2="3" v-for="label in xAxisTicks" :key="label.text" stroke-width="0.25" :stroke="axisColor"/>
				</svg>

				<!-- need to place this outside of <svg x="10"> to avoid cutting off the first label on the left side -->
				<text class="x-label" v-for="label in xAxisTicks" :key="label" text-anchor="middle" :x="label.x + tickFontSize" :y="tickFontSize" :font-size="tickFontSize" :fill="axisColor">{{ label.text }}</text>

				<foreignObject v-if="showDataPointer" :x="dataPointerTicks.x.x + 10" y="0" :width="graphSize.width" :height="graphSize.height">
					<span class="x-label" :style="{ background: 'red', color: 'white', fontSize: tickFontSize + 'px' }">WOW {{ dataPointerTicks.x.text }}</span>
				</foreignObject>
			</svg>
		</svg>

		<div class="legend">
			<div
				v-for="line in lines"
				:key="line.id"
				class="line"
				:style="{ color: line.label.color }"
				@mouseenter="handleLineLegendEntryMouseEnter(line)"
				@mouseleave="handleLineLegendEntryMouseLeave(line)">

					<div class="info">
						<span class="label">{{ line.label.text }}</span>
					</div>
			</div>
		</div>
	</section>
</template>

<script>
import chroma from 'chroma-js'
import { firstSignificantIndex, roundToSignificant } from '@/lib/utils/numbers'

import variables from 'style'

import GraphDataManager from '~/data/graph/GraphDataManager'
import { sign } from 'crypto'

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
	data() {
		return {
			width: 200,
			height: 100,
			tickFontSize: 16,
			dataPointerPosition: { x: 0, y: 0 },
			showDataPointer: false,
			strokeWidth: 0.2,
			axisWidth: 0.5,
			dataAreaBackgroundColor: chroma(variables.backgroundColor).darken(0.2),
			axisColor: chroma(variables.backgroundColor).brighten(3),
			highlightedLineId: null,
			dataManager: new GraphDataManager(this.data)
		}
	},
	computed: {
		dataBounds() {
			return this.dataManager.dataBounds
		},
		visibleArea() {
			var xMin = this.initialVisibleArea?.xMin || this.dataBounds.xMin
			var xMax = this.initialVisibleArea?.xMax || this.dataBounds.xMax
			var bounds = this.dataManager.getDataBoundsBetween(xMin, xMax)
			var area = Object.assign({}, bounds, this.initialVisibleArea)
			return area
		},
		graphSize() {
			return {
				width: this.width - this.tickFontSize,
				height: this.height - this.tickFontSize
			}
		},
		graphScale() {
			let dataXLength = Math.max(1, this.visibleArea.xMax - this.visibleArea.xMin)
			let dataYLength = Math.max(1, this.visibleArea.yMax - this.visibleArea.yMin)
			return {
				x: this.graphSize.width / dataXLength,
				y: this.graphSize.height / dataYLength
			}
		},
		maxVisiblePoints() {
			return this.$refs.dataArea ? this.$refs.dataArea.getBoundingClientRect().width / 5 : 100
		},
		lines() {
			let lines = []

			for (let dataPointListId of Object.keys(this.data)) {
				let dataPointList = this.data[dataPointListId]
				let sampledDataPoints = []
				let sampleStartIndex = null
				let sampleEndIndex = null

				for (let i = 0; i < dataPointList.length; i++) {
					let dataPoint = dataPointList[i]
					if (sampleStartIndex === null && dataPoint.x >= this.visibleArea.xMin) {
						sampleStartIndex = Math.max(0, i - 1)
					} else if (sampleEndIndex === null && dataPoint.x >= this.visibleArea.xMax) {
						sampleEndIndex = i
						break
					}
				}

				if (sampleStartIndex === null) {
					sampleStartIndex = dataPointList.length - 1
				}

				if (sampleEndIndex === null) {
					sampleEndIndex = dataPointList.length - 1
				}

				var maxSampleCount = sampleEndIndex - sampleStartIndex
				var stepSize = 0

				if (maxSampleCount <= this.maxVisiblePoints) {
					stepSize = 1
				} else {
					stepSize = maxSampleCount / this.maxVisiblePoints
				}

				for (let i = Math.max(0, sampleStartIndex); i <= sampleEndIndex; i += stepSize) {
					var flooredIndex = Math.floor(i)
					var dataPoint = dataPointList[flooredIndex]
					sampledDataPoints.push(dataPoint)
				}

				let label = this.labels[dataPointListId]

				lines.push({
					id: dataPointListId,
					label,
					opacity: this.highlightedLineId && this.highlightedLineId !== dataPointListId ? 0.2 : 1,
					points: sampledDataPoints.map(dataPoint => {
						return `${Math.floor(dataPoint.x - this.visibleArea.xMin) * this.graphScale.x},${Math.floor((dataPoint.y - this.visibleArea.yMin) * this.graphScale.y)}`
					}).join(' ')
				})
			}

			return lines
		},
		yAxisTicks() {
			var labels = []
			var visibleAxisLength = this.visibleArea.yMax - this.visibleArea.yMin
			var targetLabelCount = 10
			var stepSize = visibleAxisLength / targetLabelCount
			var significant = firstSignificantIndex(stepSize)
			stepSize = roundToSignificant(stepSize, significant)
			// apply the min with some value to prevent a following never ending loop when generating the labels
			var labelCount = Math.min(targetLabelCount * 2, Math.round(visibleAxisLength / stepSize))
			var startValue = Math.floor(this.visibleArea.yMin)

			for (var i = 0; i < labelCount; i++) {
				let value = startValue + i * stepSize
				labels.push({
					text: value.toPrecision(1),
					y: this.graphSize.height - i * stepSize * this.graphScale.y
				})
			}
			
			return labels
		},
		xAxisTicks() {
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
		},
		dataPointerTicks() {
			return {
				x: {
					text: "wow",
					x: 23
				},
				y: {
					text: "wow",
					y: 223
				}
			}
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
		handleLineLegendEntryMouseEnter(line) {
			this.highlightedLineId = line.id
		},
		handleLineLegendEntryMouseLeave(line) {
			this.highlightedLineId = null
		},
		updateAspectRatio() {
			let bounds = this.$refs.graphic.getBoundingClientRect()
			let aspectRatio = bounds.width / bounds.height
			this.width = bounds.width // aspectRatio * this.height
			this.height = bounds.height
		}
	},
	watch: {
		data() {
			this.dataManager.data = this.data
		}
	},
	mounted() {
		this.updateAspectRatio()
		window.addEventListener('resize', this.updateAspectRatio)
	},
	unmounted() {
		window.removeEventListener('resize', this.updateAspectRatio)
	}
}
</script>

<style lang="scss" scoped>
@import 'style';

.graph {
	display: flex;
}

.graphic {
	max-height: 100%;
	margin-right: 16px;
	flex-grow: 1;
}

.legend {
	display: flex;
	flex-direction: column;
	background: darken($background-color, 3%);
	border-radius: 5px;
	align-self: flex-start;

	.line {
		padding: 12px;
		max-width: 100px;
		font-size: .8rem;
		font-weight: bold;
		display: flex;
		align-items: center;
		border-bottom: 1px solid lighten($background-color, 10%);

		&:last-child {
			border-bottom: 0;
		}

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
</style>