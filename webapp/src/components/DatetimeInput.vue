<template>
  <input type="text" class="datetime-input text-input" placeholder="tt.mm.jjjj hh::mm" :value="displayText" @input="handleInput"/>
</template>

<script>
import { reactive, computed, watchEffect } from 'vue'
import { formatDatetime, parseDatetime } from '~/data/date'

export default {
  props: {
    modelValue: {
      default: 0
    }
  },
  data: () => {
    return {
      //displayText: ''
    }
  },
  computed: {

  },
  methods: {
    handleInput(event) {
      console.log("INPUT", )
      this.displayText = event.target.value
      let parsed = parseDatetime(event.target.value)

      if (parsed instanceof Date) {
        console.log('IS DATETIME', parsed)
        this.$emit('update:modelValue', Math.floor(parsed.getTime() / 1000))
      }
    }
  },
  setup(props) {
    return {
      ...setupDisplayText(props)
    }
  }
}

function setupDisplayText(props) {
  
  const state = reactive({
    displayText: format(props.modelValue)
  })

  function format(value) {

    if (!value) {
      return ''
    } else {
      return formatDatetime(value * 1000)
    }
  }

  watchEffect(() => props.modelValue, () => {
    console.log("UPDATE POPRS", props.modelValue)
    state.displayText = format(props.modelValue)
  })

  return { ...state }
}
</script>

<style lang="scss" scoped>
@import 'style';
</style>