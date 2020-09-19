<template>
	<section class="graph">
		{{ sensorData }}
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
			this.$store.state.
		}
	}
}
</script>