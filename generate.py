#!/usr/bin/env python

from lib.random import RandomGenerator
from lib.res import load_file
from lib.apps import next_popular_app, events_per_session_gen, random_inapp_event, revenue_gen
from lib.ad_networks import next_popular_adnetwork
from lib.campaigns import random_campaign, init_campaigns
from lib.sites import next_random_siteid
from lib.countries import random_country, random_city
from lib.devices import random_device

import sys
import os
import numpy
import scipy.stats
import random
import simpy
import argparse
import datetime
import pytz
import json


def engagement_delay_generator():
    '''Generates times between seeing or clicking on ad and installing an application'''
    values = numpy.random.beta(1, 100, 500)
    times = [int(d * 10000) for d in values]
    return RandomGenerator(times)


engagement_delay = engagement_delay_generator()


def user_retention_coeff_gen():
    '''Generates user retention coefficients using Gompertz distribution'''
    values = scipy.stats.gompertz.rvs(3, size=1000)
    return RandomGenerator(values)


next_user_retention_coeff = user_retention_coeff_gen()

event_fields_and_defaults = [ \
    ['app_id',            ''], \
    ['user_id',           ''], \
    ['event_time',        ''], \
    ['country',           ''], \
    ['city',              ''], \
    ['device_type',       ''], \
    ['device_vendor',     ''], \
    ['ad_network',        ''], \
    ['campaign',          ''], \
    ['site_id',           ''], \
    ['event_type',        ''], \
    ['event_name',        ''], \
    ['organic',           'False'], \
    ['days_from_install', '0'], \
    ['revenue',           '0'] \
]

tsv_header_printed = False


def print_tsv_header():
    global tsv_header_printed
    if not tsv_header_printed:
        print('\t'.join([f for f, _ in event_fields_and_defaults]))
        tsv_header_printed = True


def print_event_tsv(options, event):
    if options.output_header:
        print_tsv_header()
    try:
        print('\t'.join(
            [str(event.get(f, d)) for f, d in event_fields_and_defaults]))
    except UnicodeEncodeError:
        pass


def print_event_json(options, event):
    print(json.dumps(event))


def send_event(options, env, event_type, info, install_time=None):
    '''Generates events from the info, and outputs it'''
    event = info.copy()
    event_time = env.now * 1000
    event['event_time'] = event_time
    event['event_type'] = event_type
    if install_time is not None:
        event['days_from_install'] = int(
            (event_time - install_time) / 86400000)
    options.output_format(options, event)
    options.events_num = options.events_num - 1
    if options.events_num == 0:
        sys.exit(0)
    return event_time


def engagements(env, options, frequency=100):
    '''Generates new possible engagements based on random user and application'''
    while True:
        app_id, nonorg_probability, session_delay, events_indices = next_popular_app(
        )
        device = random_device()
        info = {
            'user_id': random.getrandbits(32),
            'app_id': app_id,
            'device_type': device.name,
            'device_vendor': device.vendor(),
            'organic': random.random() > nonorg_probability
        }
        env.process(
            engagement(env, options, session_delay, events_indices, info))
        yield env.timeout(frequency)


def engagement(env, options, session_delay, events_indices, info):
    '''Proceed through the engagement process, and generate activity'''

    if info['organic']:
        country = random_country()
        info['country'] = country
        info['city'] = random_city(country)
    else:
        event_type = 'click' \
                if random.random() < options.click_through_rate else 'impression'
        info['ad_network'] = next_popular_adnetwork()
        campaign = random_campaign(env.now)
        info['campaign'] = str(campaign)
        info['country'] = campaign.country
        info['city'] = random_city(campaign.country)
        info['site_id'] = next_random_siteid()
        send_event(options, env, event_type, info)

    yield env.timeout(engagement_delay())

    install_time = send_event(options, env, 'install', info)

    user_retention_coeff = next_user_retention_coeff()
    retention_days = 100 * user_retention_coeff
    if info['organic']:
        retention_days *= (retention_days * 0.012) + 1.46
    retention_days = int(retention_days)
    total_seconds = retention_days * 86400

    while total_seconds > 0:
        send_event(options, env, 'session', info, install_time)

        for e in range(events_per_session_gen()):
            inapp_delay = random.randint(3, 20)
            yield env.timeout(inapp_delay)
            inapp_info = info.copy()
            inapp_info['revenue'] = revenue_gen()
            inapp_info['event_name'] = random_inapp_event(events_indices)
            send_event(options, env, 'inappevent', inapp_info, install_time)
            total_seconds -= inapp_delay

        total_seconds -= session_delay
        yield env.timeout(session_delay)


def parse_args():
    parser = argparse.ArgumentParser(usage='usage: %(prog)s [options]')
    parser.add_argument(
        '-v', '--version', action='version', version='%(prog)s 1.0')

    parser.add_argument(
        '-n',
        '--events-number',
        dest='events_num',
        type=int,
        default=int(os.getenv('EVENTS_NUMBER', '-1')),
        help='Number of events to generate')

    parser.add_argument(
        '-c',
        '--click-through-rate',
        dest='click_through_rate',
        type=float,
        default=float(os.getenv('CLICK_THROUGH_RATE', '0.005')),
        help='Click-through rate')

    parser.add_argument(
        '-r',
        '--campaigns-number',
        dest='campaigns_num',
        type=int,
        default=int(os.getenv('CAMPAIGNS_NUMBER', '10000')),
        help='Number of running campaigns at any time')

    def parse_datetime(d):
        return datetime.datetime.strptime(d,
                                          '%Y-%m-%d').replace(tzinfo=pytz.UTC)

    parser.add_argument(
        '-s',
        '--start-date',
        dest='start_date',
        help='Events start date in format YYYY-MM-DD',
        default=parse_datetime(os.getenv('START_DATE', '2015-01-01')),
        type=parse_datetime)

    def parse_output_format(f):
        if f == "json":
            return print_event_json
        if f == "tsv":
            return print_event_tsv
        raise "Unsupported output format: %s" % f

    parser.add_argument(
        '-f',
        '--output-format',
        dest='output_format',
        help='Supported formats are: json, tsv',
        default=os.getenv('OUTPUT_FORMAT', 'json'),
        type=parse_output_format)

    parser.add_argument(
        '-H',
        '--output-header',
        dest='output_header',
        help='Whether to output TSV header',
        default=os.getenv('OUTPUT_HEADER') is not None,
        action='store_true')

    return parser.parse_args()


if __name__ == '__main__':
    options = parse_args()
    env = simpy.Environment(
        initial_time=int((options.start_date - datetime.datetime(
            1970, 1, 1, 0, 0, 0, 0, pytz.UTC)).total_seconds()), )
    init_campaigns(env.now, options.campaigns_num)
    env.process(engagements(env, options))
    env.run()
