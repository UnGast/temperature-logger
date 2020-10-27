<template>
  <div class="time-interval-input">
    <datetime-input class="start" v-model="start"/>
    <datetime-input class="end" v-model="end"/>
  </div>
</template>

<script>
import DatetimeInput from './DatetimeInput'

export default {
  components: { DatetimeInput },
  props: {
    modelValue: {
      type: Object,
      required: true
    }
  },
  computed: {
    start: {
      get() {
        return this.modelValue.start
      },
      set(newValue) {
        let updated = this.modelValue
        updated.start = newValue
        this.$emit('update:modelValue', updated)
      }
    },
    end: {
      get() {
        return this.modelValue.end
      },
      set(newValue) {
        let updated = this.modelValue
        updated.end = newValue
        this.$emit('update:modelValue', updated)
      }
    }
  }
}
</script>

<style lang="scss" scoped>
.start {
  margin-right: 16px;
}
</style>