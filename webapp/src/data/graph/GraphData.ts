interface GraphDataPoint {
  x: number
  y: number
}

interface GraphData {
  [key: string]: [GraphDataPoint]
}

interface Bounds {
  xMin: number
  xMax: number
  yMin: number
  yMax: number
}