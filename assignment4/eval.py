from corpus import *
from collections import *

class Evaluator(object):

  def __init__(self):
    self.accuracy = 0
    self.tags = {}

  def evaluate(self, tagged_corpus):
    tags = {}
    total_taggings = 0
    i = 0

    # Go through the tagged corpus and evaluate it
    for sentence in tagged_corpus.sentences:
      for line in sentence:
        i += 1
        POS = line['POS']

        # Make sure the tag is saved at least once
        if POS not in tags:
          tags[POS] = {}
          tags[POS]["accurate"] = 0
          tags[POS]["total"] = 0
          tags[POS]["error_pairs"] = []

        # If the POS equals PPOS, increase the accuracy count
        if POS == line['PPOS']:
          tags[POS]["accurate"] += 1
        else:
          tags[POS]["error_pairs"].append( (POS, line['PPOS']) )

        # Increase the total times the POS has been seen
        tags[POS]["total"] += 1
        total_taggings += 1

    # Compute the accuracy
    accurate_sum = 0
    for tag in tags.values():
      accurate_sum += tag["accurate"]

    self.accuracy = float(accurate_sum)/total_taggings
    self.evaluated_tags = tags
    self.tagged_corpus = tagged_corpus

  def print_stats(self, individual_tags = False):
    print "===== POS Tagger evaluation ============================="
    print "                       Tagger:", self.tagged_corpus.tagger_name
    print "                     Accuracy:", "%1.4f" % self.accuracy
    print
    print "                  Test corpus:", self.tagged_corpus.corpus_file
    print "              Training corpus:", self.tagged_corpus.training_file
    print "          Evaluated sentences:", len(self.tagged_corpus.sentences)
    print "  Time elapsed during tagging:", self.tagged_corpus.time_elapsed, "s"
    print

    if individual_tags:
      print "  Accuracy for individual tags:"
      for POS, data in OrderedDict(sorted(self.evaluated_tags.items())).iteritems():
        print "       %(tag)-4s %(acc)1.4f" % \
              {"tag": POS, "acc": (float(data["accurate"])/data["total"])}

    print "========================================================="
    print ""

  def write_confusion_matrix(self, filename):
    tags = OrderedDict(sorted(self.evaluated_tags.items()))

    # Create a zero matrix
    matrix = [[0 for key in tags.keys()] for key in tags.keys()]

    # Insert correctly tagged elements
    for i, (POS, data) in enumerate(tags.iteritems()):
      matrix[i][i] = data["accurate"]
       

    # Insert error pairs
    for row_index, (row_POS, data) in enumerate(tags.iteritems()):
      if not data['error_pairs']:
        pass
      else:
        # Go thru all error pairs and increase error hit
        for (should_be, tagged_as) in data['error_pairs']:
          for col_index, col_POS in enumerate(tags.keys()):
            if should_be == row_POS and tagged_as == col_POS:
              matrix[row_index][col_index] += 1


    # Insert axis names
    matrix.insert(0, ["%5s" % key for key in tags.keys()])
    matrix[0].insert(0, ' '*5)
    for i, key in enumerate(tags.keys()):
      matrix[i+1].insert(0, "%-5s" % key) # i+1 because first row is axis name

    # Convert number to strings
    for i, row in enumerate(matrix[1:]):
      for j, col in enumerate(row[1:]):
        matrix[i+1][j+1] = "%5d" % col if col != 0 else "%5s" % '.'

    # Create print string
    matrix_string = ""
    for row in matrix:
      for col in row:
        matrix_string += col
      matrix_string += "\n"


    # Output the print string
    #print matrix_string
    text_file = open(filename, "w")
    text_file.write(matrix_string)
    text_file.close()



if __name__ == "__main__":
  c = Corpus("ex_sentence.txt")
  
  e = Evaluator()
  e.evaluate(c)
  e.print_confusion_matrix("hej")
  #e.print_stats("Test", True)
