#!/usr/bin/python
# -*- coding: utf-8 -*-

from collections import defaultdict
import nltk
import os
import sys
from os.path import abspath, dirname, join
from datetime import datetime, date
from decimal import Decimal
import unittest

import requests
import six
import time
# Test that __all__ is sufficient:
from pyelasticsearch import *
from pyelasticsearch.client import es_kwargs

class CLASSNAME:
    job_type = 'JOBTYPE'

    def reduce(self, app, items):
        # Init the instance for search
        es = ElasticSearch('http://api.surfiki.io/search/')
        word_freq = defaultdict(int)
        for line in items:
            for word, frequency in line:
                word_freq[word] += frequency
        # make all things in word_freq to a test index
        for word in word_freq:
            key = {}
            key['name'] = word
            key['count'] = word_freq[word]
            es.index("test", "jdbc", key)
        return word_freq
