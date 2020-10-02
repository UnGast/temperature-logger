<template>
  <input type="text" class="datetime-input text-input" placeholder="tt.mm.jjjj hh::mm" :value="displayText"/>
</template>

<script>
import { reactive, computed } from 'vue'
import { formatDatetime } from '~/data/date/format'

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

  },
  setup(props) {
    return {
      ...setupDisplayText(props.modelValue * 1000)
    }
  }
}

function setupDisplayText(initialValue) {
  
  const state = reactive({
    displayText: format(initialValue)
  })

  function format(value) {

    if (!value) {
      return ''
    } else {
      return formatDatetime(initialValue)
    }
  } 

  return { ...state }
}
</script>

<style lang="scss" scoped>
@import 'style';
</style>