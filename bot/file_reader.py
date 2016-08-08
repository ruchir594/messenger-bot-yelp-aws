def read_file_lines(filename):
  f = open(filename, 'r')
  file_lines = f.readlines()
  f.close()
  return file_lines

def read_file(filename):
  f = open(filename, 'r')
  file_content = f.read()
  f.close()
  return file_content
