
class MarkovGenerator(object):

  def __init__(self, n, max):
    self.n = n # order (length) of ngrams
    self.max = max # maximum number of elements to generate
    self.ngrams = dict() # ngrams as keys; next elements as values
    self.beginnings = list() # beginning ngram of every line

  def tokenize(self, text):
    return text.split(" ")

  def feed(self, first,second):

    self.beginnings.append(first)
    # if we've already seen this ngram, append; otherwise, set the
    # value for this key as a new list
    if first[0] in self.ngrams:
      self.ngrams[first[0]].append(second)
    else:
      self.ngrams[first[0]] = [second]


  # generate a text from the information in self.ngrams
  def generate(self):

    from random import choice

    # get a random interval and add to output list,
    current = choice(self.beginnings)
    output = [current[1]]
    current_letter = current[0]
    for i in range(self.max):
      if current_letter in self.ngrams:
        possible_next = self.ngrams[current[0]]
        next = choice(possible_next)
        output.append(next[1])
        # print output
        # get the last N entries of the output; we'll use this to look up
        # an ngram in the next iteration of the loop
        current_letter = next[1].text[-1]
      else:
        break

    return output
    

if __name__ == '__main__':

  import sys

  generator = MarkovGenerator(n=3, max=500)
  for line in sys.stdin:
    line = line.strip()
    generator.feed(line)

  for i in range(14):
    print generator.generate()

