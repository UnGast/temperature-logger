import { SensorArrayData } from './SensorData';

export default class SensorDataManager {
  static getLatestTimestamp(sensorArrayData: SensorArrayData): number {
    
    var latestTimestamp = -Number.MAX_VALUE

    for (let dataPoints of Object.values(sensorArrayData)) {
      for (let dataPoint of dataPoints) {
        if (dataPoint.timestamp > latestTimestamp) {
          latestTimestamp = dataPoint.timestamp
        }
      }
    }

    return latestTimestamp
  }
}