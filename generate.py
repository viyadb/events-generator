#!/usr/bin/env python2.7

from lib.random import RandomGenerator
from lib.res import load_file
from lib.apps import next_popular_app, events_per_session_gen, random_inapp_event, revenue_gen
from lib.ad_networks import next_popular_adnetwork
from lib.campaigns import random_campaign, init_campaigns
from lib.sites import next_random_siteid
import numpy
import scipy.stats
import random
import simpy
import argparse
import datetime
import pytz
import json

def engagement_delay_generator():
  """Generates times between seeing or clicking on ad and installing an application"""
  values = numpy.random.beta(1, 100, 500)
  times = [long(d * 10000) for d in values]
  return RandomGenerator(times)

engagement_delay = engagement_delay_generator()

def user_retention_coeff_gen():
  """Generates user retention coefficients using Gompertz distribution"""
  values = scipy.stats.gompertz.rvs(3, size=1000)
  return RandomGenerator(values)

next_user_retention_coeff = user_retention_coeff_gen()

def send_event(env, event_type, info):
  """Generates events from the info, and outputs it"""
  event = info.copy()
  event["event_time"] = env.now * 1000L
  event["event_type"] = event_type
  print json.dumps(event)

def engagements(env, options, frequency=100):
  """Generates new possible engagements based on random user and application"""
  while True:
    app_id, nonorg_probability, session_delay, events_indices = next_popular_app()
    info = {
      "user_id": random.getrandbits(32),
      "app_id": app_id,
      "organic": random.random() > nonorg_probability
    }
    env.process(engagement(env, options, session_delay, events_indices, info))
    yield env.timeout(frequency)

def engagement(env, options, session_delay, events_indices, info):
  """Proceed through the engagement process, and generate activity"""

  if not info["organic"]:
    event_type = "click" if random.random() < options.ctr else "impression"
    info["ad_network"] = next_popular_adnetwork()
    info["campaign"] = str(random_campaign(env.now))
    info["site_id"] = next_random_siteid()
    send_event(env, event_type, info)

  yield env.timeout(engagement_delay())

  send_event(env, "install", info)

  user_retention_coeff = next_user_retention_coeff()
  retention_days = 100 * user_retention_coeff
  if info["organic"]:
    retention_days *= (retention_days * 0.012) + 1.46
  retention_days = long(retention_days)
  total_seconds = retention_days * 86400

  while total_seconds > 0:
    send_event(env, "session", info)

    for e in range(events_per_session_gen()):
      inapp_delay = random.randint(3, 20)
      yield env.timeout(inapp_delay)
      inapp_info = info.copy()
      inapp_info["revenue"] = revenue_gen()
      inapp_info["event_name"] = random_inapp_event(events_indices)
      send_event(env, "inappevent", inapp_info)
      total_seconds -= inapp_delay

    total_seconds -= session_delay
    yield env.timeout(session_delay)

if __name__ == '__main__':
  parser = argparse.ArgumentParser(usage="usage: %(prog)s [options]", version="%(prog)s 1.0")

  parser.add_argument("-c", "--click-through-rate",
      dest="ctr",
      type=float,
      default=0.005,
      help="Click-through rate")

  parser.add_argument("-r", "--campaigns-number",
      dest="campaigns_num",
      type=int,
      default=10000,
      help="Number of running campaigns at any time")

  parser.add_argument("-s", "--start-date",
      dest="start_date",
      help="Events start date in format YYYY-MM-DD",
      default=datetime.datetime(2015, 01, 01, 0, 0, 0, 0, pytz.UTC),
      type=lambda d: datetime.datetime.strptime(d, '%Y-%m-%d').replace(tzinfo=pytz.UTC))

  options = parser.parse_args()

  env = simpy.Environment(
    initial_time = long((options.start_date - datetime.datetime(1970, 1, 1, 0, 0, 0, 0, pytz.UTC)).total_seconds())
  )
  init_campaigns(env.now, options.campaigns_num)
  env.process(engagements(env, options))
  env.run()

