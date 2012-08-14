#!/usr/bin/env python3

from bfdtd.bfdtd_parser import *

p = Probe()
t = Time_snapshot()
f = Frequency_snapshot()

sim = BFDTDobject()
sim.flag.iterations=10

sim.fileList = []
sim.probe_list = 439*[p]
sim.snapshot_list = []
sim.writeAll('Probes')

sim.fileList = []
sim.probe_list = []
sim.snapshot_list = 439*[t]
sim.writeAll('TimeSnapshots')

sim.fileList = []
sim.probe_list = []
sim.snapshot_list = 836*[f]
sim.writeAll('FrequencySnapshots')

# TESTING COMMANDS:
#grep -ci ^probe */*.inp
#grep -ci ^snapshot */*.inp
#grep -ci ^frequency_snapshot */*.inp

#ls -1 Probes/*.prn | wc -l
#ls -1 TimeSnapshots/*.prn | wc -l
#ls -1 FrequencySnapshots/*.prn | wc -l

#./FrequencySnapshot_IDs | xargs -n1 -I{} ls FrequencySnapshots/{} 1>/dev/null
#./TimeSnapshot_IDs | xargs -n1 -I{} ls TimeSnapshots/{} 1>/dev/null
#./probe_IDs | xargs -n1 -I{} ls Probes/{} 1>/dev/null
