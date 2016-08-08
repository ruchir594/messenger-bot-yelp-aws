import get_first_sentence
import natasha_chat
import os
import subprocess
import re

import file_reader
import knowledge

def init():
  script_dir = os.path.dirname(os.path.realpath(__file__))
  os.chdir(script_dir)

  if not os.path.exists('data'):
    os.makedirs('data')

def sanitize_pos(pos_lines):
  pos_array = []
  for line in pos_lines:
    line_stripped = line.strip()
    all_pos = line_stripped.split(' ')
    line_pos_dict = {}
    for item in all_pos:
      pos_split = item.split('_')
      word = pos_split[0]
      pos = pos_split[1]
      line_pos_dict[word] = pos
    pos_array.append(line_pos_dict)
  return pos_array

def sanitize_dep(dependencies_content):
  dep_content_array = dependencies_content.split('\n\n')
  dep_array = []
  regex = re.compile(r'(.*?)\((.*)-\d+, (.*)-\d+\)')
  for content_string in dep_content_array:
    if (content_string == ''):
      continue
    line_content_array = content_string.split('\n')
    line_dep = []
    for dep in line_content_array:
      match_re = re.match(regex, dep)
      if (match_re):
        dep_type = match_re.group(1)
        dep_from = match_re.group(2)
        dep_to = match_re.group(3)
        dep_object = {'type': dep_type, 'from': dep_from, 'to': dep_to}
        line_dep.append(dep_object)
    dep_array.append(line_dep)

  return dep_array

def post_process(text):
  f = open('data/temp.txt', 'w')
  f.write(text)
  f.close()

  command = 'sh ../pos_tagger.sh data/temp.txt 2> data/temp_info.txt > data/temp_tagged.txt'
  subprocess.call(command, shell=True)

  pos_lines = file_reader.read_file_lines('data/temp_tagged.txt')
  pos_info_array = sanitize_pos(pos_lines)
  # print(pos_info_array)

  command = 'sh ../parser_dependencies.sh data/temp.txt 2> data/temp_info.txt > data/temp_dependencies.txt'
  subprocess.call(command, shell=True)

  dependencies_content = file_reader.read_file('data/temp_dependencies.txt')
  dep_info_array = sanitize_dep(dependencies_content)
  # print(dep_info_array)

  knowledge.generate(pos_info_array, dep_info_array)

def run():
  init()

  print('Natasha\n-------')
  print('Talk to the program by typing in plain English, using normal upper-')
  print('and lower-case letters and punctuation. Enter "goodbye" when done.')
  print('=' * 67)

  question = get_first_sentence.generate()
  print('N: ' + question)

  while True:
    incoming_message = raw_input('>  ')
    message_stripped = incoming_message.strip().lower()

    post_process(question)
    post_process(incoming_message)

    if message_stripped == 'goodbye' or message_stripped == 'goodbye.':
      break
    natasha_chat.eliza_chat(incoming_message)

if __name__ == "__main__":
  run()
