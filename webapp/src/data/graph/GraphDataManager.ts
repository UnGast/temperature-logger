export default class GraphDataManager {

  constructor(public data: GraphData) {
    
  }

  get dataBounds(): Bounds {

    let bounds: Bounds = {
      yMax: -Number.MAX_VALUE,
      yMin: Number.MAX_VALUE,
      xMin: Number.MAX_VALUE,
      xMax: -Number.MAX_VALUE
    }

    for (let dataPointList of Object.values(this.data)) {
      
      for (let dataPoint of dataPointList) {
        if (dataPoint.y > bounds.yMax) {
          bounds.yMax = dataPoint.y
        }
        if (dataPoint.y < bounds.yMin) {
          bounds.yMin = dataPoint.y
        }
        if (dataPoint.x > bounds.xMax) {
          bounds.xMax = dataPoint.x
        }
        if (dataPoint.x < bounds.xMin) {
          bounds.xMin = dataPoint.x
        }
      }
    }

    return bounds
  }

  getDataBoundsBetween(xMin: number, xMax: number): Bounds {

    let bounds: Bounds = {
      xMin,
      xMax,
      yMin: Number.MAX_VALUE,
      yMax: -Number.MAX_VALUE
    }

    for (let dataPointList of Object.values(this.data)) {

      for (let dataPoint of dataPointList) {

        if (dataPoint.x >= xMin && dataPoint.x <= xMax) {

          if (dataPoint.y < bounds.yMin) {

            bounds.yMin = dataPoint.y
          }

          if (dataPoint.y > bounds.yMax) {

            bounds.yMax = dataPoint.y
          }
        }
      }
    }

    return bounds
  }
}