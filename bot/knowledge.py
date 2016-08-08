from __future__ import print_function
import pdb

useful_pos = [
  'NN',
  'PRP',
  'PRP$',
  'JJ',
  'WRB',
  'VBD'
];

useful_dep = [
  ''
]

def combine_dep_and_pos(pos_array, dep_array):
  for i in range(len(pos_array)):
    line_dep = dep_array[i]
    line_pos = pos_array[i]
    for j in range(len(line_dep)):
      dep = line_dep[j]
      dep_from = dep['from']
      dep_to = dep['to']
      pos_from = line_pos.get(dep_from, 'EMPTY')
      pos_to = line_pos.get(dep_to, 'EMPTY')
      dep['from'] = {'word': dep_from, 'pos': pos_from}
      dep['to'] = {'word': dep_to, 'pos': pos_to}

def flatten_dep(dep_info_array):
  flattened_dep = []
  for dep_array in dep_info_array:
    flattened_dep.extend(dep_array)

  return flattened_dep

def merge_object(to_object, from_object):
  merged_object = {}
  for key in to_object:
    from_object_set = set(from_object.get(key, set()))
    to_object_set = set(to_object[key])
    merged_object[key] = list(to_object_set.union(from_object_set))

  return merged_object

def generate(pos_info_array, dep_info_array):
  # Remove sentences which don't have useful pos. eg. Hey_UH There_EX !_.
  for pos_dict in pos_info_array:
    keys = pos_dict.keys()
    for key in keys:
      if(pos_dict[key] not in useful_pos):
        pos_dict.pop(key, None)

  # Combine dep and pos
  combine_dep_and_pos(pos_info_array, dep_info_array)

  dep_info_array = flatten_dep(dep_info_array)

  print('')

  for dep in dep_info_array:
    print(dep)

  print('')
  # print('')

  nouns = {}
  for dep in dep_info_array:
    dep_from = dep['from']
    dep_to = dep['to']
    pos_from = dep_from['pos']
    pos_to = dep_to['pos']
    if (pos_from in ['NN', 'PRP', 'PRP$']):
      word = dep_from['word']
      noun_object = {
        'component_words': [word],
        'pos_attached': [pos_from]
      }
      if word in nouns:
        noun_object = merge_object(nouns[word], noun_object)
      nouns[word] = noun_object

    if (pos_to in ['NN', 'PRP', 'PRP$']):
      word = dep_to['word']
      noun_object = {
        'component_words': [word],
        'pos_attached': [pos_to]
      }
      if word in nouns:
        noun_object = merge_object(nouns[word], noun_object)
      nouns[word] = noun_object

  print('')
  print(nouns)

  for dep in dep_info_array:
    dep_from = dep['from']
    dep_to = dep['to']
    pos_from = dep_from['pos']
    pos_to = dep_to['pos']
    from_is_noun = pos_from in ['NN', 'PRP', 'PRP$']
    to_is_noun = pos_to in ['NN', 'PRP', 'PRP$']
    if from_is_noun and to_is_noun:
      word_to = dep_to['word']
      word_from = dep_from['word']
      new_word = word_to + ' ' + word_from
      nouns[new_word] = merge_object(nouns[word_to], nouns[word_from])
      nouns.pop(word_to, None)
      nouns.pop(word_from, None)

  print('')
  print(nouns)












