from __future__ import absolute_import
import random
from lib.res import load_file

verbs = load_file("verbs.txt")

def next_inapp_event(num_sites=10000):
  num_domains = len(popular_domains)
  return "http://{0}/page{1}".format(
    popular_domains[random.randint(0, num_domains-1)],
    random.randint(1, num_sites / num_domains)
  )

