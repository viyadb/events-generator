from __future__ import absolute_import
from lib.random import WeightedRandomGenerator, RandomGenerator
from lib.countries import random_country

import numpy
import random


def campaign_length_generator():
    '''Generates length of running campaigns in days'''
    values = numpy.random.beta(2, 8, 500)
    lengths = [int(l * 10) for l in values]
    lengths = [l for l in lengths if l > 0]
    return RandomGenerator(lengths)


random_campaign_length = campaign_length_generator()


def days_from_epoch(time):
    '''This is not a correct days from epoch representation, but it's only
     used as a campaign identifier'''
    return int(time / 86400)


class Campaign(object):
    def __init__(self, idx, time_now):
        self.idx = idx
        self.start_date = days_from_epoch(time_now)
        self.length = random_campaign_length()
        self.country = random_country()

    def update(self, time_now):
        new_date = days_from_epoch(time_now)
        if new_date - self.start_date > self.length:
            self.start_date = new_date

    def __str__(self):
        return 'campaign_{0}_{1}'.format(self.start_date, self.idx)


def campaign_index_generator(num_campaigns):
    dist = numpy.random.beta(2, 8, num_campaigns)
    return WeightedRandomGenerator([i for i in range(num_campaigns)], dist)


def init_campaigns(time_now, num_campaigns):
    global campaigns
    global random_campain_idx
    campaigns = [Campaign(i, time_now) for i in range(num_campaigns)]
    random_campain_idx = campaign_index_generator(num_campaigns)


def random_campaign(time_now):
    global campaigns
    campaign = campaigns[random_campain_idx()]
    campaign.update(time_now)
    return campaign
