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
from surfiki_JOBTYPE_stream import SurfikiJOBTYPEStream
from surfiki_JOBTYPE_reducer import SurfikiJOBTYPEReducer


class SurfikiJOBTYPEMapper():
    job_type = 'JOBTYPE'
    MAPPER_CONTENT


def main():
    start = time.time()
    hits = SurfikiJOBTYPEStream().process(None, None)
    print "input stream took %.2f" % (time.time() - start)
    # for hit in hits:
                # print hit['_source']['strKeywords']
    start = time.time()
    mapper = SurfikiJOBTYPEMapper()
    results = []
    results.append(mapper.map(hits))
    print "mapping took %.2f" % (time.time() - start)

    start = time.time()
    SurfikiJOBTYPEReducer().reduce(None, results)
    print "reducing took %.2f" % (time.time() - start)

if __name__ == '__main__':
    main()
