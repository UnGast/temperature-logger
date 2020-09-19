import { createStore } from 'vuex'

const store = createStore({

	state() {

		return {
			socket: null,
			connecting: false,
			connected: false,
			sensorInfo: {},
			sensorData: {},
			reconnectInterval: 1000
		}
	},

	mutations: {
		setSocket(state, socket) {
			state.socket = socket
		},
		setConnecting(state, connecting) {
			state.connecting = connecting
		},
		setConnected(state, value) {
			state.connected = value
		},
		setSensorInfo(state, sensorInfo) {
			state.sensorInfo = sensorInfo
		}
	},

	actions: {

		connect({ commit, dispatch, state }) {

			if (state.connected || state.connecting) return

			commit('setConnecting', true)

			let socket = new WebSocket('ws://localhost:8000')

			socket.onopen = () => {

				console.log('Connected to server.')

				commit('setSocket', socket)
				
				commit('setConnecting', false)

				commit('setConnected', true)

				dispatch('fetchSensorInfo')

				socket.send(JSON.stringify({

					action: 'stream',

					interval: 1
				}))
			}

			socket.onmessage = message => {

				dispatch('processMessage', JSON.parse(message.data))
			}

			socket.onclose = socket.onerror = (error) => {

				if (error) {
					
					socket.close()
				}

				commit('setConnected', false)

				commit('setConnecting', false)

				setTimeout(() => {

					dispatch('connect')

				}, state.reconnectInterval)
			}
		},

		fetchSensorInfo({ commit, state }) {

			state.socket.send(JSON.stringify({
				action: 'get_sensor_info'
			}))
		},

		processMessage({ commit }, message) {

			switch (message.type) {

				case 'stream_value':
					console.log('GOT STREAM VALUE')
					break

				case 'sensor_info':
					commit('setSensorInfo', message.sensors)
			}

			console.log('RECEIVED MESSAGE', message)
		}
	}
})

export default store