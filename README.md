## Surfiki Refine for Elasticsearch (Non Distributed Version)

- If you are interested in the distributed version of Refine, please contact [Intridea](http://www.intridea.com). As well, Intridea offers cloud hosted options for Refine. Please reach out to us anytime so we can help!


### Python Map-Reduce Transformation/Extraction/Manipulation Tier for Elasticsearch Indices

##### Part of the Surfiki Data Engine
- [Surfiki REBIN](http://intridea.github.io/REBIN/)
- [Surifki Developer API](http://developer.surfiki.com/)
- [Surfiki.com](http://www.surfiki.com)


### What is Refine?


Designed to work with Elasticsearch indices and API. Refine allows you to take an input stream, transform and or manipulate it for your needs, then output it in a variety of formats.


With the variety of Elasticsearch uses seen within its ecosystem (Search, Data Stores, API), a powerful and extensible processing tier was needed to meet Intridea’s needs. Our belief, is this can fit in to your Elasticsearch environment as well. And in turn, provide you with additional transformation and or manipulation capabilities.


At its heart, Refine is a collection of scripts, written by you in Python.


### How does it work?


Technically, Refine is Map-Reduce, which for each job you define incorporates:


 - A stream script defines the source of your data. A query’s results (In the case of Elasticsearch) A file or files, or a Web API such as Twitter.


 - A mapper script takes the input, divides it into smaller sub-problems, and distributes them to workers. 

- A worker may do this again in turn, leading to a multi-level tree structure. The worker processes the smaller problem, and passes the answer back to its master.


 - A reducer script collects the answers to all the sub-problems and combines them in some way to form the output – the answer to the problem it was originally trying to solve.


 - You can add as many scripts that your job may require, however the core is the stream, mapper and reducer scripts.
 
### What are some cool features?

- Online Browser based code editing, job management and results collection.

- Job Testing (Syntax & Job functions)

- Job Scheduling

- Job Duplication

- Live CLI

- Distributed (Commodity Servers) Jobs and Management (If you are interested in the distributed version of Refine, please contact [Intridea](http://www.intridea.com).)

<a href="http://www.flickr.com/photos/95752811@N04/8738542001/" title="refine1 by NyströmAnthony, on Flickr"><img src="http://farm8.staticflickr.com/7286/8738542001_8b182dfcde.jpg" width="376" height="345" alt="refine1"></a>
<a href="http://www.flickr.com/photos/95752811@N04/8738542005/" title="refine2 by NyströmAnthony, on Flickr"><img src="http://farm8.staticflickr.com/7285/8738542005_763e502a33.jpg" width="376" height="345" alt="refine2"></a>
<a href="http://www.flickr.com/photos/95752811@N04/8739661106/" title="refine3 by NyströmAnthony, on Flickr"><img src="http://farm8.staticflickr.com/7283/8739661106_1894aec094.jpg" width="376" height="345" alt="refine3"></a>
<a href="http://www.flickr.com/photos/95752811@N04/8738541955/" title="refine4 by NyströmAnthony, on Flickr"><img src="http://farm8.staticflickr.com/7282/8738541955_ccac2229ee.jpg" width="376" height="345" alt="refine4"></a>

### What are some examples?


- Combining data from multiple indices in to a new index. With Refine you can either do this ad hoc or on a scheduled basis.


- Splitting data from a single index in to new indices based upon some criteria. Refine makes this relatively simple to perform.


- Statistical facets can be taxing on the heap. You can use Refine to process/transform/count this data and expose within a new index on a set schedule.


- Transforming data already indexed with additional data. For example, some data has location information (lat, long) however you also want to store meta data associated with those locations Such as State, City and County information. While it makes sense to do some of this in line, with Refine you can do it after the initial data is already indexed.


- Accessing third party API's to append data to existing indexed data. With Refine, accessing those API’s, injecting and or manipulating is a core feature.


- Given a body of text, you can use Refine to split your stream into its separate words, perform a word count for the given word, then reduce it to a de-duped sorted array.


- Given a collection of results, you can use Refine to further score each result against a series of 
validation criteria; such as geographic region or category data.


- Need text to appear in various ways, before it can be processed further? Use Refine to prepend suffixes or concatenate strings, and dynamically add these as new attributes.


### Open Source Projects utilized:


- [redis](http://redis.io/)
- [Paramedic](https://github.com/karmi/elasticsearch-paramedic)
- [Sense](https://github.com/bleskes/sense)
- [r3](https://github.com/heynemann/r3)
- [Python Dev Bootstrap](http://anthonynystrom.github.io/python-dev-bootstrap/)
- [Lookout](https://github.com/delan/lookout)
- [Flask](http://flask.pocoo.org/)
- [Twitter Bootstrap](http://twitter.github.io/bootstrap/)
- [Cloud9](https://github.com/ajaxorg/cloud9/)
- [Python](http://python.org/)
- [PyFlakes](https://pypi.python.org/pypi/pyflakes)
- [ujson](https://pypi.python.org/pypi/ujson)
- [pyelasticsearch](https://github.com/rhec/pyelasticsearch)
- [node.js](http://nodejs.org/)
- [watchdog](http://pythonhosted.org/watchdog/)

Special Mention:

Many thanks go out to Bernardo Heynemann for his excellent work with r3 and c9.io for Cloud9.


---


### Installation Instructions

Supported Operating System: LINUX

Assume this is a fresh install on a clean [Ubuntu Server Distribution](http://www.ubuntu.com/download/server) as root

Create a root user

	$ sudo passwd root

Logout and back in as root

	$ logout
	# Log back in as root

Create a crontab file for root user (Since this is assuming a fresh ubuntu install, there is no crontab for root. We need to create one as Surfiki Refine will look for it upon startup for job scheduling. If you already have a root crontab file, then disregard.)

	To Check if you have a crontab for root already existing:
	
	$ crontab -l
	# If you are shown a list of entries then you have a crontab for root. Otherwise, continue below:

	$ select-editor
	# Select number 2 option-> nano
	
	$ crontab -e
	# Enter (on any line): @yearly /ls -al
	# Save the file
	

Update and install packages

	$ apt-get update
	$ apt-get install -y build-essential openssl libssl-dev pkg-config git-core g++ curl libxml2-dev python-dev python-pip ssh

Clone Project in to root (/root/)
 
    $ cd /root (If not already there)
    $ git clone https://github.com/intridea/surfiki-refine-elasticsearch.git refine
    
Install redis

	$ cd /usr/local/src
	$ wget http://redis.googlecode.com/files/redis-2.6.10.tar.gz
	$ tar -xzf redis-2.6.10.tar.gz
	$ cd redis-2.6.10/

	$ make
	$ make install

	$ cd utils

	$ ./install_server.sh
	# Select all the defaults as presented
	
Copy the config for redis and set defaults

	$ cd /root/refine
	$ cp redis.conf /etc/redis/6379.conf
	
	# Restart redis
	$ /etc/init.d/redis_6379 stop
	$ /etc/init.d/redis_6379 start
	
    
Install Dependencies
	
	$ cd /root/refine
	$ pip install -r requirements.txt

The editor portion of Refine uses a specific version of node.js:

Install node.js v0.6.21
	
	$ apt-get update

	$ cd /usr/local/src
	$ wget http://nodejs.org/dist/v0.6.21/node-v0.6.21.tar.gz
	$ tar -xzf node-v0.6.21.tar.gz
	$ cd node-v0.6.21/

	$ ./configure
	$ make
	$ make install
	
Update npm

	$ npm install -g npm
	
Install Cloud9 Editor

	Install and build modules (from the Surfiki Refine Repo on your filesystem)
	
	$ cd /root/refine/cloud9
	$ npm install

	Install cloud9 (from the Surfiki Refine Repo on  your filesystem) as an upstart job 
	
	$ cp cloud9.conf /etc/init/
	$ start cloud9
	
Configure Surfiki Refine

	$ nano /refine/web/config.py
	
	#!/usr/bin/python
	# -*- coding: utf-8 -*-

	DEBUG=True
	SECRET_KEY='development key'

	WEB_HOST='0.0.0.0' (NOTE: You will need to enter an IP for your VM or Server)
	WEB_PORT=8888
	UPLOAD_FOLDER='/root/refine/jobs/refine/'

	REDIS_HOST='0.0.0.0'
	REDIS_PORT=6379
	REDIS_PASS='surfikiMR'
	
Starting Surfiki Refine

	$ cd /root/refine
	$ ./server_startup.sh
	
Stopping Surfiki Refine

	$ cd /root/refine
	$ ./server_cleanup.sh
	
##### Enter the IP of the server hosting Refine and append the port: 8888

---


    
### Usage Instructions

Included with Refine is a template job. Let's walk through using that as the basis for any job you may need to write.

1. On the Jobs Sub Tab, click the "Create New Job" button.
2. You can either manually upload your files, or allow Refine to build the required files for you and populate with the provided template. Using the "Automatically Generate Job Files".
	- Input your desired Job Name.
  - Optionally provide a Job Desc: (Description)
  - Click the submit button.
3. Return to the Jobs Sub Tab and you will see your new job listed.
4. Click your job and set the number of mappers you want created when your job runs. The default is 5. If you decide the default value is fine, you still need to click the Set/Save (Required) button.
5. You will now see a link next to the Job Result Link label. Clicking this link will start the job. You will notice a new tabs opens in your browser. This is where your results will be shown. This is the case even if your job results are written to an index. Closing the tab will cancel the job. 

Notes: If you choose to schedule your job, the secondary results tab will not be available unless you manually click the Job Results Link. As well, while the results tabs are open, you are free to move around the sub tabs examining current load characteristics either upon the Server running the job and or your Elasticsearch cluster. This can be helpful in understanding how your code/job is functioning with your cluster.

Job Testing: You can easily test your job before actually running it. Simply, click the Enable Test button, then click the link created next to the Job Test Result Link. You will notice a new tabs opens in your browser. This is where your test results will be shown.

---

### Templates 

This assumes you have an Elasticsearch index with keywords and a date field that has been updated in the list n minutes. You likely will need to modify for your particular schema/s. It is a template to assist in understand the structure and use.



	#!/usr/bin/env python
	# -*- coding: utf-8 -*-

	# FILE: surfiki_DemoTemplate_stream.py


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


	class SurfikiDemoTemplateStream:
    	job_type = 'DemoTemplate'
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
                	es_from=index * batch_size,
                	size=batch_size)
            	hits = result['hits']['hits']
            	query_res = query_res + hits
        	return query_res

        
---

	#!/usr/bin/env python
	# -*- coding: utf-8 -*-

	# FILE: surfiki_DemoTemplate_mapper.py
	

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


	class SurfikiDemoTemplateMapper(Mapper):
    	job_type = 'DemoTemplate'

    	def map(self, hits):
        	# time.sleep(0.5)
        	print os.getpid()
        	return list(self.split_words(hits))

    	def split_words(self, hits):
        	for hit in hits:
            	keywords = hit['_source']['YOUR KEYWORD FIELD WITHIN YOUR INDEX 
            		COMMA DELIMITED']
            	for word in keywords.split(','):
                	if len(word.strip()) >= 2:
                    	yield word.strip().strip('.').strip(','), 1



        
---

	#!/usr/bin/env python
	# -*- coding: utf-8 -*-

	# FILE: surfiki_DemoTemplate_reducer.py


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


	class SurfikiDemoTemplateReducer:
    	job_type = 'DemoTemplate'

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


        
---

	
	#!/usr/bin/python
	# -*- coding: utf-8 -*-
	
	#FILE: app_config.py


	# DescDemonstration Job Template
	INPUT_STREAMS = [
    	'DemoTemplate.surfiki_DemoTemplate_stream.SurfikiDemoTemplateStream']
	REDUCERS = [
    	'DemoTemplate.surfiki_DemoTemplate_reducer.SurfikiDemoTemplateReducer']
    	
---

### Code Editing

All job code editing is performed online via the browser based IDE. If you prefer, you can edit offline and upload them; whichever is your preference.

<a href="http://www.flickr.com/photos/95752811@N04/8917271544/" title="CodingInterface by NyströmAnthony, on Flickr"><img src="http://farm6.staticflickr.com/5449/8917271544_2294a111c7.jpg" width="500" height="424" alt="CodingInterface"></a>

Above you see the four specific areas within the interface. When you select the edit button from the jobs sub tab, the editor will open with all files that define that job. You can make your edits and your changes will auto save. Because your stream stream file is used for the primary queries against your Elasticsearch cluster, it is convientent to also have the Elasticsearch Query Editor within the IDE such that you can formulate your query in advance of inlcuding it within the job.

-

When your changes are complete, click the Return To Jobs menu item. As seen below.

<a href="http://www.flickr.com/photos/95752811@N04/8916658237/" title="ReturnToJobs by NyströmAnthony, on Flickr"><img src="http://farm3.staticflickr.com/2856/8916658237_5624d30aac.jpg" width="500" height="389" alt="ReturnToJobs"></a>

 
