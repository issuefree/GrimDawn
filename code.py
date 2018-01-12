import itertools
import string
from dataModel import *

afs = ["1a", "1e", "1c", "1o", "1p"]

vectors = []

for i in range(5):
	vectors += [Affinity(string.join(list(a), " ")) for a in list(itertools.combinations(afs, i+1))]

for a in vectors:
	print a