#!/usr/bin/python
from collections import defaultdict
import os
import string

class Vectorizer():
  # tunable stuff
  TUNING = {
      "IGNORE_CASE": True,
      "STRIP_PUNCTUATION": True, 
      }

  START_STRING = "*** START OF THIS PROJECT GUTENBERG EBOOK"
  END_STRING = "*** END OF THIS PROJECT GUTENBERG EBOOK"

  def __init__(self, book_dir, tuning=None):
    self.directory = book_dir
    if tuning is not None:
      self.TUNING = tuning

  def tokenize_book(self, infile, age, word_dict):
    """Take a file and add its contents to a word dictionary."""
    with open(infile) as f:
      start_string_spotted = False
      for line in f:
        line = line.replace("\n", "")
        if not start_string_spotted:
          if self.START_STRING in line:
            start_string_spotted = True
            continue
          else:
            continue
        if self.END_STRING in line:
          break
        words = line.split(" ")
        if self.TUNING["IGNORE_CASE"]:
          words = map(lambda word: word.lower(), words)
        if self.TUNING["STRIP_PUNCTUATION"]:
          words = map(lambda word: word.translate(string.maketrans("", ""),
            string.punctuation), words)

        # add the words to the word dict
        for word in words:
          if word is not '':
            word_dict[word] += [age]

  def get_books(self):
    files = []
    for (dirpath, dirnames, filenames) in os.walk(self.directory):
      files += [(os.path.splitext(os.path.basename(filename))[0],
        os.path.join(dirpath, filename)) for filename in filenames]

    word_dict = defaultdict(list)
    
    for (age_str, f) in files:
      try:
        age = int(age_str)
        self.tokenize_book(f, age, word_dict)
      except ValueError as ve:
        print ve

    return word_dict

class Analyzer():
  TUNING = {
      "IGNORE_CASE": True,
      "STRIP_PUNCTUATION": True, 
      }
  def __init__(self, book_dir, tuning=None):
    self.vectorizer = Vectorizer(book_dir)
    if tuning is not None:
      self.TUNING = tuning
    
  def guess(self, input_string):
    word_dict = self.vectorizer.get_books()

    words = input_string.split(" ")
    guesses = []

    if self.TUNING["IGNORE_CASE"]:
      words = map(lambda word: word.lower(), words)
    if self.TUNING["STRIP_PUNCTUATION"]:
      words = map(lambda word: word.translate(string.maketrans("", ""),
        string.punctuation), words)

    for word in words:
      guesses += word_dict[word]

    if len(guesses) is 0:
      return "no guess was made"
    return max(set(guesses), key=guesses.count)

if __name__ == '__main__':
  a = Analyzer("books/")

  print "I guess:", a.guess('hello, world!')
