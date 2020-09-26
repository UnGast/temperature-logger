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
@import "style";

.status-bar {
    padding: 8px;
    display: flex;
    align-items: center;
    background: darken($background-color, 2%);
    border-bottom: 2px solid darken($background-color, 15%);
}

.connection-status {
    color: $accent-color; 
    fill: currentColor;
    margin-left: auto;

    .label {
        margin-right: 8px;
    }

    .icon {

    }
}
</style>