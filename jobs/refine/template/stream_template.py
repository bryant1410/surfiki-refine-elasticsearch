#!/usr/bin/env python
# -*- coding: utf-8 -*-

from os.path import abspath, dirname, join
import httplib
import time
import json

import sys
from datetime import datetime, date
from decimal import Decimal
import unittest

import requests
import six

# Test that __all__ is sufficient:
from pyelasticsearch import *
from pyelasticsearch.client import es_kwargs


class CLASSNAME:
    job_type = 'JOBTYPE'
    group_size = 20

    def process(self, app, arguments):
        batch_size = 1000
        # Init the instance for search
        es = ElasticSearch('YOUR ELASTIC SEARCH ENDPOINT')
        current = int(round(time.time() * 1000))
        # 15 minutes ago
        begin = current - (1000 * 60 * 60) / 4
        # Query Example
        query = {
            "query": {
            "bool": {
                "must": [
                {
                    "range": {
                    "YOUR INDEX DATE FIELD": {
                        "from": begin,
                        "to": current
                    }
                    }
                }
                ],
                "must_not": [],
                "should": []
            }
            },
            "from": 0,
            "size": 100000,
            "sort": [],
            "facets": {}
        }
        result = es.search(
            query,
            index='YOUR ELASTIC SEARCH INDEX',
            es_from=0,
            size=0)
        # Get the total number of hits, preparing for paging control
        total = int(str(result['hits']['total']))
        print total
        query_res = []
        # Paging handling using from--size ES Query API
        for index in range(0, (total - 1) / batch_size + 1):
            result = es.search(
                query,
                index='YOUR ELASTIC SEARCH INDEX',
                es_from=index *
                batch_size,
                size=batch_size)
            hits = result['hits']['hits']
            query_res = query_res + hits
        return query_res
