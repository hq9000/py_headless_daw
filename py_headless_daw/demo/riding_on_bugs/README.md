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

![image](https://user-images.githubusercontent.com/21345604/93955793-3a48fd00-fd59-11ea-88d9-6f94e2023c9f.png)

when rendered, the waveform looks somewhat like this:

![image](https://user-images.githubusercontent.com/21345604/93956098-09b59300-fd5a-11ea-9b53-6305e304d7fa.png)



## Implementation

the demo is mainly implemented in `RidingOnBugs` class exposing a
`def render(self, output_file: str)` method

## How to run

just run the `build.py` script
  
