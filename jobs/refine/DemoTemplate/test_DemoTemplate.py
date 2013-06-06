#!/usr/bin/env python
# -*- coding: utf-8 -*-

from refine.worker.mapper import Mapper
import os
import urllib
import httplib
from time import sleep
import re
import socket
import time
import sys
import hashlib
import datetime
import nltk
from collections import defaultdict
from pyes import *
from pyelasticsearch import *
from pyelasticsearch.client import es_kwargs
from surfiki_DemoTemplate_stream import SurfikiDemoTemplateStream
from surfiki_DemoTemplate_reducer import SurfikiDemoTemplateReducer

class SurfikiDemoTemplateMapper():
    job_type = 'DemoTemplate'
    def map(self, hits):
        #time.sleep(0.5)
        print os.getpid()
        return list(self.split_words(hits))

    def split_words(self, hits):
        for hit in hits:
            keywords = hit['_source']['strKeywords']
            for word in keywords.split(','):
                if len(word.strip()) >= 2:
                    yield word.strip().strip('.').strip(','), 1

def main():
    start = time.time()
    hits = SurfikiDemoTemplateStream().process(None, None)
    print "input stream took %.2f" % (time.time() - start)
    #for hit in hits:
                #print hit['_source']['strKeywords']
    start = time.time()
    mapper = SurfikiDemoTemplateMapper()
    results = []
    results.append(mapper.map(hits))
    print "mapping took %.2f" % (time.time() - start)

    start = time.time()
    SurfikiDemoTemplateReducer().reduce(None, results)
    print "reducing took %.2f" % (time.time() - start)

if __name__ == '__main__':
    main()
