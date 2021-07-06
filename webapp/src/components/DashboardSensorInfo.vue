<template>
  <section class="dashboard-sensor-info dashboard-section">
    <div class="heading">
      <span>Sensoren</span>
    </div>

    <div class="content">
      <div class="sensor" v-for="sensor in Object.values(sensorInfo)" :key="sensor.id" @click="handleSensorClick(sensor)">
        <div class="content-wrapper">
          <span class="type info" :style="{ color: sensor.color }">{{ sensor.type }}</span>

          <table class="meta-info">
            <tbody>
              <tr class="field">
                <td><label class="label">ID:</label></td><td><span class="info">{{ sensor.id }}</span></td>
              </tr>

              <tr class="field">
                <td><label class="label">Position:</label></td><td><span class="info">{{ sensor.position }}</span></td>
              </tr>

              <tr class="field">
                <td><label class="label">Wert:</label></td><td><span class="info">{{ getLatestSensorValue(sensor) }}</span></td>
              </tr>

              <tr class="field">
                <td><label class="label">Genauigkeit:</label></td><td><span class="info">± {{ sensor.accuracy }}</span></td>
              </tr>

              <tr class="field">
                <td><label class="label">Korrektur Offset:</label></td><td><span class="info">{{ sensor.correction_offset }}</span></td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </section>
</template>

<script>
export default {
  computed: {
    sensorInfo() {
      return this.$store.state.sensorInfo
    },
    sensorData() {
      return this.$store.state.sensorData
    }
  },
  methods: {
    handleSensorClick(sensor) {
      this.$store.commit('setSensorSelected', sensor.id)
    },
    getLatestSensorValue(sensor) {
      if (this.sensorData[sensor.id]) {
        return this.sensorData[sensor.id].slice(-1)[0].value
      } else {
        return undefined
      }
    }
  }
}
</script>

<style lang="scss" scoped>
@import 'style';

$sensor-background: darken($background-color, 3%);

.dashboard-sensor-info {
  padding: 32px;
  background: $background-color;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
}

.heading {
  margin-bottom: 64px;
  color: $primary-color;
}

.content {
  //display: grid;
  //grid-template-columns: 1fr 1fr;
  display: flex;
  flex-wrap: wrap;
}

.sensor {
  margin: 0 16px 32px 0;
  padding-top: 16px;

  .content-wrapper {
    position: relative;
    padding: 16px;
    padding-top: 24px;
    //border: 1px solid $sensor-border;
    border-radius: 5px;
    transition: background 0.2s;
    background: $sensor-background;
  }

  .type {
    position: absolute;
    top: 0;
    left: 16px;
    transform: translateY(-50%);
    background: $sensor-background;
    padding: 8px 12px;
    font-size: 1rem;
    text-transform: uppercase;
    font-weight: bold;
    border-radius: 5px;
    //border: 1px solid darken($background-color, 20%);
  }

  .meta-info {
    text-align: left;

    td {
      vertical-align: top;
      padding: 8px 0;
    }

    .label {
      font-weight: bold;
      margin-right: 16px;
      text-transform: uppercase;
    }
  }
}
</style>