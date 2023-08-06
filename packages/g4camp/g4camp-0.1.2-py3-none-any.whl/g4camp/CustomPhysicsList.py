from geant4_pybind import *
#from MuNuclearBuilder import MuNuclearBuilder

class CustomPhysicsList(G4VModularPhysicsList):

  def __init__(self, optics=True):
    super().__init__()

    self.phys_constructors = {}

    self.phys_constructors["decay"] = G4DecayPhysics()
    self.phys_constructors["em"] = G4EmStandardPhysics_option1()   # G4EmStandardPhysics(),  G4EmStandardPhysics_option4()
    self.phys_constructors["em_extra"] = G4EmExtraPhysics()  # for muon nuclear interaction
#    self.phys_constructors["rad_decay"] = G4RadioactiveDecayPhysics()
    
    if optics:
      self.phys_constructors["optical"] = G4OpticalPhysics()

    for key, phys in self.phys_constructors.items():
      self.RegisterPhysics(phys)
      phys.SetVerboseLevel(0)

