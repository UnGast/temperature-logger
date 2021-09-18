from collections import namedtuple

Column = namedtuple("Column", "data_key title type")

class CSVFileManager:
  def __init__(self, columns: [Column]):
    self.columns = columns

  def read_file(self, file_path):
    with open(file_path, 'r') as file:
      try:
        lines = file.readlines()
        data_lines = lines[1:]
        data = []

        for line in data_lines:
          try:
            line_data = {}
            raw_column_data = line.split(',')

            for index, column in enumerate(self.columns):
              line_data[column.data_key] = column.type(raw_column_data[index])

            data.append(line_data)

          except Exception as e:
            print('exception when reading data file', file_path, ":", e)

        return data

      except Exception as e:
        print('exception when reading data file', file_path, ":", e)
        return []

  def get_csv_header(self):
    header = ''
    for column in self.columns:
      header += column.title
      header += ','
    return header


