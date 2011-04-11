#!/usr/bin/env python
# -*- coding: utf-8 -*-

set -eux
find . -name "*.prn" -exec rename ":" "10" {} \;
find . -name "p??id.prn" -exec rename "p" "p0" {} \;

#rename : 10 *.prn
#rename p p0 p??id.prn
