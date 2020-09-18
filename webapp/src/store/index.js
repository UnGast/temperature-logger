import { createStore } from 'vuex'

const store = createStore({

    state() {

        return {

            sensorData: []
        }
    },

    actions: {

        connect() {

            let socket = new WebSocket('ws://localhost:8000')

            console.log('TRYING TO CONNECT')

            socket.onopen = () => {

                console.log("CONNECTED")

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
        }
    }
})

export default store