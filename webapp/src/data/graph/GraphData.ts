interface GraphDataPoint {
  x: Number
  y: Number
}

interface GraphData {
  [key: string]: [GraphDataPoint]
}

interface Bounds {
  xMin: Number
  xMax: Number
  yMin: Number
  yMax: Number
}