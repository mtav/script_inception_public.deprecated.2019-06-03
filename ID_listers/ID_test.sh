#!/bin/bash

# TESTING SCRIPT

set -eu

make -f Makefile.linux

grep -ci ^probe */*.inp

grep -ci ^snapshot */*.inp

grep -ci ^frequency_snapshot */*.inp

ls -1 Probes/*.prn | wc -l

ls -1 TimeSnapshots/*.prn | wc -l

ls -1 FrequencySnapshots/*.prn | wc -l

ls -1 ModeFilteredProbes/*.prn | wc -l

./FrequencySnapshot_IDs | xargs -n1 -I{} ls FrequencySnapshots/{} 1>/dev/null

./TimeSnapshot_IDs | xargs -n1 -I{} ls TimeSnapshots/{} 1>/dev/null

./Probe_IDs | xargs -n1 -I{} ls Probes/{} 1>/dev/null

./ModeFilteredProbe_IDs | xargs -n1 -I{} ls ModeFilteredProbes/{} 1>/dev/null
