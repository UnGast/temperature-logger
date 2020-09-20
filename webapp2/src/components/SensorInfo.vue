<template>
  
  <section class="sensor-info card">

    <div class="heading">

      <span>Sensoren</span>

    </div>

    <div class="content">

      <div class="sensor" v-for="sensor in sensorInfo" :key="sensor.id" @click="handleSensorClick(sensor)">

        <span class="name info">{{ sensor.name }}</span>

        <table class="meta-info">

          <tbody>

            <tr>
              <div class="field">
                
                <td><label class="label">Position:</label></td><td><span class="position info">{{ sensor.position }}</span></td>
                
              </div>
            </tr>

            <tr>
              <div class="field">

                <td><label class="label">ID:</label></td><td><span class="id info">{{ sensor.id }}</span></td>

              </div>
            </tr>

          </tbody>

        </table>

      </div>

    </div>

  </section>

</template>

<script>
export default {
  computed: {
    sensorInfo() {
      return this.$store.state.sensorInfo
    }
  },
  methods: {
    handleSensorClick(sensor) {
      this.$store.commit('setSensorSelected', sensor)
    }
  }
}
</script>

<style lang="scss" scoped>
@import 'style';

$sensor-info-background: lighten($background-color, 5%);

.card {
  padding: 16px;
  background: $sensor-info-background;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
}

.heading {
  margin-bottom: 32px;
  color: $primary-color;
}

.content {
  display: grid;
  grid-template-columns: 1fr 1fr;
}

.sensor {
  border: 1px solid white;
  border-radius: 5px;
  border-color: darken($sensor-info-background, 20%);
  margin: 0 16px 16px 0;
  padding: 16px;
  padding-top: 24px;
  position: relative;
  cursor: pointer;
  transition: background 0.2s;

  .name {
    position: absolute;
    top: 0;
    left: 8px;
    transform: translateY(-50%);
    background: $sensor-info-background;
    padding: 8px;
    font-family: $special-font-family;
    font-size: 1.2rem;
    border-radius: 5px;
  }

  .label {
    font-weight: bold;
    margin-right: 16px;
  }

  .meta-info {
    text-align: left;

    td {
      vertical-align: top;
    }

    .field {
      margin-bottom: 16px;

      &:last-child {
        margin-bottom: 0;
      }
    }
  }

  &:hover {
    background: lighten($sensor-info-background, 5%);
  }
}
</style>