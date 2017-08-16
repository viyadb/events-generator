from __future__ import absolute_import
import bisect
import random

class RandomGenerator(object):
  """Choses random element from the list"""
  def __init__(self, elements):
    self.elements = elements

  def next(self):
    return self.elements[random.randint(0, len(self.elements) - 1)]

  def __call__(self):
    return self.next()

class WeightedRandomGenerator(object):
  """Generator for elements according to their weights"""
  def __init__(self, elements, weights):
    self.elements = elements
    self.totals = []
    running_total = 0
    for w in weights:
      running_total += w
      self.totals.append(running_total)

  def next(self):
    rnd = random.random() * self.totals[-1]
    idx = bisect.bisect_right(self.totals, rnd)
    return self.elements[idx]

  def __call__(self):
    return self.next()

