# "Riding on Bugs" demo song

## Overview

This "song" has two tracks

- reverberated bass drum 
  - this is a `SamplerTrack` where  `bd.wav`-based clips are evenly placed
  - this track has a reverb plugin (a `VstPlugin` using `DragonflyRoomReverb-vst.x86_64-linux`)
  
- synth track
  - an audio track with an instance of `VstPlugin` which loads `amsynth-vst.x86_64-linux`
- midi track
  - this track is input for the synth track and consists of a single midi clip playing a short note

![image](https://user-images.githubusercontent.com/21345604/93659049-ee8d0f80-fa49-11ea-91b4-8085965048e4.png)

when rendered, the waveform looks somewhat like this:

![image](https://user-images.githubusercontent.com/21345604/93659060-19776380-fa4a-11ea-9abb-09bd996b9e9c.png)

## Implementation

the demo is mainly implemented in `RidingOnBugs` class exposing a
`def render(self, output_file: str)` method
  