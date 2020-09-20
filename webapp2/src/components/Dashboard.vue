<template>

    <section class="dashboard">

        <status-bar/>

        <div class="body">

            <sensor-info/>

            <graph :sensorIds="[1, 2, 4]"/>

        </div>

    </section>

</template>

<script>
import StatusBar from './StatusBar'
import SensorInfo from './SensorInfo'
import Graph from './Graph'

export default {
    
    components: { StatusBar, SensorInfo, Graph },
}
</script>

<style lang="scss" scoped>
@import "~/assets/style/index.scss";

.dashboard {
    background: $background-color;
    color: white;
}

.body {
    padding: 16px;
    display: flex;
}
</style>