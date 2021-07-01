/**
 * Get the index of the first significant (non zero) digit. Before decimal separator negative, after positive
 */
export function firstSignificantIndex(number: number): number {
  if (number === 0 || isNaN(number)) {
    return 0
  }
  let separatorIndex = number.toString().indexOf('.')
  let startIndex = -separatorIndex
  let numberString = number.toString()
  for (let i = 0; i < numberString.length; i++) {
    let digit = numberString[i]

    if (digit === '.') {
      startIndex = 1
      continue
    } else {
      if (parseFloat(digit) > 0) {
        return startIndex
      }
      startIndex += 1
    }
  }
  return 0
}

export function roundToSignificant(number: number, significant: number): number {
  let multiplier: number
  if (significant < 0) {
    multiplier = Math.pow(10, (significant + 1))
  } else {
    multiplier = Math.pow(10, significant)
  }
  return Math.round(number * multiplier) / multiplier
}