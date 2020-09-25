<template>
  <input type="text" class="date-time-input" placeholder="tt.mm.jjjj hh::mm" :value="displayText"/>
</template>

<script>
import { reactive, computed } from 'vue'
import { format as formatDate } from 'date-fns'

export default {
  props: {
    modelValue: {
      default: "WOW"
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
      ...setupDisplayText(props.modelValue)
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
      return formatDate(initialValue, 'dd/MM/yyyy HH:mm')
    }
  } 

  return { ...state }
}
</script>