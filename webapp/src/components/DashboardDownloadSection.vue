<template>
  <section class="dashboard-download-section dashboard-section">
    <h1 class="heading">Download</h1>
    
    <div class="sections">
      <section class="section interval">
        <label class="label">Interval</label>
        
        <time-interval-input v-model="interval"/>

        <button class="button" @click="handleDownloadIntervalRequest">Herunterladen</button>
      </section>

      <section class="section">
        <label class="label">Alle</label>

        <button class="button" @click="handleDownloadAllRequest">Alle herunterladen</button>
      </section>
    </div>
  </section>
</template>

<script>
import TimeIntervalInput from './TimeIntervalInput'

export default {
  components: { TimeIntervalInput },
  data() {
    return {
      interval: {
        start: Date.now() / 1000,
        end: Date.now() / 1000
      }
    }
  },
  methods: {
    handleDownloadIntervalRequest() {
      this.$store.dispatch('initiateIntervalContainingFilesDownload', this.interval)
    },
    handleDownloadAllRequest() {

    }
  }
}
</script>

<style lang="scss" scoped>
@import 'style';

.dashboard-download-section {
  padding: 32px;
}

.sections {
  display: flex;
  flex-wrap: wrap;

  .section {
    position: relative;
    padding: 16px;
    padding-top: 24px;
    display: flex;
    border: 2px solid darken($background-color, 20%);
    border-radius: 5px;
    margin-right: 32px;
    margin-bottom: 32px;

    .label {
      position: absolute;
      top: 0;
      left: 32px;
      transform: translateY(calc(-50% - .1em)); // -.1em for better optical center
      background: $background-color;
      padding: 0 8px;
      font-size: 1rem;
      text-transform: uppercase;
      font-weight: bold;
    }

    &.interval {
      .time-interval-input {
        margin-right: 16px;
      }
    }
  }
}
</style>