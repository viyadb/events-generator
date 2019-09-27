from __future__ import absolute_import
from lib.res import load_file
import random

popular_domains = load_file("domains.txt")

def next_random_siteid(num_sites=10000):
  num_domains = len(popular_domains)
  return "http://{0}/page{1}".format(
    popular_domains[random.randint(0, num_domains-1)],
    random.randint(1, int(num_sites / num_domains))
  )

