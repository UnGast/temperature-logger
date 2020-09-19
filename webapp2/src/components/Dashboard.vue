<template>

    <section class="dashboard">

        <status-bar/>

        <div class="body">

            <sensor-info/>

        </div>

    </section>

</template>

<script>
import StatusBar from './StatusBar'
import SensorInfo from './SensorInfo'

export default {
    
    components: { StatusBar, SensorInfo },
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