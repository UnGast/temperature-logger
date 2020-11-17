<template>
  <section class="dashboard-server-meta-section dashboard-section">
    <h1 class="heading">Server</h1>

    <template v-if="meta">
      <table v-if="meta.disc">
        <tbody>
          <tr class="meta-field">
            <td><label class="label">gesamter Speicher:</label></td>
            <td><span class="value">{{ totalSpace }}GiB</span></td>
          </tr>
          <tr class="meta-field">
            <td><label class="label">benutzer Speicher:</label></td>
            <td><span class="value">{{ usedSpace }}GiB</span></td>
          </tr>
          <tr class="meta-field">
            <td><label class="label">freier Speicher:</label></td>
            <td><span class="value">{{ freeSpace }}GiB</span></td>
          </tr>
        </tbody>
      </table>
    </template>

    <template v-else>
      <p class="dashboard-section-unavailable-message">noch keine Daten verfügbar</p>
    </template>
  </section>
</template>

<script>
export default {
  computed: {
    meta() {
      return this.$store.state.serverMeta
    },
    totalSpace() {
      return this.meta.disc.total / Math.pow(2, 30)
    },
    usedSpace() {
      return this.meta.disc.used / Math.pow(2, 30)
    },
    freeSpace() {
      return this.meta.disc.free / Math.pow(2, 30)
    }
  }
}
</script>

<style lang="scss" scoped>
@import 'style';

.dashboard-server-meta-section {
  padding: $dashboard-screen-spacing;
}

.meta-field {
  td {
    padding: 8px 0;
  }
  
  .label {
    font-weight: bold;
    text-transform: uppercase;
    margin-right: 8px;
  }
}
</style>