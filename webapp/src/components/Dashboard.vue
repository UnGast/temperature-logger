<template>

    <section class="dashboard">

        <status-bar/>

        <div class="body">

            <graph/>

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

    .sensor-info {
        flex-basis: 20%;
        flex-grow: 0;
    }

    .graph {
        align-self: stretch;
        margin-bottom: 1px;
    }
}
</style>