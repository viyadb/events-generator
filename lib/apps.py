from __future__ import absolute_import
from lib.res import load_file
from lib.random import WeightedRandomGenerator, RandomGenerator
import numpy
import random

events = load_file("events.txt")

# Probability of whether the application is installed organically
# Taken from here: https://www.statista.com/statistics/373529/ios-organic-paid-installs/
nonorg_probability_gen = WeightedRandomGenerator([0.52, 0.4, 0.2, 0.17, 0.16, 0.15], [7, 3, 20, 23, 5, 25])

# Time between opening application:
session_delay_gen = WeightedRandomGenerator([h * 3600 for h in range(1, 11)], sorted(numpy.random.beta(8, 8, 10)))

# Different inapp events number per app:
app_events_num_gen = RandomGenerator([long(r) + 1 for r in numpy.random.beta(3, 10, 100) * 10])

def random_events_indices():
  events_num = len(events)
  app_events_num = app_events_num_gen()
  start_idx = random.randint(0, events_num - 1 - app_events_num)
  return [start_idx, start_idx + app_events_num]

def apps_generator(outliers=10):
  """Create generator function that returns random application and its non-organic installs probability"""
  apps = [[name, nonorg_probability_gen(), session_delay_gen(), random_events_indices()]
      for name in load_file("apps.txt")]
  dist = numpy.random.beta(0.1, 8, len(apps))
  popular_dist = 3
  for i in range(outliers):
    dist[-(i+1)] = popular_dist
    popular_dist -= 0.01
  return WeightedRandomGenerator(apps, dist)

next_popular_app = apps_generator()

# In-app event revenue:
revenue_gen = RandomGenerator(numpy.random.beta(0.2, 10, 1000) * 10)

# Number of events per session to generate
events_per_session_gen = RandomGenerator([long(r) for r in numpy.random.beta(1, 4, 100) * 10])

def random_inapp_event(event_indices):
  return events[random.randint(event_indices[0], event_indices[1])]

