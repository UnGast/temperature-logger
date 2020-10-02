<template>
    
    <section class="status-bar">
        
        <div class="connection-setup">
            
            <!--<label class="label">Verbinden mit</label>-->

            <input type="text" class="text-input small" size="12" placeholder="Host" title="z.B. localhost, 127.0.0.1" v-model="serverHost"/>
            
            <input type="text" class="text-input small" size="5" placeholder="Port" title="z.B. 8080" v-model="serverPort"/>

            <button class="button small" @click="handleConnectRequest">verbinden</button>

        </div>

        <div class="connection-status" :class="{ connected }">

            <span class="status special-font">{{ connected ? "verbunden" : "verbindet" }}</span>

            <icon class="icon" :name="connected ? 'cloud' : 'cloud_queue'"/>
        </div>
    </section>

</template>

<script>
import Icon from './Icon'

export default {
    
    components: { Icon },

    computed: {

        connected() {

            return this.$store.state.connected
        },

        serverHost: {

            get() {

                return this.$store.state.serverHost
            },

            set(value) {

                this.$store.commit('setServerHost', value)
            }
        },

        serverPort: {

            get() {

                return this.$store.state.serverPort
            },

            set(value) {

                this.$store.commit('setServerPort', value)
            },
        }
    },

    methods: {

        handleConnectRequest() {

            this.$store.dispatch('connect')
        }
    }
}
</script>

<style lang="scss" scoped>
@import "style";

.status-bar {
    padding: 8px;
    display: flex;
    align-items: center;
    background: darken($background-color, 2%);
    border-bottom: 2px solid darken($background-color, 15%);
}

.connection-setup {
    margin-left: auto;
    margin-right: 16px;

    .label {
        font-size:  .8rem;
        font-weight: bold;
        text-transform: uppercase;
        opacity: .7;
    }

    > * {

        margin-right: 8px;
    }
}

.connection-status {
    color: $accent-color; 
    fill: currentColor;

    .status {
        margin-right: 8px;
    }

    .icon {

    }
}
</style>