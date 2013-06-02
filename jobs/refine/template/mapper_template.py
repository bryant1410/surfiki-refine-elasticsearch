#!/usr/bin/env python
# -*- coding: utf-8 -*-

from refine.worker.mapper import Mapper
import os
import nltk
import sys
import urllib
import httplib
import hashlib
from time import sleep
from datetime import datetime, date
from decimal import Decimal
import re
import json
import unittest
import socket
import requests
import six
import time
# Test that __all__ is sufficient:
from pyelasticsearch import *
from pyelasticsearch.client import es_kwargs


class CLASSNAME(Mapper):
    job_type = 'JOBTYPE'

    def map(self, hits):
        # time.sleep(0.5)
        print os.getpid()
        return list(self.split_words(hits))

    def split_words(self, hits):
        for hit in hits:
            keywords = hit['_source']['YOUR KEYWORD FIELD WITHIN YOUR INDEX COMMA DELIMITED']
            for word in keywords.split(','):
                if len(word.strip()) >= 2:
                    yield word.strip().strip('.').strip(','), 1
