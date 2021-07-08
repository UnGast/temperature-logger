<template>
    <section class="dashboard">
        <status-bar/>

        <div class="body">
            <dashboard-graph/>
            <dashboard-download-section/>
            <dashboard-sensor-info/>
            <dashboard-notification-configs-section/>
            <dashboard-server-meta-section/>
        </div>
    </section>
</template>

<script>
import StatusBar from './StatusBar'
import DashboardSensorInfo from './DashboardSensorInfo'
import DashboardNotificationConfigsSection from './DashboardNotificationConfigsSection.vue'
import DashboardGraph from './DashboardGraph'
import DashboardDownloadSection from './DashboardDownloadSection'
import DashboardServerMetaSection from './DashboardServerMetaSection'

export default {
    components: { StatusBar, DashboardSensorInfo, DashboardNotificationConfigsSection, DashboardGraph, DashboardDownloadSection, DashboardServerMetaSection },
}
</script>

<style lang="scss" s
        DashboardServerMetaSectioncoped>
@import "~/assets/style/index.scss";

.dashboard {
    background: $background-color;
    color: white;
}

.body {
    //padding: 16px;
    display: flex;
    flex-direction: column;
}

.dashboard-section {
    border-bottom: 1px solid lighten($background-color, 10%);

    &:last-child {
        border-bottom: 0;
    }
}

.dashboard-graph {
    padding-bottom: 64px;
}

.dashboard-download-section {
}

.dashboard-sensor-info {
    padding-top: 48px;
}
</style>