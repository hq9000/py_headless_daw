# Simple EDM reference producer

## Overview

The project includes and example reference producer called "Simple EDM producer".

see `simple_edm_producer.py` and `simple_edm_producer_test.py`

This producer, although not currently generating musically satisfying output, is meant to serve as a reference producer implementation.

If you intend to write your own producer, the best way to get familiar with existing production approaches would be to study the (not so big) code of this producer.

## Details

Below go a human-readable introduction to what actually happens there:

The producer, given a seed, generates a project consisting of:
1. a base drum track using built-in drum synthesizer
1. from 2 to 4 synth tracks using `amsynth` plugin
1. a reverb send track (`dragonfly reverb`) that synth tracks send to

synths play some pseudo-random notes, patches are, as well, chosen pseudo-randomly.

By pseudo-randomness it is meant that random decisions, though belonging to required distribution,
are totally deterministic. I.e. given the same seed, a producer is expected to generate identical projects each time it is run. 

see `seed.py` to get familiar with the "heart" of this deterministic randomness.