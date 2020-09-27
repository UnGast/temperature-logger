<template>
  <input type="text" class="datetime-input" placeholder="tt.mm.jjjj hh::mm" :value="displayText"/>
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

.datetime-input {
  background: lighten($background-color, 15%);
  color: white;
  border: 0;
  padding: 8px;
  outline: 0;
  border: 1px solid darken($background-color, 10%);
  border-radius: 3px;
  background: radial-gradient(at center, change-color(lighten($background-color, 10%), $alpha: .5) 50%, change-color(darken($background-color, 4%), $alpha: .4) 100%),
    linear-gradient(to bottom, darken($background-color, 0%), lighten($background-color, 10%) 20%, lighten($background-color, 10%) 80%, darken($background-color, 0%) 100%);
}
</style>