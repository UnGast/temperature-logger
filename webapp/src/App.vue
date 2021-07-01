<template>
  <section class="app">
    <div style="display:none" v-html="iconSvg"></div>
    <dashboard/>
  </section>
</template>

<script>
import iconSvg from '!raw-loader!~/assets/icons/icomoon/symbol-defs.svg'
import Dashboard from './components/Dashboard.vue'

export default {
  name: 'App',
  components: {
    Dashboard
  },
  computed: {
    iconSvg() {
      return iconSvg
    }
  }
}
</script>

<style lang="scss">
@import "~/assets/style/global/index.scss";
</style>

<style lang="scss" scoped>
.app {
  display: flex;
  flex-direction: column;
  height: 100vh;
}

.dashboard {
  flex-grow: 1;
}
</style>