# Natural Language Toolkit: Eliza
#
# Copyright (C) 2001-2016 NLTK Project
# Authors: Steven Bird <stevenbird1@gmail.com>
#          Edward Loper <edloper@gmail.com>
# URL: <http://nltk.org/>
# For license information, see LICENSE.TXT

# Based on an Eliza implementation by Joe Strout <joe@strout.net>,
# Jeff Epler <jepler@inetnebr.com> and Jez Higgins <mailto:jez@jezuk.co.uk>.

# a translation table used to convert things you say into things the
# computer says back, e.g. "I am" --> "you are"

from __future__ import print_function

from bot.nltk_chat_util import Chat, reflections

# a table of response pairs, where each pair consists of a
# regular expression, and a list of possible responses,
# with group-macros labelled as %1, %2.

pairs = (
  (r'I need (.*)',
  ( "I need your location and your preference... both, in a single text.",
    "Tell me where you are and what you want to eat. I am good at that. Other things... not so much.")),


  (r'Are you (.*)',
  ( "I am going to be a super smart bot. I am powered by tech developed at http://tonatasha.com",
    "I use Yelp API to help you, I am just a tiny AI who is learning.",
    "Perhaps you believe I am %1. I am good at only finding food.",
    "I may be %1 -- whatever you think doesn't matter! :P Let me find some eating place for you.")),

  (r'How (.*)',
  ( "How do you suppose?",
    "Perhaps you can answer your own question.",
    "What is it you're really asking?")),

  (r'Because (.*)',
  ( "Is that the real reason?",
    "What other reasons come to mind?",
    "Does that reason apply to anything else?",
    "If %1, what else must be true?")),

  (r'(.*) sorry (.*)',
  ( "There are many times when no apology is needed. :P Let me find some eating place for you.",
    "What feelings do you have when you apologize? :P Let me find some eating place for you.")),

  (r'Hello(.*)',
  ( "Hello... I'm glad you could drop by today.",
    "Hi there... how are you today? :P Let me find some eating place for you.",
    "Hello, how are you feeling today? I am good at finding food. Other things, not so much.")),

    (r'Hi(.*)',
    ( "Hello... I'm glad you could drop by today.",
      "Hi there... how are you today? :P Let me find some eating place for you.",
      "Hello, how are you feeling today? I am good at finding food. Other things, not so much.")),

  (r'I think (.*)',
  ( "Do you doubt %1?",
    "Do you really think so?",
    "But you're not sure %1?")),

  (r'(.*) friend (.*)',
  ( "Tell me more about your friends.",
    "When you think of a friend, what comes to mind?",
    "Why don't you tell me about a childhood friend?")),

  (r'Yes',
  ( "I need you to tell me what would you like to eat and where.",
    "OK, but can you elaborate a bit? What and where you want to eat?")),


  (r'Is it (.*)',
  ( "I am only good at finding places to eat. Please hit me up with new query. ",
    "It could well be that %1. I don't know.")),

  (r'It is (.*)',
  ( "You seem very certain.","What would you like to eat? where?")),

  (r'Can you (.*)',
  ( "What makes you think I can't %1?",
    "If I could %1, then what?",
    "Why do you ask if I can %1?")),

  (r'Can I (.*)',
  ( "You are a free person in a free country. Aren't you?. Let me help you find food.",
  "I am not good at things other than finding food.")),

  (r'You are (.*)',
  ( "All I do is find food places near you.",
    "Let me serve you. Thank you. Ask me what and where you want to eat. I need both information in a single text. ")),

    (r'(.*)',
    ( "I am not good at things other than finding food. please specify both food and city/town in the text.",
    "I am good at finding food in a city, other things not so much. please specify both food and city/town in the text."))
)

eliza_chatbot = Chat(pairs, reflections)

def eliza_chat(incoming_message):
    return eliza_chatbot.converse3(incoming_message)

def demo():
    eliza_chat()

if __name__ == "__main__":
    demo()
