<template>
  <i class="icon"><svg><use :xlink:href="'#icon-' + name"></use></svg></i>
</template>

<script>
export default {
  props: {
    name: String
  }
}
</script>

<style lang="scss" scoped>
.icon {
  width: 1em;
  height: 1em;
  vertical-align: middle;
}

svg {
  fill: inherit;
  width: inherit;
  height: inherit;
}
</style>