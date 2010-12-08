#!/usr/bin/env python

import schemepy as scheme

vm = scheme.VM()
vm.load('values.ctl')
print vm.get('foo')
print vm.get('bar')
print vm.get('foobar')
