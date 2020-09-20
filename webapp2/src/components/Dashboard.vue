<template>

    <section class="dashboard">

        <status-bar/>

        <div class="body">

            <graph :sensorIds="[1, 2, 4]"/>

            <sensor-info/>

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
    //padding: 16px;
    display: flex;
    flex-direction: column;
    align-items: flex-start;

    .sensor-info {
        flex-basis: 20%;
        flex-grow: 0;
        margin-right: 48px;
    }

    .graph {
        align-self: stretch;
        height: 50vh;
        margin-bottom: 32px;
    }
}
</style>