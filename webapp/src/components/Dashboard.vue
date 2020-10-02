<template>

    <section class="dashboard">

        <status-bar/>

        <div class="body">

            <dashboard-graph/>

            <dashboard-sensor-info/>

        </div>

    </section>

</template>

<script>
import StatusBar from './StatusBar'
import DashboardSensorInfo from './DashboardSensorInfo'
import DashboardGraph from './DashboardGraph'

export default {
    
    components: { StatusBar, DashboardSensorInfo, DashboardGraph },
}
</script>

<style lang="scss" scoped>
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

.dashboard-graph {
    border-bottom: 1px solid lighten($background-color, 10%);
    padding-bottom: 64px;
}

.dashboard-sensor-info {
    padding-top: 48px;
}
</style>