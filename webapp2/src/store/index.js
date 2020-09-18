import { createStore } from 'vuex'

const store = createStore({

    state() {

        return {

            sensorData: [],

            connected: false
        }
    },

    mutations: {

        setConnected(state, value) {

            state.connected = value
        }
    },

    actions: {

        connect({ commit }) {

            let socket = new WebSocket('ws://localhost:8000')

            socket.onopen = () => {

                console.log("Connected to server.")

                commit('setConnected', true)

                socket.send(JSON.stringify({
                    
                    action: "stream",

                    interval: 1
                }))

                setTimeout(() => {

                    socket.send(JSON.stringify({

                        action: "end_stream"

                    }))

                }, 3000)
            }

            socket.onmessage = message => {

                console.log('RECEIVED MESSAGE', message)
            }

            socket.onclose = () => {

                commit('setConnected', false)
            }
        }
    }
})

export default store