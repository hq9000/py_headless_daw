# "Riding on Bugs" demo song

## Overview

This "song" has tree tracks

- reverberated bass drum 
  - this is a `SamplerTrack` where  `bd.wav`-based clips are evenly placed
  - this track has a reverb plugin (a `VstPlugin` using `DragonflyRoomReverb-vst.x86_64-linux`)
  
- synth track
  - an audio track with an instance of `VstPlugin` which loads `amsynth-vst.x86_64-linux`
- midi track
  - this track is an input for the synth track and consists of a single midi clip playing a short note
- drum synth track
  - an audio track with an instance of `DrumSynthPlugin`
- midi track
  - this track is an input for the drum synth track and consists of a single midi clip playing a short note


![image](https://user-images.githubusercontent.com/21345604/99762138-dfd5de00-2b08-11eb-9a29-af1ececc83f8.png)


## Implementation

the demo is mainly implemented in `RidingOnBugs` class exposing a
`def render(self, output_file: str)` method

## How to run

just run the `build.py` script
  
