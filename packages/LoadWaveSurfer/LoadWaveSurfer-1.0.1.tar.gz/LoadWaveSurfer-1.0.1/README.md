![PyPI](https://img.shields.io/pypi/v/LoadWaveSurfer?color=g)
# LoadWaveSurfer
 Load and parse ephys data acquired using Janelia's WaveSurfer.

## Example usage
```
from loadwavesurfer import loadws

# initialize loadws object
f = loadws(inputFile, filter=False)

# access the data as a named tuple
f.data()

# or individually
f.data().volt
f.data().curr
f.data().time

# and their units
voltage_units, current_units, time_units = f.units()

# reconstruct current or voltage stimulation parameters
f.stimParams()

# get sampling rate
f.sampleRate()

# get timestamp at start of recording, in UNIX time
f.clock()
```