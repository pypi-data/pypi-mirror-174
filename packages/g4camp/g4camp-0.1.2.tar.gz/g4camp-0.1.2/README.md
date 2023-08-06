# G4CAMP: Cascade and Muon Parameterization (Geant4-based)

`g4camp` is a Pyhton module based on `Geant4` framework and `geant4_pybind` pythonization. It simulates propagation of particles in a water volume and produces Cherenkov photons.

`g4camp` simulated cascade development with production of secondary particles (e+/e- and gamma for EM cascades) and emission of Cherenkov photons.

## Main features
 - Possibility to turn on/off Cherenkov effect (affects simulation speed a lot)
 - Possibility to skip certain particles, e.g. e+/e- within an energy range [E_skip_min, E_skip_max]. These particles are killed and their vertex is saved.

## Output (in memory):
 - **Vertices** for e+/e- particles with E_skip_min < E_kin < E_skip_max
 - **Tracks** 
   - for all electrically charged particles above Cherenkov threshold 
   - for all other particles except optical photons
 - **Photons** from all propagated particles (skipped particles do not emit photons)


## Requirements

 - Geant4 built with CMake option `GEANT4_BUILD_TLS_MODEL=global-dynamic`


## Installation

```bash
pip install g4camp

```

## Usage

You will need a macro file for Geant4. Any standard command for Geant4 can be added to a macro file. You can see the list of available commands in the interactive mode (see "Example with visualization"). Example macro files can be found in `g4camp/examples`.

### As a module

Assume that you have a macro file for Geant4 in your working directory (e.g. `electroms.mac`). 

```python
from g4camp.g4camp import g4camp
import sys

n_events = 10

app = g4camp()
app.setMacro("electrons.mac")
app.setSkipMinMax(0.001, 0.05)
app.configure()
for data in app.run(n_events):
    vertices = data.vertices
    tracks = data.tracks
    photons = data.photon_cloud
```

### Example with visualization

```bash
cd /path/to/g4camp
python3 example_vis.py
```

Make sure that you have `default.mac` and `vis.mac` macro files in your working directory. 

### As a standalon application

You need a symlink to `run_g4camp.py` script and a macro file:

```bash
ln -s /path/to/g4camp/run_g4camp.py
cp /path/to/g4camp/macro.mac .
```

You may modify `macro.mac` using standard Geant4 commands. The full list of available commands can be found in the interactive mode (see `Example with vizualization' above).

Use `run_g4camp.py` to generate 10 muons configured in `muons.mac` skipping e+ and e- with E within [0.001, 0.05] GeV energy range:

```bash
python3 run_g4camp.py -n 10 -m muons.mac --skip_min 0.001 --skip_max 0.05 -o output.h5
```

It outputs vertices, tracks and photons into a HDF5 file.
