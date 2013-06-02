#!/usr/bin/env python
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
        es = ElasticSearch('YOUR ELASTIC SEARCH ENDPOINT')
        word_freq = defaultdict(int)
        for line in items:
            for word, frequency in line:
                word_freq[word] += frequency
        # Write word_freq values to a test index (EXAMPLE WHERE RESULTS ARE
        # ADDED TO AN ELASTIC INDEX)
        for word in word_freq:
            key = {}
            key['name'] = word
            key['count'] = word_freq[word]
            es.index("YOUR NEW INDEX", "YOUR NEW INDEX", key)
        return word_freq
