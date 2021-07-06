export interface SensorDataPoint {
  sensorId?: string
  timestamp: number 
  value: number 
}

export interface SensorArrayData {
 [key: string]: [SensorDataPoint]
}

export interface SensorInfo {
  id: string
  type: string
  position: string
  accuracy: number 
  correction_offset: number
}

export interface SensorArrayInfo {
  [key: string]: SensorInfo
}