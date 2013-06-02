#!/usr/bin/python
# -*- coding: utf-8 -*-

from refine.app.handlers import BaseHandler

class HealthcheckHandler(BaseHandler):
    def get(self):
        self.write('WORKING')

