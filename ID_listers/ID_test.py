#!/usr/bin/env python3

from bfdtd.bfdtd_parser import *

p = Probe()
t = Time_snapshot()
f = Frequency_snapshot()

sim = BFDTDobject()
sim.flag.iterations=10

sim.probe_list = 439*[p]
sim.snapshot_list = []
sim.writeAll('Probes')

sim.probe_list = []
sim.snapshot_list = 439*[t]
sim.writeAll('TimeSnapshots')

sim.probe_list = []
sim.snapshot_list = 836*[f]
sim.writeAll('FrequencySnapshots')
