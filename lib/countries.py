from __future__ import absolute_import
from lib.random import WeightedRandomGenerator
from lib.res import load_file
import numpy, random

cities_by_country = {}
for l in load_file("cities.txt"):
  country_code, city = l.split("\t")
  if country_code not in cities_by_country:
    cities_by_country[country_code] = []
  cities_by_country[country_code].append(city)

def random_city(country):
  cities = cities_by_country[country]
  return cities[random.randint(0, len(cities) - 1)]

country_codes = cities_by_country.keys()
popular_countries = [u"IL", u"RU", u"TH", u"GB", u"FR", u"HK", u"CA", u"CH", u"IN", u"US"]
country_codes.extend(popular_countries)

def country_generator():
  dist = numpy.random.beta(0.1, 8, len(country_codes))
  popular_dist = 3.0
  for i in range(len(popular_countries)):
    dist[-(i+1)] = popular_dist
    popular_dist -= 0.01
  return WeightedRandomGenerator(country_codes, dist)

random_country = country_generator()
