#!/usr/bin/env python3

from bfdtd.bfdtd_parser import *

FREQUENCYSNAPSHOT_MAX = 836
TIMESNAPSHOT_MAX = 439
PROBE_MAX = 439
MODEFILTEREDPROBE_MAX = 43

p = Probe()
t = Time_snapshot()
f = Frequency_snapshot()
m = ModeFilteredProbe()

sim = BFDTDobject()
sim.flag.iterations=10

sim.fileList = []
sim.probe_list = PROBE_MAX*[p]
sim.snapshot_list = []
sim.writeAll('Probes')

sim.fileList = []
sim.probe_list = []
sim.snapshot_list = TIMESNAPSHOT_MAX*[t]
sim.writeAll('TimeSnapshots')

sim.fileList = []
sim.probe_list = []
sim.snapshot_list = FREQUENCYSNAPSHOT_MAX*[f]
sim.writeAll('FrequencySnapshots')

sim.excitation_list = [ExcitationWithGaussianTemplate()]

sim.fileList = []
sim.probe_list = []
sim.snapshot_list = MODEFILTEREDPROBE_MAX*[m]
sim.writeAll('ModeFilteredProbes')
