from g4camp.g4camp import g4camp
from time import time
import sys

n_events = 10
gun_args = { 'particle':   'e-', 
             'energy_GeV': 1000, 
             'position_m': [0,0,0],
             'direction':  [0,0,1]  }
optics = True

app = g4camp(primary_generator='gun', gun_args=gun_args, optics=optics)
app.setSkipMinMax(0.0001, 0.01)
app.setPhotonSuppressionFactor(100)
app.configure()

time0 = time()
for data in app.run(n_events):
    vertices = data.vertices
    tracks = data.tracks
    photon_cloud = data.photon_cloud
    print(f"{len(photon_cloud):>10}(x{app.ph_suppression_factor}) photons, {len(tracks):>6} tracks, {len(vertices):>6} vertices;")
print(f"# Run time:  {(time()-time0):.2f} sec, {((time()-time0)/n_events):.2f} sec/event")
