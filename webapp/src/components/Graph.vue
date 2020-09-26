<template>
	<section class="graph">

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
							:key="line.id"
							transform="translate(10, 0)"
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
					<line x1="10" y1="0" x2="10" :y2="graphSize.height" :stroke-width="axisWidth" stroke="white"/>

					<line x1="7" :y1="label.y" x2="10" :y2="label.y" v-for="label in yAxisLabels" :key="label.text" stroke-width="0.25" stroke="white"/>

					<text v-for="label in yAxisLabels" :key="label" :x="0" :y="label.y" font-size="3" transform="translate(0, 1)" fill="white">{{ label.text }}</text>
				</svg>

				<svg x="0" :y="graphSize.height">
					<svg x="10">
						<line x1="0" y1="0" :x2="graphSize.width" y2="0" :stroke-width="axisWidth" stroke="white"/>
						
						<line :x1="label.x" :y1="0" :x2="label.x" :y2="3" v-for="label in xAxisLabels" :key="label.text" stroke-width="0.25" stroke="white"/>
					</svg>

					<text class="x-label" v-for="label in xAxisLabels" :key="label" text-anchor="middle" :x="label.x + 10" :y="7" font-size="3" fill="white">{{ label.text }}</text>			</svg>
			</svg>

			<div class="legend">
				<div
					v-for="line in lines"
					:key="line.id"
					class="line"
					:style="{ background: line.label.color }"
					@mouseenter="handleLineLegendEntryMouseEnter(line)"
					@mouseleave="handleLineLegendEntryMouseLeave(line)">

						<div class="info">
							<span class="label">{{ line.label.text }}</span>
						</div>
				</div>
			</div>
		</div>
	</section>
</template>

<script>
import chroma from 'chroma-js'

import variables from 'style'

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
	data: () => ({
		width: 200,
		height: 100,
		dataPointerPosition: { x: 0, y: 0 },
		showDataPointer: false,
		strokeWidth: 0.2,
		axisWidth: 0.5,
		visibleXLength: 100,
		dataAreaBackgroundColor: chroma(variables.backgroundColor).darken(0.2),
		highlightedLineId: null
	}),
	computed: {
		dataFeatures() {
			let features = {
				yMax: -1000,
				yMin: 10000,
				xMin: Number.MAX_VALUE,
				xMax: -Number.MAX_VALUE
			}

			for (let dataPointList of Object.values(this.data)) {
				for (let dataPoint of dataPointList) {
					if (dataPoint.y > features.yMax) {
						features.yMax = dataPoint.y
					}
					if (dataPoint.y < features.yMin) {
						features.yMin = dataPoint.y
					}
					if (dataPoint.x > features.xMax) {
						features.xMax = dataPoint.x
					}
					if (dataPoint.x < features.xMin) {
						features.xMin = dataPoint.x
					}
				}
			}

			return features
		},
		visibleArea() {
			var area = {
				xMin: this.dataFeatures.xMin - this.visibleXLength,
				xMax: this.dataFeatures.xMax,
				yMin: this.dataFeatures.yMin,
				yMax: this.dataFeatures.yMax
			}
			
			if (this.dataFeatures.xMax - this.dataFeatures.xMin < this.visibleXLength) {
				area.xMin = this.dataFeatures.xMin
				area.xMax = this.dataFeatures.xMin + this.visibleXLength
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

			for (let dataPointListId of Object.keys(this.data)) {

				let dataPointList = this.data[dataPointListId]

				let label = this.labels[dataPointListId]

				lines.push({
					id: dataPointListId,
					label,
					opacity: this.highlightedLineId && this.highlightedLineId !== dataPointListId ? 0.2 : 1,
					points: dataPointList.map(dataPoint => {
						return `${Math.floor(dataPoint.x - this.visibleArea.xMin) * this.graphScale.x},${Math.floor((dataPoint.y - this.visibleArea.yMin) * this.graphScale.y)}`
					}).join(' ')
				})
			}

			return lines
		},
		yAxisLabels() {

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
		xAxisLabels() {

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
		handleLineLegendEntryMouseEnter(line) {
			this.highlightedLineId = line.id
		},
		handleLineLegendEntryMouseLeave(line) {
			this.highlightedLineId = null
		},
		updateAspectRatio() {
			let bounds = this.$refs.graphic.getBoundingClientRect()
			let aspectRatio = bounds.width / bounds.height
			this.width = aspectRatio * this.height
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
	flex-direction: column;
	padding: 16px 16px 32px 16px;
}

.upper {
	display: flex;
	margin-bottom: 32px;
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
</style>