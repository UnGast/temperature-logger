import { createStore } from 'vuex'
import chroma from 'chroma-js'
import localforage from 'localforage'
import { formatDatetime } from '@/data/date'
import DownloadPackager from '~/data/sensor/DownloadPackager'

let sensorColorScale = chroma.scale(['yellow', 'lightgreen', 'lime', 'lightblue', 'orange']).mode('lch')

const store = createStore({

	state() {

		return {
			serverHost: process.env.VUE_APP_DEFAULT_SERVER_HOST,
			serverPort: process.env.VUE_APP_DEFAULT_SERVER_PORT,
			socket: null,
			connecting: false,
			connected: false,
			sensorInfo: {},
			sensorData: {},
			reconnectInterval: 1000,
			selectedSensorIds: new Set(),
			selectedTimeframe: 'interval',
			timeframeSettings: {
				interval: {
					start: Math.floor(Date.now() / 1000) - 1000,
					end: Math.floor(Date.now() / 1000)
				}
			}
		}
	},

	mutations: {
		setServerHost(state, value) {
			state.serverHost = value
		},
		setServerPort(state, value) {
			state.serverPort = value
		},
		setSocket(state, socket) {
			state.socket = socket
		},
		setConnecting(state, connecting) {
			state.connecting = connecting
		},
		setConnected(state, value) {
			state.connected = value
		},
		clearServerData(state) {
			state.sensorData = {}
			state.sensorInfo = {}
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
		storeStreamValues(state, { timestamp, values }) {

			for (let [sensorId, value] of Object.entries(values)) {

				if (!state.sensorData[sensorId]) {
					state.sensorData[sensorId] = []
				}

				state.sensorData[sensorId].push({ timestamp, value })
			}
		},
		setSelectedTimeframe(state, value) {
			state.selectedTimeframe = value
		},
		setTimeframeIntervalStart(state, value) {
			state.timeframeSettings.interval.start = value
		},
		setTimeframeIntervalEnd(state, value) {
			state.timeframeSettings.interval.end = value
		},
		storeTimeframeIntervalValues(state, values) {

			for (let timeValue of values) {

				if (!state.sensorData[timeValue.sensorId]) {
					state.sensorData[timeValue.sensorId] = []
				}

				state.sensorData[timeValue.sensorId].push({
					timestamp: timeValue.timestamp,
					value: timeValue.value
				})
			}

			for (let timeValues of Object.values(state.sensorData)) {
				timeValues.sort((a, b) => a.timestamp - b.timestamp)
			}
		}
	},

	actions: {

		async restoreSettings({ commit })  {

			let storedServerSettings = await localforage.getItem('server')

			if (storedServerSettings) {

				commit('setServerHost', storedServerSettings.host)
				commit('setServerPort', storedServerSettings.port)
			}
		},

		async storeSettings({ state }) {

			await localforage.setItem('server', {
				host: state.serverHost,
				port: state.serverPort
			})
		},

		connect({ commit, dispatch, state }) {

			if (state.connecting) return

			commit('clearServerData')

			commit('setConnecting', true)

			let socket = new WebSocket(`ws://${state.serverHost}:${state.serverPort}`)

			socket.onopen = () => {

				console.log('Connected to server.')

				commit('setSocket', socket)
				
				commit('setConnecting', false)

				commit('setConnected', true)

				dispatch('fetchSensorInfo')

				dispatch('fetchTimeframeIntervalData')

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
					commit('storeStreamValues', { timestamp: message.timestamp, values: message.values })
					break

				case 'sensor_info':
					commit('setSensorInfo', message.sensors)
					commit('setSelectedSensorIds', message.sensors.map(sensor => sensor.id))
					break
				
				case 'past_data':
					commit('storeTimeframeIntervalValues', message.data)
					break
			}
		},

		fetchTimeframeIntervalData({ state }) {

			state.socket.send(JSON.stringify({
				action: 'get_past_data',
				start: state.timeframeSettings.interval.start,
				end: state.timeframeSettings.interval.end
			}))
		},

		downloadTimeframeIntervalData({ state }) {

			let blob = DownloadPackager.pack(state.sensorData, state.sensorInfo)

			let blobUrl = window.URL.createObjectURL(blob)

			let a = document.createElement('a')

			a.href = blobUrl

			let startDate = new Date(state.timeframeSettings.interval.start)

			let endDate = new Date(state.timeframeSettings.interval.end)

			a.setAttribute('download', `sensor-data-${formatDatetime(startDate)}-${formatDatetime(endDate)}.csv`)

			a.style.display = 'none'

			document.body.append(a)

			a.click()

			a.remove()
		}
	},
})

store.watch(state => {

	return `${state.serverHost}${state.serverPort}`

}, () => {

	store.dispatch('storeSettings')
})

export default store