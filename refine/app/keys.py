#!/usr/bin/python
# -*- coding: utf-8 -*-

ALL_KEYS = 'surfiki::*'

# MAPPER KEYS
MAPPERS_KEY = 'surfiki::mappers'
MAPPER_INPUT_KEY = 'surfiki::jobs::%s::input'
MAPPER_OUTPUT_KEY = 'surfiki::jobs::%s::%s::output'
MAPPER_ERROR_KEY = 'surfiki::jobs::%s::errors'
MAPPER_WORKING_KEY = 'surfiki::jobs::%s::working'
LAST_PING_KEY = 'surfiki::mappers::%s::last-ping'
WORKING_KEY = 'surfiki::mappers::%s::working'

# JOB TYPES KEYS
JOB_TYPES_KEY = 'surfiki::job-types'
JOB_TYPES_ERRORS_KEY = 'surfiki::jobs::*::errors'
JOB_TYPE_KEY = 'surfiki::job-types::%s'
JOB_STATUS_KEY = 'surfiki::job-types::status::%s'
# JOB PORT KEY
JOB_PORT_KEY = 'surfiki::jobs::%s::port'

# STATS KEYS
PROCESSED = 'surfiki::stats::processed'
PROCESSED_SUCCESS = 'surfiki::stats::processed::success'
PROCESSED_FAILED = 'surfiki::stats::processed::fail'

# EDIT FILE KEY
CURRENT_EDIT = 'surfiki::edit:current'
CURRENT_CONTENT = 'surfiki::edit:currentcontent'

# JOB TEST RESULT KEY
CURRENT_RESULT = 'surfiki::test::job::content'
JOB_TEST = 'surfiki::test::job::run'

# ElasticSearch Endpoint setting
ELASTIC_ENDPOINT = 'settings::endpoint'
