# py_headless_daw
A GUI-less DAW (Digital Audio Workstation) for producing electronic music using python

## Links to detailed documentation

Here are links to more in-depth docs on several aspects of the system:

- [Reference producer implementation](doc/simple_edm_producer.md)
  - an example of a "producer" that generates random "songs". This is meant to be a reference for "real" producers' implementations.
- [Drum synth](doc/drum_synth_plugin.md)
- [Readme for "Riding on Bugs" demo project](py_headless_daw/demo/riding_on_bugs/README.md)

## Main concepts

To create some audio with this library, the 3-step workflow described below is to be followed.
Each step of the workflow uses the output artifact produced by the previous one:

- Step 1: create a project
  - **output:** an instance of `Project` class
- Step 2: compile a project
  - **output**: a pair of so called "output stream nodes"
- Step 3: render audio 
  - **output:** a wave file

![image](https://user-images.githubusercontent.com/21345604/92206579-6b3bbd80-ee90-11ea-8f86-7fe2842838cc.png)

Below go more detailed descriptions of concepts related to each step of the workflow. 

### Demo project

There is a demo project that can be used as a reference. Find its more dertailed readme here:

[Readme for "Riding on Bugs" demo project](py_headless_daw/demo/riding_on_bugs/README.md)


### Create a Project

A project (an instance of `Project` class), is, essentially, a group of interconnected tracks (`Track` class)

Among tracks, one is special: the "master". This is the track that project object refers to, the rest of the tracks can be discovered through track connections.

Basically, the set of tracks is a bi-directional graph where every track knows its inputs and outputs.

![image](https://user-images.githubusercontent.com/21345604/92208124-38df8f80-ee93-11ea-905e-985ad21df904.png)

Apart from inputs and outputs, each track has a **chain of "plugins"** used to modify data prior to passing it to the track's outputs.

#### Types Of Tracks

![track_hierarchy](https://user-images.githubusercontent.com/21345604/92209351-84933880-ee95-11ea-863b-8bed6a37e996.png)

#### Midi Track
A track that produces midi data. Midi data is stored in `MidiClip` instances.
Importantly, `MidiTrack` can only be connected to an `AudioTrack` whose plugin chain has a synth as the first plugin.

#### Audio Track
A track that takes its inputs, applies some processing to it (using plugins) and outputs audio to downstream tracks.

#### Sampler Track
A special case of audio track that has no inputs (it does not expect any track to feed audio into it). 
Instead, it maintains the list of `AudioClip` instances that are used to produce the data to feed into the head of its plugin chain.
In any other respect, `SamplerTrack` is like any other `AudioTrack`

### Compile a Project

On a lower level, the sound-producing structure consists of interconnected units:

![image](https://user-images.githubusercontent.com/21345604/92205525-89082300-ee8e-11ea-858a-be7e0aeda101.png)



Every unit is comprised of:

- a number of input nodes
- a number of output nodes
- a processing strategy that knows how to use data taken from input nodes to produce output data to be sent to output ndoes

There are two types of nodes:

- **stream nodes**, each representing a single channel of audio (e.g. "left")
- **event nodes**, each representing a stream of events

Units can be interconnected to produce multi-stage processing. For that, connectors are used.

#### Compiling a project

Compilation of a project is turning a project instance into a list of StreamNode instances.
After successful compilation, it is possible to render stream data from these nodes to produce the resulting master.
