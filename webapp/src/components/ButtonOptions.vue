<template>
  <div class="button-options">
    <div class="buttons">
      <button class="button" v-for="option in options" :key="option.label" :class="{ selected: option.value === modelValue }" @click="selectOption(option)">{{ option.label }}</button>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    options: {
      type: Array,
      required: true
    },
    modelValue: {
      required: true
    }
  },
  methods: {
    selectOption(option) {
      this.$emit('update:modelValue', option.value)
    }
  }
}
</script>

<style lang="scss" scoped>
@import 'style';

.button-options {
  display: flex;
}

.buttons {
  border-radius: 3px;
  overflow: hidden;
  border: 1px solid darken($background-color, 10%);
}

.button {
  box-shadow: none;
  border-radius: 0;
  border: 0;
  border-right: 1px solid darken($background-color, 10%);

  &:last-child {
    border-right: 0;
  }

  &.selected {
    background: $background-color;
  }
}
</style>