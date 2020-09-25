import { createStore } from 'vuex'
import chroma from 'chroma-js'

let sensorColorScale = chroma.scale(['yellow', 'lightgreen', 'lime', 'lightblue', 'orange']).mode('lch')

const store = createStore({

	state() {

		return {
			socket: null,
			connecting: false,
			connected: false,
			sensorInfo: {},
			sensorData: {},
			reconnectInterval: 1000,
			selectedSensorIds: new Set([1, 2, 3, 4]),
			timeframeStart: Date.now() - 1000 * 1000,
			timeframeEnd: Date.now()
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
			state.sensorInfo = {}

			let colors = sensorColorScale.colors(sensorInfo.length)

			for (let [index, sensor] of sensorInfo.entries()) {
				state.sensorInfo[sensor.id] = sensor
				state.sensorInfo[sensor.id].color = colors[index]
			}
		},
		setSelectedSensorIds(state, ids) {
			state.selectedSensorIds = new Set(ids)
		},
		setSensorSelected(state, sensorId) {
			state.selectedSensorIds.add(sensorId)
		},
		setSensorUnselected(state, sensorId) {
			state.selectedSensorIds.delete(sensorId)
		},
		storeStreamValues(state, values) {

			for (let [sensorId, value] of Object.entries(values)) {

				if (!state.sensorData[sensorId]) {
					state.sensorData[sensorId] = []
				}

				state.sensorData[sensorId].push(value)

		/*		var appendIndex = 0

				for (var i = state.sensorData[sensorId].length; i > 0; i++) {
					if state.sensorData[sensorId][i - 1].timestamp >
				}

				state.sensorData[sensorId].splice(appendIndex, 0, value)*/
			}
		},
		setTimeframeStart(state, value) {
			state.timeframeStart = value
		},
		setTimeframeEnd(state, value) {
			state.timeframeEnd = value
		},
		storeTimeframeIntervalValues(state, values) {

			for (let timeValue of values) {

				state.sensorData[String(timeValue.sensorId)].push({
					timestamp: timeValue.timestamp,
					value: timeValue.value
				})
			}

			for (let timeValues of state.sensorData.values()) {
				timeValues.sort((a, b) => a.timestamp - b.timestamp)
			}
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
					commit('storeStreamValues', message.values)
					break

				case 'sensor_info':
					commit('setSensorInfo', message.sensors)
					break
				
				case 'past_data':
					commit('storeTimeframeIntervalValues', message.data)
					break
			}
		},

		fetchTimeframeIntervalData({ state }) {

			state.socket.send(JSON.stringify({
				action: 'get_past_data',
				start: Math.floor(state.timeframeStart / 1000),
				end: Math.floor(state.timeframeEnd / 1000)
			}))
		}
	}
})

export default store