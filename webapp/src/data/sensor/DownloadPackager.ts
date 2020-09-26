import { SensorArrayData, SensorArrayInfo } from './SensorData'
import { formatDatetime } from '~/data/date/format'

export default class DownloadPackager {

  static pack(data: SensorArrayData, info: SensorArrayInfo): Blob {
    
    var csv = ''

    csv += 'timestamp,'

    let timestamps = new Set<number>()

    let dataByTimestamp: { [key: number]: { [key: string]: number } } = {}

    for (let sensorId of Object.keys(data)) {

      let sensorInfo = info[sensorId]

      csv += 'temperature(°C):'

      if (sensorInfo) {

        csv += `${sensorInfo.id}:${sensorInfo.position}`

      } else {

        csv += `${sensorId}:noinfo`
      }

      csv += ','

      let sensorDataPoints = data[sensorId]

      for (let dataPoint of sensorDataPoints) {
        
        if (!dataByTimestamp[dataPoint.timestamp]) {

          timestamps.add(dataPoint.timestamp)

          dataByTimestamp[dataPoint.timestamp] = {}
        }

        dataByTimestamp[dataPoint.timestamp][sensorId] = dataPoint.value
      }
    }

    csv += '\n'

    let sortedTimestamps = Array.from(timestamps).sort((a, b) => a - b)

    for (let timestamp of sortedTimestamps) {

      csv += formatDatetime(new Date(timestamp * 1000), true) + ','

      for (let sensorId of Object.keys(data)) {

        csv += dataByTimestamp[timestamp][sensorId] + ','
      }

      csv += '\n'
    }

    return new Blob([csv], { type: 'application/text' })
  }
}