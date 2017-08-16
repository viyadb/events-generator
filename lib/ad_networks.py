from lib.res import load_file
from lib.random import WeightedRandomGenerator
import numpy

def adnetwork_generator(outliers=3):
  """Create generator function that returns random Ad Network"""
  ad_networks = load_file("networks.txt")
  dist = numpy.random.beta(0.1, 8, len(ad_networks))
  popular_dist = 3
  for i in range(outliers):
    dist[-(i+1)] = popular_dist
    popular_dist -= 0.01
  return WeightedRandomGenerator(ad_networks, dist)

next_popular_adnetwork = adnetwork_generator()

