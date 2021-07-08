<template>
	<section class="dashboard-section-notification-configs dashboard-section">
		<div class="heading">
			<span>Benachrichtigungen</span>
		</div>

		<div class="content">
			<table class="config" v-for="config in configs" :key="config.type + config.threshold">
				<tr class="key-value-pair">
					<td><label class="label">type:</label></td>
					<td class="value-column"><span class="value">{{config.type}}</span></td></tr>
				<tr class="key-value-pair">
					<td><label class="label">threshold:</label></td>
					<td class="value-column"><span class="value">{{config.threshold}}</span></td>
				</tr>
			</table>
		</div>
	</section>
</template>

<script>
export default {
	computed: {
		configs() {
			return this.$store.state.notificationConfigs
		}
	},
}
</script>

<style lang="scss" scoped>
@import 'style';

.dashboard-section-notification-configs {
  padding: 32px;
}

.heading {
	margin-bottom: 32;
}

.config {
	background: $tile-background;
	padding: 16px;
	width: 100%;
	white-space: nowrap;
	border-radius: $tile-corner-radius;

	.label {
		display: block;
		padding: 4px 8px 4px 0;
		font-weight: bold;
		text-transform: uppercase;
	}

	.value-column {
		width: 100%;
	}
}
</style>