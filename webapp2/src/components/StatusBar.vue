<template>
    
    <section class="status-bar">
        
        <div class="connection-status" :class="{ connected }">
            <span class="label special-font">{{ connected ? "verbunden" : "verbinden" }}</span>

            <icon class="icon" :name="connected ? 'cloud' : 'cloud_queue'"/>
        </div>
    </section>

</template>

<script>
import Icon from './Icon'

export default {
    
    components: { Icon },

    computed: {

        connected() {

            return this.$store.state.connected
        }
    }
}
</script>

<style lang="scss" scoped>
@import "~/assets/style/index.scss";

.status-bar {
    padding: 8px;
    display: flex;
    align-items: center;
    background: darken($background-color, 2%);
}

.connection-status {
    color: rgb(255, 201, 74);
    fill: currentColor;
    margin-left: auto;

    &.connected {
        color: $primary-color;
        fill: $primary-color;
    }
    
    .label {
        margin-right: 8px;
    }

    .icon {

    }
}
</style>