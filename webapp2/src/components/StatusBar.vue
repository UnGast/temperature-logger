<template>
    
    <section class="status-bar">

        <span class="connected-label">{{ connected ? "verbunden" : "nicht verbunden" }}</span>
    </section>

</template>

<script>
export default {
    
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

    background: $background-color;
}
</style>