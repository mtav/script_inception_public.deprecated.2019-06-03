#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import getopt

class Usage(Exception):
  def __init__(self, msg):
    self.msg = msg
