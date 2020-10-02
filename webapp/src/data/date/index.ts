import { format, parse } from 'date-fns'

export function formatDate(date: Date): string {
  return format(date, 'dd/MM/yyyy')
}

export function formatDatetime(date: Date, seconds: boolean = false): string {
  return format(date, 'dd/MM/yyyy HH:mm' + (seconds ? ':ss' : ''))
}

export function formatTime(date: Date): string {
  return format(date, 'HH:mm')
}

export function parseDatetime(datetime: string): Date {
  return parse(datetime, 'dd/MM/yyyy HH:mm', new Date())
}
