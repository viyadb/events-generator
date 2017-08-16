from lib.res import load_file
from lib.random import WeightedRandomGenerator
import numpy

# Probability of whether the application is installed organically
# Taken from here: https://www.statista.com/statistics/373529/ios-organic-paid-installs/
nonorg_probability_gen = WeightedRandomGenerator([0.52, 0.4, 0.2, 0.17, 0.16, 0.15], [7, 3, 20, 23, 5, 25])

# Time between opening application:
session_delay_gen = WeightedRandomGenerator([h * 3600 for h in range(1, 11)], sorted(numpy.random.beta(8, 8, 10)))

def apps_generator(outliers=10):
  """Create generator function that returns random application and its non-organic installs probability"""
  apps = [[name, nonorg_probability_gen(), session_delay_gen()] for name in load_file("apps.txt")]
  dist = numpy.random.beta(0.1, 8, len(apps))
  popular_dist = 3
  for i in range(outliers):
    dist[-(i+1)] = popular_dist
    popular_dist -= 0.01
  return WeightedRandomGenerator(apps, dist)

next_popular_app = apps_generator()

