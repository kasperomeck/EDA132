from readARFF import readARFF
from DLT import DLT



if __name__ == "__main__":
  dataset = readARFF("weather.arff")
  tree = DLT(dataset,dataset)
  print tree
  