from geant4_pybind import *
from g4camp.g4camp import g4camp
import sys

app = g4camp(optics=False, primary_generator='gun')
ui = G4UIExecutive(len(sys.argv), sys.argv)
visManager = G4VisExecutive("Quiet")
visManager.Initialize()
app.configure() # should be after initialization of visual manager
app.applyGeant4Command("/control/execute",  ["vis.mac"])
ui.SessionStart()
