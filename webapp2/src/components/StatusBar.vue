<template>
    
    <section class="status-bar">

        <span class="connected-label special-font">{{ connected ? "verbunden" : "nicht verbunden" }}</span>

        <icon class="connected-icon" :name="connected ? 'link' : 'link_off'"/>
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
    background: darken($background-color, 10%);
}

.connected-label {
    color: $primary-color;
    margin-left: auto;
    margin-right: 8px;
}

.connected-icon {
    fill: $primary-color;
}
</style>